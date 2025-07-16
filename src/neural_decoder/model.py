import torch
from torch import nn

from .augmentations import GaussianSmoothing


class GRUDecoder(nn.Module):
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
        super(GRUDecoder, self).__init__()

        # Defining the number of layers and the nodes in each layer
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
        
        # Input projection layer (16 -> 256 for compatibility)
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
        self.gaussianSmoother = GaussianSmoothing(
            self.actual_neural_dim, 20, self.gaussianSmoothWidth, dim=1
        )
        
        # Day embedding (optional for unified dataset)
        if self.use_day_embed:
            self.dayWeights = torch.nn.Parameter(torch.randn(nDays, self.actual_neural_dim, self.actual_neural_dim))
            self.dayBias = torch.nn.Parameter(torch.zeros(nDays, 1, self.actual_neural_dim))

            for x in range(nDays):
                self.dayWeights.data[x, :, :] = torch.eye(self.actual_neural_dim)
        else:
            self.dayWeights = None
            self.dayBias = None

        # GRU layers
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

        # Input layers (only if using day embedding)
        if self.use_day_embed:
            for x in range(nDays):
                setattr(self, "inpLayer" + str(x), nn.Linear(self.actual_neural_dim, self.actual_neural_dim))

            for x in range(nDays):
                thisLayer = getattr(self, "inpLayer" + str(x))
                thisLayer.weight = torch.nn.Parameter(
                    thisLayer.weight + torch.eye(self.actual_neural_dim)
                )

        # rnn outputs
        if self.bidirectional:
            self.fc_decoder_out = nn.Linear(
                hidden_dim * 2, n_classes + 1
            )  # +1 for CTC blank
        else:
            self.fc_decoder_out = nn.Linear(hidden_dim, n_classes + 1)  # +1 for CTC blank

    def forward(self, neuralInput, dayIdx):
        # Apply input projection if needed (16 -> 256)
        if self.input_proj is not None:
            neuralInput = self.input_proj(neuralInput)
            
        neuralInput = torch.permute(neuralInput, (0, 2, 1))
        neuralInput = self.gaussianSmoother(neuralInput)
        neuralInput = torch.permute(neuralInput, (0, 2, 1))

        # Apply day layer (if enabled)
        if self.use_day_embed and self.dayWeights is not None:
            dayWeights = torch.index_select(self.dayWeights, 0, dayIdx)
            transformedNeural = torch.einsum(
                "btd,bdk->btk", neuralInput, dayWeights
            ) + torch.index_select(self.dayBias, 0, dayIdx)
            transformedNeural = self.inputLayerNonlinearity(transformedNeural)
        else:
            # Skip day embedding for unified dataset
            transformedNeural = self.inputLayerNonlinearity(neuralInput)

        # stride/kernel
        stridedInputs = torch.permute(
            self.unfolder(
                torch.unsqueeze(torch.permute(transformedNeural, (0, 2, 1)), 3)
            ),
            (0, 2, 1),
        )

        # apply RNN layer
        if self.bidirectional:
            h0 = torch.zeros(
                self.layer_dim * 2,
                transformedNeural.size(0),
                self.hidden_dim,
                device=transformedNeural.device,
            ).requires_grad_()
        else:
            h0 = torch.zeros(
                self.layer_dim,
                transformedNeural.size(0),
                self.hidden_dim,
                device=transformedNeural.device,
            ).requires_grad_()

        hid, _ = self.gru_decoder(stridedInputs, h0.detach())

        # get seq
        seq_out = self.fc_decoder_out(hid)
        return seq_out
