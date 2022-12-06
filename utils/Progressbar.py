# -*- coding: utf-8 -*-
# @File  : Progressbar.py
# @Author: Zjh
# @Date  : 2022/12/6
# @Update: 2022/12/6
# @Desc  :
import time
from tqdm import tqdm, trange

if __name__ == '__main__':
    #################################
    # 基于迭代对象运行: tqdm(iterator) #
    #################################
    # trange(i)是tqdm(range(i))的一种简单写法
    for i in trange(100):
        time.sleep(0.05)

    for i in tqdm(range(100), desc='Processing'):
        time.sleep(0.05)

    dic = ['a', 'b', 'c', 'd', 'e']
    pbar = tqdm(dic)
    for i in pbar:
        pbar.set_description('Processing ' + i)
        time.sleep(0.2)

    # 100%|██████████| 100/100 [00:06<00:00, 16.04it/s]
    # Processing: 100%|██████████| 100/100 [00:06<00:00, 16.05it/s]
    # Processing e: 100%|██████████| 5/5 [00:01<00:00,  4.69it/s]

    #################################
    # 手动进行更新 #
    #################################
    import time
    from tqdm import tqdm

    with tqdm(total=200) as pbar:
        pbar.set_description('Processing')
        # total表示总的项目, 循环的次数20*10(每次更新数目) = 200(total)
        for i in range(20):
            # 进行动作, 这里是过0.1s
            time.sleep(0.1)
            # 进行进度更新, 这里设置10个
            pbar.update(10)

    # Processing: 100%|██████████| 200/200 [00:02<00:00, 91.94it/s]
