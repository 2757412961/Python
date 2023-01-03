# -*- coding: utf-8 -*-
import torch
import torch.nn as nn


class ConvNetwork(nn.Module):
    """
    M_Num , N_Num代表convolutional filters and  neurons in the fully connected layer
    """

    def __init__(self, M_Num, N_Num):
        self.M = M_Num
        self.N = N_Num
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(6, M_Num, kernel_size=(4, 8), padding="same"),
            nn.Tanh(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),
            nn.Conv2d(M_Num, M_Num, kernel_size=(4, 2), padding="same"),
            nn.Tanh(),
            nn.MaxPool2d(stride=(2, 2), kernel_size=(2, 2)),
            nn.Conv2d(M_Num, M_Num, kernel_size=(4, 2), stride=(1, 1), padding="same"),
            nn.Tanh(), )
        self.dense = nn.Sequential(
            nn.Linear(6 * 18 * M_Num, N_Num),
            nn.Linear(N_Num, 23))

    def forward(self, InData):
        x = self.conv(InData)
        x = x.reshape(-1, 6 * 18 * self.M)
        x = self.dense(x)
        return x
