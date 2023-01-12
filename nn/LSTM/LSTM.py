import torch.nn
import torch.nn as nn


class LSTM(nn.Module):
    def __init__(self):
        super(LSTM, self).__init__()

        inputSize = 1
        hiddenSize = 32  # 隐藏单元个数 可调
        numLayers = 1  # lstm的层数

        self.LSTM = nn.LSTM(input_size=inputSize, hidden_size=hiddenSize, num_layers=numLayers, batch_first=True)
        self.Linear = nn.Linear(hiddenSize, 1)
        self.activefn = torch.nn.LeakyReLU(negative_slope=0.01, inplace=False)

    def forward(self, X):
        _, (hn, cn) = self.LSTM(X)
        hn = hn.transpose(0, 1)
        output = self.Linear(hn)
        output = self.activefn(output)
        output = output.reshape(-1, 1)
        return output
