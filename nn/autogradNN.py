# -*- coding: utf-8 -*-
import torch
import math

'''
在上面的示例中，我们必须手动实现神经网络的前向和后向传递。手动实现反向传递对于小型两层网络来说不是什么大问题，但对于大型复杂网络来说很快就会变得非常棘手。
值得庆幸的是，我们可以使用自动微分 来自动计算神经网络中的反向传递。PyTorch 中的 autograd包正好提供了这个功能。使用 autograd 时，网络的前向传播将定义一个 计算图；图中的节点将是张量，边将是从输入张量生成输出张量的函数。通过该图反向传播可以让您轻松计算梯度。
这听起来很复杂，在实践中使用起来非常简单。每个 Tensor 代表计算图中的一个节点。如果x是一个张量， x.requires_grad=True那么x.grad另一个张量持有x关于某个标量值的梯度。
在这里，我们使用 PyTorch Tensors 和 autograd 来实现我们的三阶多项式拟合正弦波示例；现在我们不再需要通过网络手动实现反向传递：
'''


if __name__ == '__main__':
    # Create Tensors to hold input and outputs.
    x = torch.linspace(-math.pi, math.pi, 2000)
    y = torch.sin(x)

    # For this example, the output y is a linear function of (x, x^2, x^3), so
    # we can consider it as a linear layer neural network. Let's prepare the
    # tensor (x, x^2, x^3).
    p = torch.tensor([1, 2, 3])
    xx = x.unsqueeze(-1).pow(p)

    # In the above code, x.unsqueeze(-1) has shape (2000, 1), and p has shape
    # (3,), for this case, broadcasting semantics will apply to obtain a tensor
    # of shape (2000, 3)

    # Use the nn package to define our model as a sequence of layers. nn.Sequential
    # is a Module which contains other Modules, and applies them in sequence to
    # produce its output. The Linear Module computes output from input using a
    # linear function, and holds internal Tensors for its weight and bias.
    # The Flatten layer flattens the output of the linear layer to a 1D tensor,
    # to match the shape of `y`.
    model = torch.nn.Sequential(
        torch.nn.Linear(3, 1),
        torch.nn.Flatten(0, 1)
    )

    # The nn package also contains definitions of popular loss functions; in this
    # case we will use Mean Squared Error (MSE) as our loss function.
    loss_fn = torch.nn.MSELoss(reduction='sum')

    learning_rate = 1e-6
    for t in range(2000):

        # Forward pass: compute predicted y by passing x to the model. Module objects
        # override the __call__ operator so you can call them like functions. When
        # doing so you pass a Tensor of input data to the Module and it produces
        # a Tensor of output data.
        y_pred = model(xx)

        # Compute and print loss. We pass Tensors containing the predicted and true
        # values of y, and the loss function returns a Tensor containing the
        # loss.
        loss = loss_fn(y_pred, y)
        if t % 100 == 99:
            print(t, loss.item())

        # Zero the gradients before running the backward pass.
        model.zero_grad()

        # Backward pass: compute gradient of the loss with respect to all the learnable
        # parameters of the model. Internally, the parameters of each Module are stored
        # in Tensors with requires_grad=True, so this call will compute gradients for
        # all learnable parameters in the model.
        loss.backward()

        # Update the weights using gradient descent. Each parameter is a Tensor, so
        # we can access its gradients like we did before.
        with torch.no_grad():
            for param in model.parameters():
                param -= learning_rate * param.grad

    # You can access the first layer of `model` like accessing the first item of a list
    linear_layer = model[0]
    print(model)

    # For linear layer, its parameters are stored as `weight` and `bias`.
    print(
        f'Result: y = {linear_layer.bias.item()} + {linear_layer.weight[:, 0].item()} x + {linear_layer.weight[:, 1].item()} x^2 + {linear_layer.weight[:, 2].item()} x^3')

