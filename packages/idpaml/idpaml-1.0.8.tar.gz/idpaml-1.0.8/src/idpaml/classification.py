#!/usr/bin/env python
import pandas as pd
import torch

class BinaryClassificationDataset(torch.utils.data.Dataset):
    def __init__(self, df: pd.DataFrame, tensor=None, class_label: str="class"):
        self.data = df
        self.tensor = tensor
        self.class_label = class_label
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        features = self.data.drop(self.class_label, axis=1)
        labels = self.data[self.class_label].to_numpy()
        feature = features.iloc[idx, :].to_numpy()
        if self.tensor:
            # convert to tensor
            feature = torch.Tensor(feature)
            labels = torch.Tensor(labels)
            labels = labels.type(torch.LongTensor)
            label = labels[idx]
            return feature, label
        else:
            label = labels.iloc[idx]
        return feature, label
    