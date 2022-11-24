# -*- coding: utf-8 -*-
# @File  : DownloadBar.py
# @Author: Zjh
# @Date  : 2022/11/24
# @Update: 2022/11/24
# @Desc  :

from progressbar import *

if __name__ == '__main__':
    to_do = [2, 3, 4, 4, 31, 5, 6, 457, 67, 564, 87, 458, 23]
    widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
    bar = ProgressBar(widgets=widgets)
    # bar.start()
    for i in bar(to_do):  # future变量表示已完成的Future对象，所以后续future.result()绝不会阻塞
        print(i)
