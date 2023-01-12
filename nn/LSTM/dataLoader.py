import numpy as np
import torch
import torch.utils.data as data
from torch.utils.data import DataLoader

def normalization(x):
    """
    :param x:shape[days,features]
    :return:
    """
    train_rate = 0.15
    train_len = (int)(x.shape[0] * train_rate)
    train_data = x[:train_len, :]
    max = np.max(train_data, axis=0)
    min = np.min(train_data, axis=0)
    train_data = (train_data - min) / (max - min)
    test_data = x[train_len:, :]
    test_data = (test_data - min) / (max - min)
    return train_data, test_data, max, min

class Dataset(data.Dataset):
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.length = x.shape[0]

    def __getitem__(self, index):
        return self.x[index][:, :], self.y[index][:]

    def __len__(self):
        return self.length


class DataLoaderH(object):
    def __init__(self, batchsize, seqlength, x,y):
        self.batchSize = batchsize
        self.seqlength = seqlength

        self.x = x
        self.y = y

    def getdataloader(self):
        train_data, test_data, _, _ = normalization(self.x)
        train_y, test_y, max, min = normalization(self.y)
        train_set = []
        test_set = []

        train_set_y = []
        test_set_y = []

        for i in range(0,train_data.shape[0]-self.seqlength-1):
            train_set.append(train_data[i:i+self.seqlength,:])
            train_set_y.append(train_y[i+self.seqlength,:])


        for i in range(0,test_data.shape[0]-self.seqlength-1):
            test_set.append(test_data[i:i+self.seqlength,:])
            test_set_y.append(test_y[i+self.seqlength,:])

        train_set = np.array(train_set,dtype = np.float32)
        test_set = np.array(test_set,dtype = np.float32)
        train_set_y = np.array(train_set_y,dtype = np.float32)
        test_set_y = np.array(test_set_y,dtype = np.float32)

        train_set = torch.tensor(train_set,dtype = torch.float32)
        test_set = torch.tensor(test_set, dtype=torch.float32)
        train_set_y = torch.tensor(train_set_y, dtype=torch.float32)
        test_set_y = torch.tensor(test_set_y, dtype=torch.float32)


        train_dataset = Dataset(train_set,train_set_y)
        train_loader = DataLoader(dataset=train_dataset, batch_size=self.batchSize, num_workers=0, pin_memory=False,shuffle=True)
        test_dataset = Dataset(test_set,test_set_y)
        test_loader = DataLoader(dataset=test_dataset, batch_size=test_set_y.shape[0], num_workers=0, pin_memory=False,shuffle=False)

        return train_loader, test_loader, max, min




