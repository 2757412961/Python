import torch
from LSTM import LSTM
import pandas as pd
import numpy as np
from dataLoader import DataLoaderH
import os
import random
from sklearn.metrics import mean_squared_error


def seed_torch(seed=1029):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


seed_torch()  # 设置随机种子，结果可复现

path = './nino34.csv'
x = np.array(pd.read_csv(path)['nino3.4']).reshape(-1, 1)
y = np.array(pd.read_csv(path)['nino3.4']).reshape(-1, 1)

batchsize = 20  # batchsize 可调
seqlength = 24  # 步长 可调
outdim = 1  # 输出维度
dataLoader = DataLoaderH(batchsize, seqlength, x, y)
train_loader, test_loader, max, min = dataLoader.getdataloader()

import matplotlib.pyplot as plt


def train(lr=0.05, epochs=50):  # lr（学习率）和epoch（迭代轮数）都可调

    print('training start-----------------------------------------------------------------')
    train_loss = []
    test_loss = []
    criterion = torch.nn.MSELoss()
    model = LSTM()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=0.0001, nesterov=False)
    model.train()

    for epoch in range(epochs):

        sum_loss = 0
        for iter, batch in enumerate(train_loader):
            optimizer.zero_grad()
            x, y = batch
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            sum_loss += loss

        epoch_loss = sum_loss.item()
        train_loss.append(epoch_loss)
        print("epoch " + str(epoch) + " loss" + " : " + str(epoch_loss))

        for iter, batch in enumerate(test_loader):
            x, y = batch
            out = model(x)
            test_mse = criterion(out, y)
            test_loss.append(test_mse.item())

    torch.save(model, 'LSTM.pth')  # 保存模型
    print('training end-----------------------------------------------------------------')


def valid():
    print('test start-----------------------------------------------------------------')
    model = torch.load('LSTM.pth')  # 加载模型
    model.eval()

    for iter, batch in enumerate(test_loader):
        x, y = batch
        out = model(x)
        mse = mean_squared_error(y.detach().cpu().numpy(), out.detach().cpu().numpy())
        print("反归一化之前 mse:", mse)
        y = y.detach().numpy() * (max - min) + min
        out = out.detach().numpy() * (max - min) + min

        mse = mean_squared_error(y, out)
        print("反归一化之后 mse:", mse)
        plt.plot(y, color='r', label='true')
        plt.plot(out, color='b', label='predict')
        plt.legend()
        plt.savefig('result.png')
        plt.show()

        print('test end-----------------------------------------------------------------')


if __name__ == '__main__':
    train()  # 训练函数
    valid()  # 测试函数
