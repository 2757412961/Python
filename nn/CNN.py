# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    # 您只需定义forward函数，backward 函数（计算梯度的地方）会自动为您使用autograd. forward您可以在函数中使用任何 Tensor 操作。
    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square, you can specify with a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


if __name__ == '__main__':
    print("===================== Define the network =====================")
    net = Net()
    print(net)

    print("===============================================================")
    params = list(net.parameters())
    print(len(params))
    print(params[0].size())  # conv1's .weight

    print("===============================================================")
    # Let’s try a random 32x32 input. Note: expected input size of this net (LeNet) is 32x32.
    # To use this net on the MNIST dataset, please resize the images from the dataset to 32x32.
    input = torch.randn(1, 1, 32, 32)
    out = net(input)
    print(out)
    print(out.size())

    print("===============================================================")
    # Zero the gradient buffers of all parameters and backprops with random gradients:
    net.zero_grad()
    out.backward(torch.randn(1, 10))

    print("======================== Loss Function ========================")
    output = net(input)
    target = torch.randn(10)  # a dummy target, for example
    target = target.view(1, -1)  # make it the same shape as output
    criterion = nn.MSELoss()
    loss = criterion(output, target)
    print(loss)
    '''
    input -> conv2d -> relu -> maxpool2d -> conv2d -> relu -> maxpool2d
      -> flatten -> linear -> relu -> linear -> relu -> linear
      -> MSELoss
      -> loss
      '''

    print("======================== Backpropagate ========================")
    net.zero_grad()  # zeroes the gradient buffers of all parameters
    print('conv1.bias.grad before backward')
    print(net.conv1.bias.grad)
    loss.backward()
    print('conv1.bias.grad after backward')
    print(net.conv1.bias.grad)

    print("===================== Update the weights =====================")
    # weight = weight - learning_rate * gradient
    learning_rate = 0.01
    for f in net.parameters():
        f.data.sub_(f.grad.data * learning_rate)
    # However, as you use neural networks, you want to use various different update rules such as
    # SGD, Nesterov-SGD, Adam, RMSProp, etc. To enable this, we built a small package: torch.optim
    # that implements all these methods. Using it is very simple:
    import torch.optim as optim
    # create your optimizer
    optimizer = optim.SGD(net.parameters(), lr=0.01)
    # in your training loop:
    optimizer.zero_grad()  # zero the gradient buffers
    print(net.conv1.bias.grad)
    output = net(input)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()  # Does the update
    print(net.conv1.bias.grad)



