# -*- coding: utf-8 -*-
"""
@File  : normalization.py
@Author: zjh
@Date  : 2023/1/11
@Update: 2023/1/11
@Desc  :
"""

if __name__ == '__main__':
    # Batch Normalization
    import torch
    from torch import nn

    bn = nn.BatchNorm2d(num_features=3, eps=0, affine=False, track_running_stats=False)
    x = torch.rand(10, 3, 5, 5) * 10000
    official_bn = bn(x)  # 官方代码

    x1 = x.permute(1, 0, 2, 3).reshape(3, -1)  # 对(N, H, W)计算均值方差
    mean = x1.mean(dim=1).reshape(1, 3, 1, 1)
    # x1.mean(dim=1)后维度为(3,)
    std = x1.std(dim=1, unbiased=False).reshape(1, 3, 1, 1)
    my_bn = (x - mean) / std
    print((official_bn - my_bn).sum())  # 输出误差

    # Layer Normalization
    import torch
    from torch import nn

    ln = nn.LayerNorm(normalized_shape=[3, 5, 5], eps=0, elementwise_affine=False)
    x = torch.rand(10, 3, 5, 5) * 10000
    official_ln = ln(x)  # 官方代码

    x1 = x.reshape(10, -1)  # 对（C,H,W）计算均值方差
    mean = x1.mean(dim=1).reshape(10, 1, 1, 1)
    std = x1.std(dim=1, unbiased=False).reshape(10, 1, 1, 1)
    my_ln = (x - mean) / std
    print((official_ln - my_ln).sum())

    # Instance Normalization
    import torch
    from torch import nn

    In = nn.InstanceNorm2d(num_features=3, eps=0, affine=False, track_running_stats=False)
    x = torch.rand(10, 3, 5, 5) * 10000
    official_In = In(x)  # 官方代码

    x1 = x.reshape(30, -1)  # 对（H,W）计算均值方差
    mean = x1.mean(dim=1).reshape(10, 3, 1, 1)
    std = x1.std(dim=1, unbiased=False).reshape(10, 3, 1, 1)
    my_In = (x - mean) / std
    print((official_In - my_In).sum())

    # Group Normalization
    import torch
    from torch import nn

    gn = nn.GroupNorm(num_groups=4, num_channels=20, eps=0, affine=False)
    # 分成了4组，也就是说蓝色区域为（5，5, 5）
    x = torch.rand(10, 20, 5, 5) * 10000
    official_gn = gn(x)  # 官方代码

    x1 = x.reshape(10, 4, -1)  # 对（H,W）计算均值方差
    mean = x1.mean(dim=2).reshape(10, 4, -1)
    std = x1.std(dim=2, unbiased=False).reshape(10, 4, -1)
    my_gn = ((x1 - mean) / std).reshape(10, 20, 5, 5)
    print((official_gn - my_gn).sum())
