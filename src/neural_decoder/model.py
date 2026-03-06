import torch
import torch.nn.functional as F
from torch import nn

from .augmentations import GaussianSmoothing
from .smartpalate_map import load_map as load_smartpalate_map

from typing import Dict, List, Optional, Sequence, Tuple


class _BaseTemporalDecoder(nn.Module):
    def __init__(
        self,
        neural_dim,
        n_classes,
        hidden_dim,
        layer_dim,
        nDays=24,
        dropout=0,
        device="cuda",
        strideLen=4,
        kernelLen=14,
        gaussianSmoothWidth=0,
        bidirectional=False,
        input_proj_dim=None,
        use_day_embed=True,
    ):
        super().__init__()

        self.layer_dim = layer_dim
        self.hidden_dim = hidden_dim
        self.neural_dim = neural_dim
        self.n_classes = n_classes
        self.nDays = nDays
        self.device = device
        self.dropout = dropout
        self.strideLen = strideLen
        self.kernelLen = kernelLen
        self.gaussianSmoothWidth = gaussianSmoothWidth
        self.bidirectional = bidirectional
        self.use_day_embed = use_day_embed
        self.input_proj_dim = input_proj_dim or neural_dim

        if input_proj_dim and input_proj_dim != neural_dim:
            self.input_proj = nn.Linear(neural_dim, input_proj_dim)
            self.actual_neural_dim = input_proj_dim
        else:
            self.input_proj = None
            self.actual_neural_dim = neural_dim
            
        self.inputLayerNonlinearity = torch.nn.Softsign()
        self.unfolder = torch.nn.Unfold(
            (self.kernelLen, 1), dilation=1, padding=0, stride=self.strideLen
        )
        if self.gaussianSmoothWidth > 0:
            self.gaussianSmoother = GaussianSmoothing(
                self.actual_neural_dim, 20, self.gaussianSmoothWidth, dim=1
            )
        else:
            self.gaussianSmoother = nn.Identity()

        if self.use_day_embed:
            self.dayWeights = torch.nn.Parameter(
                torch.randn(nDays, self.actual_neural_dim, self.actual_neural_dim)
            )
            self.dayBias = torch.nn.Parameter(torch.zeros(nDays, 1, self.actual_neural_dim))
            for x in range(nDays):
                self.dayWeights.data[x, :, :] = torch.eye(self.actual_neural_dim)
        else:
            self.dayWeights = None
            self.dayBias = None

    def _frontend(self, neuralInput, dayIdx):
        if self.input_proj is not None:
            neuralInput = self.input_proj(neuralInput)

        neuralInput = torch.permute(neuralInput, (0, 2, 1))
        neuralInput = self.gaussianSmoother(neuralInput)
        neuralInput = torch.permute(neuralInput, (0, 2, 1))

        if self.use_day_embed and self.dayWeights is not None:
            dayWeights = torch.index_select(self.dayWeights, 0, dayIdx)
            transformedNeural = torch.einsum(
                "btd,bdk->btk", neuralInput, dayWeights
            ) + torch.index_select(self.dayBias, 0, dayIdx)
            transformedNeural = self.inputLayerNonlinearity(transformedNeural)
        else:
            transformedNeural = self.inputLayerNonlinearity(neuralInput)

        # Ensure the unfolding frontend has at least one window.
        # This matters for aggressive downsampling (e.g., ds4) where some sequences can be shorter
        # than kernelLen; without padding, Unfold would produce a zero-length sequence.
        if transformedNeural.shape[1] < self.kernelLen:
            pad_t = self.kernelLen - transformedNeural.shape[1]
            transformedNeural = F.pad(transformedNeural, (0, 0, 0, pad_t))

        return torch.permute(
            self.unfolder(
                torch.unsqueeze(torch.permute(transformedNeural, (0, 2, 1)), 3)
            ),
            (0, 2, 1),
        )


class GRUDecoder(_BaseTemporalDecoder):
    def __init__(
        self,
        neural_dim,
        n_classes,
        hidden_dim,
        layer_dim,
        nDays=24,
        dropout=0,
        device="cuda",
        strideLen=4,
        kernelLen=14,
        gaussianSmoothWidth=0,
        bidirectional=False,
        input_proj_dim=None,
        use_day_embed=True,
    ):
        super().__init__(
            neural_dim=neural_dim,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            device=device,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            bidirectional=bidirectional,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
        )

        self.gru_decoder = nn.GRU(
            (self.actual_neural_dim) * self.kernelLen,
            hidden_dim,
            layer_dim,
            batch_first=True,
            dropout=self.dropout,
            bidirectional=self.bidirectional,
        )

        for name, param in self.gru_decoder.named_parameters():
            if "weight_hh" in name:
                nn.init.orthogonal_(param)
            if "weight_ih" in name:
                nn.init.xavier_uniform_(param)

        if self.use_day_embed:
            for x in range(nDays):
                setattr(self, "inpLayer" + str(x), nn.Linear(self.actual_neural_dim, self.actual_neural_dim))

            for x in range(nDays):
                thisLayer = getattr(self, "inpLayer" + str(x))
                thisLayer.weight = torch.nn.Parameter(
                    thisLayer.weight + torch.eye(self.actual_neural_dim)
                )

        if self.bidirectional:
            self.fc_decoder_out = nn.Linear(
                hidden_dim * 2, n_classes + 1
            )  # +1 for CTC blank
        else:
            self.fc_decoder_out = nn.Linear(hidden_dim, n_classes + 1)  # +1 for CTC blank

    def forward(self, neuralInput, dayIdx):
        stridedInputs = self._frontend(neuralInput, dayIdx)
        if self.bidirectional:
            h0 = torch.zeros(
                self.layer_dim * 2,
                stridedInputs.size(0),
                self.hidden_dim,
                device=stridedInputs.device,
            ).requires_grad_()
        else:
            h0 = torch.zeros(
                self.layer_dim,
                stridedInputs.size(0),
                self.hidden_dim,
                device=stridedInputs.device,
            ).requires_grad_()

        hid, _ = self.gru_decoder(stridedInputs, h0.detach())
        seq_out = self.fc_decoder_out(hid)
        return seq_out


class _CausalConvBlock(nn.Module):
    def __init__(self, channels: int, kernel_size: int, dilation: int, dropout: float):
        super().__init__()
        self.pad = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(channels, channels, kernel_size, dilation=dilation)
        self.norm = nn.BatchNorm1d(channels)
        self.dropout = nn.Dropout(dropout)
        self.act = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        x = F.pad(x, (self.pad, 0))
        x = self.conv(x)
        x = self.norm(x)
        x = self.act(x)
        x = self.dropout(x)
        return x + residual


class CausalTCNDecoder(_BaseTemporalDecoder):
    def __init__(
        self,
        neural_dim,
        n_classes,
        hidden_dim,
        layer_dim,
        nDays=24,
        dropout=0,
        device="cuda",
        strideLen=4,
        kernelLen=14,
        gaussianSmoothWidth=0,
        bidirectional=False,
        input_proj_dim=None,
        use_day_embed=True,
        tcn_layers=4,
        tcn_kernel_size=3,
    ):
        super().__init__(
            neural_dim=neural_dim,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            device=device,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            bidirectional=bidirectional,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
        )
        in_dim = self.actual_neural_dim * self.kernelLen
        self.input_linear = nn.Linear(in_dim, hidden_dim)
        blocks = []
        for i in range(tcn_layers):
            blocks.append(
                _CausalConvBlock(
                    channels=hidden_dim,
                    kernel_size=tcn_kernel_size,
                    dilation=2 ** i,
                    dropout=dropout,
                )
            )
        self.tcn = nn.Sequential(*blocks)
        self.fc_decoder_out = nn.Linear(hidden_dim, n_classes + 1)

    def forward(self, neuralInput, dayIdx):
        x = self._frontend(neuralInput, dayIdx)
        x = self.input_linear(x)
        x = torch.permute(x, (0, 2, 1))
        x = self.tcn(x)
        x = torch.permute(x, (0, 2, 1))
        return self.fc_decoder_out(x)


class MiniTransformerDecoder(_BaseTemporalDecoder):
    def __init__(
        self,
        neural_dim,
        n_classes,
        hidden_dim,
        layer_dim,
        nDays=24,
        dropout=0,
        device="cuda",
        strideLen=4,
        kernelLen=14,
        gaussianSmoothWidth=0,
        bidirectional=False,
        input_proj_dim=None,
        use_day_embed=True,
        transformer_heads=4,
        transformer_layers=2,
        transformer_ff_mult=4,
    ):
        super().__init__(
            neural_dim=neural_dim,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            device=device,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            bidirectional=bidirectional,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
        )
        in_dim = self.actual_neural_dim * self.kernelLen
        self.input_linear = nn.Linear(in_dim, hidden_dim)
        ff_dim = max(hidden_dim, hidden_dim * transformer_ff_mult)
        enc_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=transformer_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True,
            norm_first=True,
            activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=transformer_layers)
        self.fc_decoder_out = nn.Linear(hidden_dim, n_classes + 1)

    def forward(self, neuralInput, dayIdx):
        x = self._frontend(neuralInput, dayIdx)
        x = self.input_linear(x)
        t = x.size(1)
        causal_mask = torch.triu(
            torch.ones((t, t), dtype=torch.bool, device=x.device), diagonal=1
        )
        x = self.encoder(x, mask=causal_mask)
        return self.fc_decoder_out(x)


def _build_scatter_buffers(
    *,
    selected_channel_indices: Sequence[int],
    channel_to_rc: Dict[int, Tuple[int, int]],
    h: int,
    w: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    mapped_feat_idx: List[int] = []
    mapped_cell_idx: List[int] = []
    unmapped_feat_idx: List[int] = []

    for feat_i, ch in enumerate(selected_channel_indices):
        rc = channel_to_rc.get(int(ch))
        if rc is None:
            unmapped_feat_idx.append(int(feat_i))
            continue
        r, c = rc
        if not (0 <= int(r) < h and 0 <= int(c) < w):
            unmapped_feat_idx.append(int(feat_i))
            continue
        mapped_feat_idx.append(int(feat_i))
        mapped_cell_idx.append(int(r) * w + int(c))

    counts = [0] * (h * w)
    for cell in mapped_cell_idx:
        counts[int(cell)] += 1

    mapped_feat_t = torch.tensor(mapped_feat_idx, dtype=torch.long)
    mapped_cell_t = torch.tensor(mapped_cell_idx, dtype=torch.long)
    unmapped_feat_t = torch.tensor(unmapped_feat_idx, dtype=torch.long)
    cell_counts_t = torch.tensor(counts, dtype=torch.float32)  # (h*w,)
    mask_grid_t = (cell_counts_t > 0).to(torch.float32).view(h, w)
    return mapped_feat_t, mapped_cell_t, unmapped_feat_t, cell_counts_t, mask_grid_t


class _SpatialTemporalDecoderBase(nn.Module):
    def __init__(
        self,
        *,
        embed_dim: int,
        n_classes: int,
        hidden_dim: int,
        layer_dim: int,
        nDays: int,
        dropout: float,
        strideLen: int,
        kernelLen: int,
        gaussianSmoothWidth: float,
        use_day_embed: bool,
    ):
        super().__init__()
        self.embed_dim = int(embed_dim)
        self.n_classes = int(n_classes)
        self.hidden_dim = int(hidden_dim)
        self.layer_dim = int(layer_dim)
        self.nDays = int(nDays)
        self.dropout = float(dropout)
        self.strideLen = int(strideLen)
        self.kernelLen = int(kernelLen)
        self.gaussianSmoothWidth = float(gaussianSmoothWidth)
        self.use_day_embed = bool(use_day_embed)

        self.inputLayerNonlinearity = torch.nn.Softsign()

        self.unfolder = torch.nn.Unfold(
            (self.kernelLen, 1), dilation=1, padding=0, stride=self.strideLen
        )
        if self.gaussianSmoothWidth > 0:
            self.gaussianSmoother = GaussianSmoothing(
                self.embed_dim, 20, self.gaussianSmoothWidth, dim=1
            )
        else:
            self.gaussianSmoother = nn.Identity()

        if self.use_day_embed:
            self.dayWeights = torch.nn.Parameter(
                torch.randn(nDays, self.embed_dim, self.embed_dim)
            )
            self.dayBias = torch.nn.Parameter(torch.zeros(nDays, 1, self.embed_dim))
            for x in range(nDays):
                self.dayWeights.data[x, :, :] = torch.eye(self.embed_dim)
        else:
            self.dayWeights = None
            self.dayBias = None

        self.gru_decoder = nn.GRU(
            self.embed_dim * self.kernelLen,
            self.hidden_dim,
            self.layer_dim,
            batch_first=True,
            dropout=self.dropout,
            bidirectional=False,
        )

        for name, param in self.gru_decoder.named_parameters():
            if "weight_hh" in name:
                nn.init.orthogonal_(param)
            if "weight_ih" in name:
                nn.init.xavier_uniform_(param)

        self.fc_decoder_out = nn.Linear(self.hidden_dim, self.n_classes + 1)  # +1 for CTC blank

    def _frame_embeddings(self, neuralInput: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

    def forward(self, neuralInput: torch.Tensor, dayIdx: torch.Tensor) -> torch.Tensor:
        # neuralInput: (B, T, K) -> embeddings: (B, T, D)
        emb = self._frame_embeddings(neuralInput)
        emb = torch.permute(emb, (0, 2, 1))
        emb = self.gaussianSmoother(emb)
        emb = torch.permute(emb, (0, 2, 1))

        if self.use_day_embed and self.dayWeights is not None:
            dayWeights = torch.index_select(self.dayWeights, 0, dayIdx)
            transformed = torch.einsum("btd,bdk->btk", emb, dayWeights) + torch.index_select(
                self.dayBias, 0, dayIdx
            )
            transformed = self.inputLayerNonlinearity(transformed)
        else:
            transformed = self.inputLayerNonlinearity(emb)

        if transformed.shape[1] < self.kernelLen:
            pad_t = self.kernelLen - transformed.shape[1]
            transformed = F.pad(transformed, (0, 0, 0, pad_t))

        strided = torch.permute(
            self.unfolder(torch.unsqueeze(torch.permute(transformed, (0, 2, 1)), 3)),
            (0, 2, 1),
        )

        h0 = torch.zeros(
            self.layer_dim,
            strided.size(0),
            self.hidden_dim,
            device=strided.device,
        ).requires_grad_()
        hid, _ = self.gru_decoder(strided, h0.detach())
        return self.fc_decoder_out(hid)


class Spatial2DUniGRUDecoder(_SpatialTemporalDecoderBase):
    def __init__(
        self,
        *,
        neural_dim: int,
        selected_channel_indices: Optional[Sequence[int]],
        n_classes: int,
        hidden_dim: int,
        layer_dim: int,
        nDays: int,
        dropout: float,
        strideLen: int,
        kernelLen: int,
        gaussianSmoothWidth: float,
        input_proj_dim: Optional[int],
        use_day_embed: bool,
        enable_spatial_aug: bool,
        grid_h: int = 16,
        grid_w: int = 16,
    ):
        if input_proj_dim is None:
            raise ValueError("spatial2d_uni_gru requires input_proj_dim (frame embedding dim)")
        self.grid_h = int(grid_h)
        self.grid_w = int(grid_w)
        self.neural_dim = int(neural_dim)
        self.enable_spatial_aug = bool(enable_spatial_aug)

        if selected_channel_indices is None:
            selected_channel_indices = list(range(self.neural_dim))
        if len(selected_channel_indices) != self.neural_dim:
            raise ValueError(
                f"selected_channel_indices length mismatch: got {len(selected_channel_indices)} vs neural_dim={self.neural_dim}"
            )

        channel_to_rc = load_smartpalate_map()
        mapped_feat_t, mapped_cell_t, unmapped_feat_t, cell_counts_t, mask_grid_t = _build_scatter_buffers(
            selected_channel_indices=selected_channel_indices,
            channel_to_rc=channel_to_rc,
            h=self.grid_h,
            w=self.grid_w,
        )

        super().__init__(
            embed_dim=int(input_proj_dim),
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            use_day_embed=use_day_embed,
        )

        self.register_buffer("_mapped_feat_idx", mapped_feat_t)
        self.register_buffer("_mapped_cell_idx", mapped_cell_t)
        self.register_buffer("_unmapped_feat_idx", unmapped_feat_t)
        self.register_buffer("_cell_counts", cell_counts_t)
        self.register_buffer("_mask_grid", mask_grid_t)  # (H,W)

        self.conv = nn.Sequential(
            nn.Conv2d(2, 16, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Conv2d(32, self.embed_dim, kernel_size=3, padding=1),
            nn.GELU(),
        )
        self.pool = nn.AdaptiveAvgPool2d((1, 1))

        n_unmapped = int(self._unmapped_feat_idx.numel())
        self.unmapped_linear = nn.Linear(n_unmapped, self.embed_dim) if n_unmapped > 0 else None

    def _apply_spatial_aug(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, T, 2, H, W). Augment per-sample (constant over time).
        B, T, C, H, W = x.shape
        out = x.clone()

        p_block = 0.4
        block_sizes = (2, 3, 4)
        p_shift = 0.5

        for b in range(B):
            if torch.rand((), device=out.device).item() < p_block:
                size = int(block_sizes[int(torch.randint(0, len(block_sizes), (1,), device=out.device).item())])
                top = int(torch.randint(0, max(1, H - size + 1), (1,), device=out.device).item())
                left = int(torch.randint(0, max(1, W - size + 1), (1,), device=out.device).item())
                out[b, :, :, top : top + size, left : left + size] = 0

            if torch.rand((), device=out.device).item() < p_shift:
                dx = int(torch.randint(-1, 2, (1,), device=out.device).item())
                dy = int(torch.randint(-1, 2, (1,), device=out.device).item())
                if dx != 0 or dy != 0:
                    src = out[b].clone()  # (T,2,H,W)
                    out[b] = 0
                    src_y0 = max(0, -dy)
                    src_y1 = min(H, H - dy)
                    dst_y0 = max(0, dy)
                    dst_y1 = min(H, H + dy)
                    src_x0 = max(0, -dx)
                    src_x1 = min(W, W - dx)
                    dst_x0 = max(0, dx)
                    dst_x1 = min(W, W + dx)
                    out[b, :, :, dst_y0:dst_y1, dst_x0:dst_x1] = src[:, :, src_y0:src_y1, src_x0:src_x1]

        return out

    def _frame_embeddings(self, neuralInput: torch.Tensor) -> torch.Tensor:
        B, T, K = neuralInput.shape
        if K != self.neural_dim:
            raise ValueError(f"Input feature dim mismatch: got K={K} vs expected neural_dim={self.neural_dim}")

        x_flat = neuralInput.reshape(B * T, K)
        grid_flat = x_flat.new_zeros((B * T, self.grid_h * self.grid_w))

        if self._mapped_feat_idx.numel() > 0:
            vals = x_flat.index_select(1, self._mapped_feat_idx)  # (B*T, M)
            idx = self._mapped_cell_idx.view(1, -1).expand(B * T, -1)
            grid_flat.scatter_add_(1, idx, vals)
            counts = torch.clamp(self._cell_counts, min=1.0).view(1, -1)
            grid_flat = grid_flat / counts

        value = grid_flat.view(B, T, self.grid_h, self.grid_w)
        mask = self._mask_grid.view(1, 1, self.grid_h, self.grid_w).expand(B, T, self.grid_h, self.grid_w)
        stacked = torch.stack([value, mask], dim=2)  # (B,T,2,H,W)

        if self.enable_spatial_aug and self.training:
            stacked = self._apply_spatial_aug(stacked)

        x2 = stacked.reshape(B * T, 2, self.grid_h, self.grid_w)
        y = self.conv(x2)
        y = self.pool(y).flatten(1)  # (B*T, D)

        if self.unmapped_linear is not None and self._unmapped_feat_idx.numel() > 0:
            unmapped = x_flat.index_select(1, self._unmapped_feat_idx)
            y = y + self.unmapped_linear(unmapped)

        return y.view(B, T, self.embed_dim)


class Spatial2DPatchPoolUniGRUDecoder(_SpatialTemporalDecoderBase):
    """Spatial2D front end that preserves coarse 2D structure via patch pooling.

    Differences vs Spatial2DUniGRUDecoder:
    - Pool to (4,4) instead of (1,1).
    - Project flattened patches back to embed_dim with Linear + LayerNorm.
    """

    def __init__(
        self,
        *,
        neural_dim: int,
        selected_channel_indices: Optional[Sequence[int]],
        n_classes: int,
        hidden_dim: int,
        layer_dim: int,
        nDays: int,
        dropout: float,
        strideLen: int,
        kernelLen: int,
        gaussianSmoothWidth: float,
        input_proj_dim: Optional[int],
        use_day_embed: bool,
        enable_spatial_aug: bool,
        grid_h: int = 16,
        grid_w: int = 16,
        pool_h: int = 4,
        pool_w: int = 4,
    ):
        if input_proj_dim is None:
            raise ValueError("spatial2d_patchpool_uni_gru requires input_proj_dim (frame embedding dim)")
        self.grid_h = int(grid_h)
        self.grid_w = int(grid_w)
        self.pool_h = int(pool_h)
        self.pool_w = int(pool_w)
        self.neural_dim = int(neural_dim)
        self.enable_spatial_aug = bool(enable_spatial_aug)

        if selected_channel_indices is None:
            selected_channel_indices = list(range(self.neural_dim))
        if len(selected_channel_indices) != self.neural_dim:
            raise ValueError(
                f"selected_channel_indices length mismatch: got {len(selected_channel_indices)} vs neural_dim={self.neural_dim}"
            )

        channel_to_rc = load_smartpalate_map()
        mapped_feat_t, mapped_cell_t, unmapped_feat_t, cell_counts_t, mask_grid_t = _build_scatter_buffers(
            selected_channel_indices=selected_channel_indices,
            channel_to_rc=channel_to_rc,
            h=self.grid_h,
            w=self.grid_w,
        )

        super().__init__(
            embed_dim=int(input_proj_dim),
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            use_day_embed=use_day_embed,
        )

        self.register_buffer("_mapped_feat_idx", mapped_feat_t)
        self.register_buffer("_mapped_cell_idx", mapped_cell_t)
        self.register_buffer("_unmapped_feat_idx", unmapped_feat_t)
        self.register_buffer("_cell_counts", cell_counts_t)
        self.register_buffer("_mask_grid", mask_grid_t)  # (H,W)

        self.conv = nn.Sequential(
            nn.Conv2d(2, 16, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Conv2d(32, self.embed_dim, kernel_size=3, padding=1),
            nn.GELU(),
        )
        self.pool = nn.AdaptiveAvgPool2d((self.pool_h, self.pool_w))
        self.patch_proj = nn.Linear(self.embed_dim * self.pool_h * self.pool_w, self.embed_dim)
        self.patch_ln = nn.LayerNorm(self.embed_dim)

        n_unmapped = int(self._unmapped_feat_idx.numel())
        self.unmapped_linear = nn.Linear(n_unmapped, self.embed_dim) if n_unmapped > 0 else None

    def _apply_spatial_aug(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, T, 2, H, W). Augment per-sample (constant over time).
        B, T, C, H, W = x.shape
        out = x.clone()

        p_block = 0.4
        block_sizes = (2, 3, 4)
        p_shift = 0.5

        for b in range(B):
            if torch.rand((), device=out.device).item() < p_block:
                size = int(block_sizes[int(torch.randint(0, len(block_sizes), (1,), device=out.device).item())])
                top = int(torch.randint(0, max(1, H - size + 1), (1,), device=out.device).item())
                left = int(torch.randint(0, max(1, W - size + 1), (1,), device=out.device).item())
                out[b, :, :, top : top + size, left : left + size] = 0

            if torch.rand((), device=out.device).item() < p_shift:
                dx = int(torch.randint(-1, 2, (1,), device=out.device).item())
                dy = int(torch.randint(-1, 2, (1,), device=out.device).item())
                if dx != 0 or dy != 0:
                    src = out[b].clone()  # (T,2,H,W)
                    out[b] = 0
                    src_y0 = max(0, -dy)
                    src_y1 = min(H, H - dy)
                    dst_y0 = max(0, dy)
                    dst_y1 = min(H, H + dy)
                    src_x0 = max(0, -dx)
                    src_x1 = min(W, W - dx)
                    dst_x0 = max(0, dx)
                    dst_x1 = min(W, W + dx)
                    out[b, :, :, dst_y0:dst_y1, dst_x0:dst_x1] = src[:, :, src_y0:src_y1, src_x0:src_x1]

        return out

    def _frame_embeddings(self, neuralInput: torch.Tensor) -> torch.Tensor:
        B, T, K = neuralInput.shape
        if K != self.neural_dim:
            raise ValueError(f"Input feature dim mismatch: got K={K} vs expected neural_dim={self.neural_dim}")

        x_flat = neuralInput.reshape(B * T, K)
        grid_flat = x_flat.new_zeros((B * T, self.grid_h * self.grid_w))

        if self._mapped_feat_idx.numel() > 0:
            vals = x_flat.index_select(1, self._mapped_feat_idx)  # (B*T, M)
            idx = self._mapped_cell_idx.view(1, -1).expand(B * T, -1)
            grid_flat.scatter_add_(1, idx, vals)
            counts = torch.clamp(self._cell_counts, min=1.0).view(1, -1)
            grid_flat = grid_flat / counts

        value = grid_flat.view(B, T, self.grid_h, self.grid_w)
        mask = self._mask_grid.view(1, 1, self.grid_h, self.grid_w).expand(B, T, self.grid_h, self.grid_w)
        stacked = torch.stack([value, mask], dim=2)  # (B,T,2,H,W)

        if self.enable_spatial_aug and self.training:
            stacked = self._apply_spatial_aug(stacked)

        x2 = stacked.reshape(B * T, 2, self.grid_h, self.grid_w)
        y = self.conv(x2)
        y = self.pool(y).flatten(1)  # (B*T, D*pool_h*pool_w)
        y = self.patch_ln(self.patch_proj(y))  # (B*T, D)

        if self.unmapped_linear is not None and self._unmapped_feat_idx.numel() > 0:
            unmapped = x_flat.index_select(1, self._unmapped_feat_idx)
            y = y + self.unmapped_linear(unmapped)

        return y.view(B, T, self.embed_dim)


class RowColUniGRUDecoder(_SpatialTemporalDecoderBase):
    def __init__(
        self,
        *,
        neural_dim: int,
        selected_channel_indices: Optional[Sequence[int]],
        n_classes: int,
        hidden_dim: int,
        layer_dim: int,
        nDays: int,
        dropout: float,
        strideLen: int,
        kernelLen: int,
        gaussianSmoothWidth: float,
        input_proj_dim: Optional[int],
        use_day_embed: bool,
        grid_h: int = 16,
        grid_w: int = 16,
    ):
        if input_proj_dim is None:
            raise ValueError("rowcol_uni_gru requires input_proj_dim (frame embedding dim)")
        self.grid_h = int(grid_h)
        self.grid_w = int(grid_w)
        self.neural_dim = int(neural_dim)

        if selected_channel_indices is None:
            selected_channel_indices = list(range(self.neural_dim))
        if len(selected_channel_indices) != self.neural_dim:
            raise ValueError(
                f"selected_channel_indices length mismatch: got {len(selected_channel_indices)} vs neural_dim={self.neural_dim}"
            )

        channel_to_rc = load_smartpalate_map()
        mapped_feat_t, mapped_cell_t, unmapped_feat_t, cell_counts_t, mask_grid_t = _build_scatter_buffers(
            selected_channel_indices=selected_channel_indices,
            channel_to_rc=channel_to_rc,
            h=self.grid_h,
            w=self.grid_w,
        )

        super().__init__(
            embed_dim=int(input_proj_dim),
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            use_day_embed=use_day_embed,
        )

        self.register_buffer("_mapped_feat_idx", mapped_feat_t)
        self.register_buffer("_mapped_cell_idx", mapped_cell_t)
        self.register_buffer("_unmapped_feat_idx", unmapped_feat_t)
        self.register_buffer("_cell_counts", cell_counts_t)
        self.register_buffer("_mask_grid", mask_grid_t)  # (H,W)

        in_dim = self.grid_h + self.grid_w + int(self._unmapped_feat_idx.numel())
        self.in_linear = nn.Linear(in_dim, self.embed_dim)

    def _frame_embeddings(self, neuralInput: torch.Tensor) -> torch.Tensor:
        B, T, K = neuralInput.shape
        if K != self.neural_dim:
            raise ValueError(f"Input feature dim mismatch: got K={K} vs expected neural_dim={self.neural_dim}")

        x_flat = neuralInput.reshape(B * T, K)
        grid_flat = x_flat.new_zeros((B * T, self.grid_h * self.grid_w))

        if self._mapped_feat_idx.numel() > 0:
            vals = x_flat.index_select(1, self._mapped_feat_idx)  # (B*T, M)
            idx = self._mapped_cell_idx.view(1, -1).expand(B * T, -1)
            grid_flat.scatter_add_(1, idx, vals)
            counts = torch.clamp(self._cell_counts, min=1.0).view(1, -1)
            grid_flat = grid_flat / counts

        value = grid_flat.view(B, T, self.grid_h, self.grid_w)
        mask = self._mask_grid.view(1, 1, self.grid_h, self.grid_w).expand(B, T, self.grid_h, self.grid_w)

        row_sum = (value * mask).sum(dim=-1)  # (B,T,H)
        row_cnt = mask.sum(dim=-1).clamp(min=1.0)
        row_mean = row_sum / row_cnt

        col_sum = (value * mask).sum(dim=-2)  # (B,T,W)
        col_cnt = mask.sum(dim=-2).clamp(min=1.0)
        col_mean = col_sum / col_cnt

        feat = torch.cat([row_mean, col_mean], dim=-1)  # (B,T,H+W)
        if self._unmapped_feat_idx.numel() > 0:
            unmapped = neuralInput.index_select(2, self._unmapped_feat_idx)  # (B,T,Nu)
            feat = torch.cat([feat, unmapped], dim=-1)

        return self.in_linear(feat)


def build_model(
    model_family: str,
    *,
    neural_dim: int,
    n_classes: int,
    hidden_dim: int,
    layer_dim: int,
    nDays: int,
    dropout: float,
    device,
    strideLen: int,
    kernelLen: int,
    gaussianSmoothWidth: float,
    bidirectional: bool,
    input_proj_dim,
    use_day_embed: bool,
    tcn_layers: int = 4,
    tcn_kernel_size: int = 3,
    transformer_heads: int = 4,
    transformer_layers: int = 2,
    transformer_ff_mult: int = 4,
    selected_channel_indices: Optional[Sequence[int]] = None,
    enable_spatial_aug: bool = False,
):
    fam = (model_family or "gru").strip().lower()
    if fam == "gru":
        return GRUDecoder(
            neural_dim=neural_dim,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            device=device,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            bidirectional=bidirectional,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
        )
    if fam == "uni_gru":
        return GRUDecoder(
            neural_dim=neural_dim,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            device=device,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            bidirectional=False,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
        )
    if fam == "causal_tcn":
        return CausalTCNDecoder(
            neural_dim=neural_dim,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            device=device,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            bidirectional=False,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
            tcn_layers=tcn_layers,
            tcn_kernel_size=tcn_kernel_size,
        )
    if fam == "mini_transformer":
        return MiniTransformerDecoder(
            neural_dim=neural_dim,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            device=device,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            bidirectional=False,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
            transformer_heads=transformer_heads,
            transformer_layers=transformer_layers,
            transformer_ff_mult=transformer_ff_mult,
        )
    if fam == "spatial2d_uni_gru":
        return Spatial2DUniGRUDecoder(
            neural_dim=neural_dim,
            selected_channel_indices=selected_channel_indices,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
            enable_spatial_aug=enable_spatial_aug,
        )
    if fam == "spatial2d_patchpool_uni_gru":
        return Spatial2DPatchPoolUniGRUDecoder(
            neural_dim=neural_dim,
            selected_channel_indices=selected_channel_indices,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
            enable_spatial_aug=enable_spatial_aug,
        )
    if fam == "rowcol_uni_gru":
        return RowColUniGRUDecoder(
            neural_dim=neural_dim,
            selected_channel_indices=selected_channel_indices,
            n_classes=n_classes,
            hidden_dim=hidden_dim,
            layer_dim=layer_dim,
            nDays=nDays,
            dropout=dropout,
            strideLen=strideLen,
            kernelLen=kernelLen,
            gaussianSmoothWidth=gaussianSmoothWidth,
            input_proj_dim=input_proj_dim,
            use_day_embed=use_day_embed,
        )
    raise ValueError(f"Unsupported model_family: {model_family}")
