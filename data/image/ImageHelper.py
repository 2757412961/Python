# -*- coding: utf-8 -*-
# @File  : ImageHelper.py
# @Author: Zjh
# @Date  : 2022/12/7
# @Update: 2022/12/7
# @Desc  :

import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as transforms

# URL
# https://zhuanlan.zhihu.com/p/353938168
if __name__ == '__main__':
    dirpath = '/home/zjh/Ocean/MODIS_AQUA_PAR_par/AQUA_MODIS.20030104.L3m.DAY.PAR.par.4km.nc.png'
    # img_plt = plt.imread('/home/zjh/Ocean/MODIS_AQUA_IOP_a_412/AQUA_MODIS.20030102.L3m.DAY.IOP.a_412.4km.nc.png')
    # img_plt = plt.imread('/home/zjh/Ocean/MODIS_AQUA_PIC_pic/AQUA_MODIS.20020704.L3m.DAY.PIC.pic.4km.nc.png')
    img_plt = plt.imread('/home/zjh/Ocean/MODIS_AQUA_PAR_par/AQUA_MODIS.20030104.L3m.DAY.PAR.par.4km.nc.png')
    print("img_plt :", img_plt.shape)
    print("img_plt :", type(img_plt))

    img_res = img_plt[..., 0:3].transpose(2, 0, 1)

    # 注意：使用torchvision.transforms时要注意一下，其子函数 ToTensor() 是没有参数输入
    transf = transforms.ToTensor()
    img_tensor = transf(img_res)

    ########################################
    # 一、OpenCV读取图片
    import cv2

    img_cv = cv2.imread(dirpath)  # 读取数据
    print("img_cv:", img_cv.shape)
    print("img_cv:", type(img_cv))

    ########################################
    # 二、PIL读取图片
    from PIL import Image
    import numpy as np

    img_PIL = Image.open(dirpath)  # 读取数据
    print("img_PIL:", img_PIL)
    print("img_PIL:", type(img_PIL))
    # 将图片转换成np.ndarray格式
    img_PIL = np.array(img_PIL)

    ########################################
    # 四、skimage读取图片
    import skimage.io as io

    img_io = io.imread(dirpath)  # 读取数据
    print("img_io :", img_io.shape)
    print("img_io :", type(img_io))

    ########################################
    # 五、matplotlib.image读取图片
    import matplotlib.image as mpig

    img_mpig = mpig.imread(dirpath)  # 读取数据
    print("img_mpig :", img_mpig.shape)
    print("img_mpig :", type(img_mpig))

    ########################################
    # 六、matplotlib.pyplot读取图片
    import matplotlib.pyplot as plt

    img_plt = plt.imread(dirpath)
    print("img_plt :", img_plt.shape)
    print("img_plt :", type(img_plt))

    ########################################
    # 显示读取的图片
    plt.imshow(img_plt, cmap=plt.cm.binary)
    plt.show()
