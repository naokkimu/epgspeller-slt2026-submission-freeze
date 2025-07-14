import torch
from torch.utils.data import Dataset
from .augmentations import TimeMask, ElectrodeMask, TimeWarp


class SpeechDataset(Dataset):
    def __init__(self, data, transform=None, sort_by_length=False, aug_conf=None):
        self.data = data
        self.transform = transform
        self.n_days = len(data)
        self.n_trials = sum([len(d["sentenceDat"]) for d in data])

        self.neural_feats = []
        self.phone_seqs = []
        self.neural_time_bins = []
        self.phone_seq_lens = []
        self.days = []
        for day in range(self.n_days):
            for trial in range(len(data[day]["sentenceDat"])):
                self.neural_feats.append(data[day]["sentenceDat"][trial])
                self.phone_seqs.append(data[day]["phonemes"][trial])
                self.neural_time_bins.append(data[day]["sentenceDat"][trial].shape[0])
                self.phone_seq_lens.append(data[day]["phoneLens"][trial])
                self.days.append(day)
        
        # シーケンス長でソート
        if sort_by_length:
            sorted_indices = sorted(range(len(self.neural_time_bins)), 
                                 key=lambda k: self.neural_time_bins[k])
            self.neural_feats = [self.neural_feats[i] for i in sorted_indices]
            self.phone_seqs = [self.phone_seqs[i] for i in sorted_indices]
            self.neural_time_bins = [self.neural_time_bins[i] for i in sorted_indices]
            self.phone_seq_lens = [self.phone_seq_lens[i] for i in sorted_indices]
            self.days = [self.days[i] for i in sorted_indices]

        # Initialize augmentation operations
        self.aug_ops = []
        if aug_conf:
            if aug_conf.get("time_mask"):
                self.aug_ops.append(TimeMask(**aug_conf["time_mask"]))
            if aug_conf.get("electrode_mask"):
                self.aug_ops.append(ElectrodeMask(**aug_conf["electrode_mask"]))
            if aug_conf.get("time_warp"):
                self.aug_ops.append(TimeWarp(**aug_conf["time_warp"]))

    def __len__(self):
        return self.n_trials

    def __getitem__(self, idx):
        neural_feats = torch.tensor(self.neural_feats[idx], dtype=torch.float32)

        if self.transform:
            neural_feats = self.transform(neural_feats)

        # Apply augmentations
        for op in self.aug_ops:
            neural_feats = op(neural_feats)

        return (
            neural_feats,
            torch.tensor(self.phone_seqs[idx], dtype=torch.int32),
            torch.tensor(self.neural_time_bins[idx], dtype=torch.int32),
            torch.tensor(self.phone_seq_lens[idx], dtype=torch.int32),
            torch.tensor(self.days[idx], dtype=torch.int64),
        )
