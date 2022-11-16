# -*- coding: utf-8 -*-
import torchvision
from torchvision import datasets, transforms
transform = transforms.Compose([transforms.ToTensor(),
                              transforms.Normalize((0.5,), (0.5,)),
                              ])
trainset = datasets.MNIST('.', download=True, train=True, transform=transform)

