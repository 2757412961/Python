# -*- coding: utf-8 -*-
"""
一个简简单单的训练脚本，训练名叫 Exp1
"""
import torch
from torch.utils.data import DataLoader, ConcatDataset
from CNNClass import ConvNetwork
from ConvLSTM import ENSOConvLSTM
from ConvLSTMDataLoader import ENSODataset
import TrainFuncVal as TFV
import FuncPlot
import os

# 忽略 matplotlib与torch的一个加载错误。
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# 初始化网络
Net = ENSOConvLSTM(input_dim=2,
                   hidden_dim=[8, 16, 16],
                   output_dim=23,
                   kernel_size=[(3, 3), (5, 5), (7, 7)],
                   num_layers=3,
                   batch_first=True,
                   bias=True,
                   return_all_layers=True)

# 加载数据
DS = ENSODataset("OBSTrain")
DS1 = ENSODataset("OBSVal")
# 生成DataLoader
DL = DataLoader(ConcatDataset((DS, DS1)), batch_size=400, shuffle=True)

# 开始训练与验证
TFV.trainFunc(Net, DL, 5, saveName="Exp2", optim=torch.optim.Adam(Net.parameters()),
              val_data=iter(DataLoader(ENSODataset(type_="OBSVal"), batch_size=1000, shuffle=False)))

# 如果需要迁移学习 ， 可以 将Dataset分开加载
# 画出结果
FuncPlot.trainPlot("Exp2")
