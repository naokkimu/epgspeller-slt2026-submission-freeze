import os
import pickle
import time

from edit_distance import SequenceMatcher
import hydra
import numpy as np
import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader

from .model import build_model
from .dataset import SpeechDataset


def getUnifiedDatasetLoaders(cfg):
    """New unified dataset loader for npz-based data."""
    from .unified_dataset import UnifiedEPGDataset
    
    def _padding(batch):
        X, y = zip(*batch)
        X_padded = pad_sequence(X, batch_first=True, padding_value=0)
        
        # y is now sequence of character IDs
        y_padded = pad_sequence(y, batch_first=True, padding_value=27)  # SIL padding
        
        # Calculate actual lengths
        X_lens = torch.tensor([x.size(0) for x in X], dtype=torch.int32)
        y_lens = torch.tensor([len(seq) for seq in y], dtype=torch.int32)
        days = torch.zeros(len(X), dtype=torch.int64)  # No day info for unified
        
        return X_padded, y_padded, X_lens, y_lens, days
    
    train_ds = UnifiedEPGDataset("train", cfg)
    test_ds = UnifiedEPGDataset("test", cfg)
    
    # Handle both OmegaConf and dict access
    batch_size = cfg.batchSize if hasattr(cfg, 'batchSize') else cfg.get('batchSize', 64)
    
    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
        pin_memory=True,
        collate_fn=_padding,
    )
    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=True,
        collate_fn=_padding,
    )
    
    # Return dummy loadedData for compatibility
    dummy_data = {"train": [], "test": []}
    return train_loader, test_loader, dummy_data


def getDatasetLoaders(
    datasetName,
    batchSize,
    aug_conf=None,
    val_split="test",
):
    with open(datasetName, "rb") as handle:
        loadedData = pickle.load(handle)
    
    if val_split not in ["test", "competition"]:
        raise ValueError(f"val_split must be 'test' or 'competition', got {val_split}")

    def _padding(batch):
        X, y, X_lens, y_lens, days = zip(*batch)
        X_padded = pad_sequence(X, batch_first=True, padding_value=0)
        y_padded = pad_sequence(y, batch_first=True, padding_value=0)

        return (
            X_padded,
            y_padded,
            torch.stack(X_lens),
            torch.stack(y_lens),
            torch.stack(days),
        )

    train_ds = SpeechDataset(loadedData["train"], transform=None, aug_conf=aug_conf)
    val_ds = SpeechDataset(loadedData[val_split])

    train_loader = DataLoader(
        train_ds,
        batch_size=batchSize,
        shuffle=True,
        num_workers=0,
        pin_memory=True,
        collate_fn=_padding,
    )
    test_loader = DataLoader(
        val_ds,
        batch_size=batchSize,
        shuffle=False,
        num_workers=0,
        pin_memory=True,
        collate_fn=_padding,
    )
    
    return train_loader, test_loader, loadedData

def trainModel(args):
    os.makedirs(args["outputDir"], exist_ok=True)
    torch.manual_seed(args["seed"])
    np.random.seed(args["seed"])
    
    # Device selection: CUDA -> MPS -> CPU
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("Using CUDA device")
    elif torch.backends.mps.is_available():
        device = torch.device("cpu")  # Fallback to CPU due to CTC loss not supported on MPS
        print("MPS available but using CPU due to CTC loss compatibility")
    else:
        device = torch.device("cpu")
        print("Using CPU device")

    with open(args["outputDir"] + "/args", "wb") as file:
        pickle.dump(args, file)

    # Dataset selection: unified vs legacy
    if args.get("dataset_cls", "legacy") == "unified":
        print("Using unified dataset pipeline")
        trainLoader, testLoader, loadedData = getUnifiedDatasetLoaders(args)
    else:
        print("Using legacy dataset pipeline")
        trainLoader, testLoader, loadedData = getDatasetLoaders(
            args["datasetPath"],
            args["batchSize"],
            aug_conf=args.get("aug_conf", None),
            val_split=args.get("val_split", "test"),
        )

    # Handle both unified and legacy model configuration
    model_cfg = args.get("model", {})
    use_day_embed = model_cfg.get("use_day_embed", True)
    input_proj_dim = model_cfg.get("input_proj_dim", None)
    model_family = model_cfg.get("model_family", "gru")
    selected_channel_indices = model_cfg.get("selected_channel_indices", None)
    enable_spatial_aug = bool(model_cfg.get("enable_spatial_aug", False))
    tcn_layers = int(model_cfg.get("tcn_layers", 4))
    tcn_kernel_size = int(model_cfg.get("tcn_kernel_size", 3))
    transformer_heads = int(model_cfg.get("transformer_heads", 4))
    transformer_layers = int(model_cfg.get("transformer_layers", 2))
    transformer_ff_mult = int(model_cfg.get("transformer_ff_mult", 4))
    
    # For unified dataset, use dummy nDays=1 when day embedding is disabled
    nDays = 1 if not use_day_embed else len(loadedData["train"])
    
    model = build_model(
        model_family,
        neural_dim=args["nInputFeatures"],
        n_classes=args["nClasses"],
        hidden_dim=args["nUnits"],
        layer_dim=args["nLayers"],
        nDays=nDays,
        dropout=args["dropout"],
        device=device,
        strideLen=args["strideLen"],
        kernelLen=args["kernelLen"],
        gaussianSmoothWidth=args["gaussianSmoothWidth"],
        bidirectional=args["bidirectional"],
        input_proj_dim=input_proj_dim,
        use_day_embed=use_day_embed,
        tcn_layers=tcn_layers,
        tcn_kernel_size=tcn_kernel_size,
        transformer_heads=transformer_heads,
        transformer_layers=transformer_layers,
        transformer_ff_mult=transformer_ff_mult,
        selected_channel_indices=selected_channel_indices,
        enable_spatial_aug=enable_spatial_aug,
    ).to(device)

    loss_ctc = torch.nn.CTCLoss(blank=0, reduction="mean", zero_infinity=True)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=args["lrStart"],
        betas=(0.9, 0.999),
        eps=0.1,
        weight_decay=args["l2_decay"],
    )
    scheduler = torch.optim.lr_scheduler.LinearLR(
        optimizer,
        start_factor=1.0,
        end_factor=args["lrEnd"] / args["lrStart"],
        total_iters=args["nBatch"],
    )

    # --train--
    testLoss = []
    testCER = []
    startTime = time.time()
    best_cer = float('inf')
    for batch in range(args["nBatch"]):
        model.train()

        X, y, X_len, y_len, dayIdx = next(iter(trainLoader))
        X, y, X_len, y_len, dayIdx = (
            X.to(device),
            y.to(device),
            X_len.to(device),
            y_len.to(device),
            dayIdx.to(device),
        )

        # Noise augmentation is faster on GPU
        if args["whiteNoiseSD"] > 0:
            X += torch.randn(X.shape, device=device) * args["whiteNoiseSD"]

        if args["constantOffsetSD"] > 0:
            X += (
                torch.randn([X.shape[0], 1, X.shape[2]], device=device)
                * args["constantOffsetSD"]
            )

        # Compute prediction error
        pred = model.forward(X, dayIdx)

        ctc_input_lens = ((X_len - model.kernelLen) / model.strideLen).to(torch.int32)
        ctc_input_lens = torch.clamp(ctc_input_lens, min=1)

        loss = loss_ctc(
            torch.permute(pred.log_softmax(2), [1, 0, 2]),
            y,
            ctc_input_lens,
            y_len,
        )
        loss = torch.sum(loss)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()

        # print(endTime - startTime)

        # Eval
        if batch % 100 == 0:
            with torch.no_grad():
                model.eval()
                allLoss = []
                total_edit_distance = 0
                total_seq_length = 0
                for X, y, X_len, y_len, testDayIdx in testLoader:
                    X, y, X_len, y_len, testDayIdx = (
                        X.to(device),
                        y.to(device),
                        X_len.to(device),
                        y_len.to(device),
                        testDayIdx.to(device),
                    )

                    pred = model.forward(X, testDayIdx)
                    ctc_input_lens = ((X_len - model.kernelLen) / model.strideLen).to(torch.int32)
                    ctc_input_lens = torch.clamp(ctc_input_lens, min=1)

                    loss = loss_ctc(
                        torch.permute(pred.log_softmax(2), [1, 0, 2]),
                        y,
                        ctc_input_lens,
                        y_len,
                    )
                    loss = torch.sum(loss)
                    allLoss.append(loss.cpu().detach().numpy())

                    adjustedLens = ctc_input_lens
                    for iterIdx in range(pred.shape[0]):
                        decodedSeq = torch.argmax(
                            torch.tensor(pred[iterIdx, 0 : adjustedLens[iterIdx], :]),
                            dim=-1,
                        )  # [num_seq,]
                        decodedSeq = torch.unique_consecutive(decodedSeq, dim=-1)
                        decodedSeq = decodedSeq.cpu().detach().numpy()
                        decodedSeq = np.array([i for i in decodedSeq if i != 0])

                        trueSeq = np.array(
                            y[iterIdx][0 : y_len[iterIdx]].cpu().detach()
                        )

                        matcher = SequenceMatcher(
                            a=trueSeq.tolist(), b=decodedSeq.tolist()
                        )
                        total_edit_distance += matcher.distance()
                        total_seq_length += len(trueSeq)

                avgDayLoss = np.sum(allLoss) / len(testLoader)
                cer = total_edit_distance / total_seq_length

                endTime = time.time()
                print(
                    f"batch {batch}, val ctc loss: {avgDayLoss:>7f}, val cer: {cer:>7f}, time/batch: {(endTime - startTime)/100:>7.3f}"
                )
                startTime = time.time()

            if cer < best_cer:
                torch.save(model.state_dict(), args["outputDir"] + "/modelWeights")
                best_cer = cer
            testLoss.append(avgDayLoss)
            testCER.append(cer)

            tStats = {}
            tStats["testLoss"] = np.array(testLoss)
            tStats["testCER"] = np.array(testCER)

            with open(args["outputDir"] + "/trainingStats", "wb") as file:
                pickle.dump(tStats, file)

    # Return the final metrics
    return {
        'validation_loss': testLoss[-1] if testLoss else float('inf'),
        'validation_cer': testCER[-1] if testCER else float('inf'),
        'best_validation_cer': best_cer
    }


def loadModel(modelDir, nInputLayers=24, device=None):
    if device is None:
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("cpu")  # Fallback to CPU due to CTC loss compatibility
        else:
            device = torch.device("cpu")
            
    modelWeightPath = modelDir + "/modelWeights"
    with open(modelDir + "/args", "rb") as handle:
        args = pickle.load(handle)

    model_cfg = args.get("model", {})
    if not isinstance(model_cfg, dict):
        model_cfg = {}
    use_day_embed = bool(model_cfg.get("use_day_embed", True))
    input_proj_dim = model_cfg.get("input_proj_dim", None)
    model_family = model_cfg.get("model_family", "gru")
    selected_channel_indices = model_cfg.get("selected_channel_indices", None)
    enable_spatial_aug = bool(model_cfg.get("enable_spatial_aug", False))
    tcn_layers = int(model_cfg.get("tcn_layers", 4))
    tcn_kernel_size = int(model_cfg.get("tcn_kernel_size", 3))
    transformer_heads = int(model_cfg.get("transformer_heads", 4))
    transformer_layers = int(model_cfg.get("transformer_layers", 2))
    transformer_ff_mult = int(model_cfg.get("transformer_ff_mult", 4))
    effective_n_input_layers = nInputLayers if use_day_embed else 1

    model = build_model(
        model_family,
        neural_dim=args["nInputFeatures"],
        n_classes=args["nClasses"],
        hidden_dim=args["nUnits"],
        layer_dim=args["nLayers"],
        nDays=effective_n_input_layers,
        dropout=args["dropout"],
        device=device,
        strideLen=args["strideLen"],
        kernelLen=args["kernelLen"],
        gaussianSmoothWidth=args["gaussianSmoothWidth"],
        bidirectional=args["bidirectional"],
        input_proj_dim=input_proj_dim,
        use_day_embed=use_day_embed,
        tcn_layers=tcn_layers,
        tcn_kernel_size=tcn_kernel_size,
        transformer_heads=transformer_heads,
        transformer_layers=transformer_layers,
        transformer_ff_mult=transformer_ff_mult,
        selected_channel_indices=selected_channel_indices,
        enable_spatial_aug=enable_spatial_aug,
    ).to(device)

    model.load_state_dict(torch.load(modelWeightPath, map_location=device))
    return model


@hydra.main(config_path="conf", config_name="config")
def main(cfg):
    cfg.outputDir = os.getcwd()
    trainModel(cfg)

if __name__ == "__main__":
    main()
