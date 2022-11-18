import torch
import torch.nn as nn


#  定义模型
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.linear = nn.Linear(3, 1)

    def forward(self, x):
        y = self.linear(x)
        return y

if __name__ == '__main__':
    #  Check if we have a CUDA-capable device; if so, use it
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('Will train on {}'.format(device))

    #  为了让参数恢复成初始化状态，使用最简单的SGD优化器
    net = CNN().to(device)
    optimizer = torch.optim.SGD(net.parameters(), lr=0.1)

    #  载入模型与输入，并打印此时的模型参数
    x = (torch.rand(3)).to(device)
    print('the first output!')
    for name, parameters in net.named_parameters():
        print(name, ':', parameters)

    print('-------------------------------------------------------------------------------')
    #  做梯度下降
    optimizer.zero_grad()
    y = net(x)
    loss = (1 - y) ** 2

    loss.backward()
    optimizer.step()
    #  打印梯度信息
    for name, parameters in net.named_parameters():
        print(name, ':', parameters.grad)
    #  经过第一次更新以后，打印网络参数
    for name, parameters in net.named_parameters():
        print(name, ':', parameters)

    print('-------------------------------------------------------------------------------')
    #  我们直接将网络参数的梯度信息改为相反数来进行梯度上升
    for name, parameters in net.named_parameters():
        parameters.grad *= -1
    #  打印
    optimizer.step()
    print('the second output!')
    for name, parameters in net.named_parameters():
        print(name, ':', parameters.grad)
    #  经过第二次更新以后，打印网络参数
    for name, parameters in net.named_parameters():
        print(name, ':', parameters)
