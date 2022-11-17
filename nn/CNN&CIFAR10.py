# -*- coding: utf-8 -*-
'''
Training an image classifier
1. Load and normalize the CIFAR10 training and test datasets using torchvision
2. Define a Convolutional Neural Network
3. Define a loss function
4. Train the network on the training data
5. Test the network on the test data
'''

import torch

device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
print(f'Run with device:{device}')

if __name__ == '__main__':
    # 1. Load and normalize CIFAR10
    print("================================== 1. Load and normalize CIFAR10 ====================================")
    # Using torchvision, it’s extremely easy to load CIFAR10.
    import torchvision
    import torchvision.transforms as transforms

    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    batch_size = 4
    trainset = torchvision.datasets.CIFAR10(root='../data', train=True, download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=2)
    testset = torchvision.datasets.CIFAR10(root='../data', train=False, download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=2)
    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
    print(trainloader.dataset.data.shape)
    print(testloader.dataset.data.shape)

    print("========================================== Print img ================================================")
    import matplotlib.pyplot as plt
    import numpy as np

    # functions to show an image
    def imshow(img):
        img = img / 2 + 0.5  # unnormalize
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.show()

    # get some random training images
    dataiter = iter(trainloader)
    images, labels = next(dataiter)

    # show images
    imshow(torchvision.utils.make_grid(images))
    # print labels
    print(' '.join(f'{classes[labels[j]]:5s}' for j in range(batch_size)))

    print("============================= 2. Define a Convolutional Neural Network ===============================")
    import torch.nn as nn
    import torch.nn.functional as F

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 6, 5)
            self.pool = nn.MaxPool2d(2, 2)
            self.conv2 = nn.Conv2d(6, 16, 5)
            self.fc1 = nn.Linear(16 * 5 * 5, 120)
            self.fc2 = nn.Linear(120, 84)
            self.fc3 = nn.Linear(84, 10)

        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            x = torch.flatten(x, 1)  # flatten all dimensions except batch
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    net = Net().to(device)
    print(net)

    print("============================= 3. Define a Loss function and optimizer ===============================")
    # Let’s use a Classification Cross-Entropy loss and SGD with momentum.
    import torch.optim as optim

    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    print(optimizer)

    print("====================================== 4. Train the network =========================================")
    # We simply have to loop over our data iterator, and feed the inputs to the network and optimize.
    # loss.backward()函数的作用是根据loss来计算网络参数的梯度，其对应的输入默认为网络的叶子节点
    # 优化器的作用就是针对计算得到的参数梯度对网络参数进行更新，所以要想使得优化器起作用，主要需要两个东西：
    # - 优化器需要知道当前的网络模型的参数空间
    # - 优化器需要知道反向传播的梯度信息（即backward计算得到的信息）
    import time

    start = time.time()
    # for epoch in range(2):  # loop over the dataset multiple times
    #     running_loss = 0.0
    #     for i, data in enumerate(trainloader, 0):
    #         # get the inputs; data is a list of [inputs, labels]
    #         inputs, labels = data
    #         inputs = inputs.to(device)
    #         labels = labels.to(device)
    #
    #         # zero the parameter gradients
    #         optimizer.zero_grad()
    #
    #         # forward + backward + optimize
    #         outputs = net(inputs)
    #         loss = criterion(outputs, labels)
    #         loss.backward()
    #         optimizer.step()
    #
    #         # print statistics
    #         running_loss += loss.item()
    #         if i % 2000 == 1999:  # print every 2000 mini-batches
    #             currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #             print(f'[{currentTime}] [{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
    #             running_loss = 0.0

    end = time.time()
    print("程序运行时间为：" + str(end - start) + "秒")
    # Let’s quickly save our trained model:
    PATH = 'model/cifar_net.pth'
    torch.save(net.state_dict(), PATH)
    print('Finished Training')

    print("================================ 5. Test the network on the test data ================================")
    dataiter = iter(testloader)
    for _ in range(5):
        images, labels = next(dataiter)

        # print images
        imshow(torchvision.utils.make_grid(images))
        print('GroundTruth: ', ' '.join(f'{classes[labels[j]]:5s}' for j in range(4)))
        print('CNN  Result: ', ' '.join(f'{classes[net(images)]:5s}' for j in range(4)))




