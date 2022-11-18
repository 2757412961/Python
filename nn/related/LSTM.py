import torch
import torch.nn as nn

if __name__ == '__main__':
    rnn = nn.LSTM(10, 20, 2)  # 定义一个LSTM（初始化）
    input = torch.randn(5, 3, 10)
    h0 = torch.randn(2, 3, 20)
    c0 = torch.randn(2, 3, 20)
    output, (hn, cn) = rnn(input, (h0, c0))  # 使用LSTM测试
