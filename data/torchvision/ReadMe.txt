torchvision 库是服务于pytorch深度学习框架的,用来生成图片,视频数据集,和一些流行的模型类和预训练模型.

所有数据集都是 torch.utils.data.dataset 的子类，也就是说，它们都实现了 __getitem__ 和 __len__ 方法。
因此，它们都可以传递给 torch.utils.data.dataloader，后者可以使用 torch.multiprocessing workers 并行加载多个样本。例如：

imagenet_data = torchvision.datasets.ImageFolder('path/to/imagenet_root/')
data_loader = torch.utils.data.DataLoader(imagenet_data,
                                          batch_size=4,
                                          shuffle=True,
                                          num_workers=args.nThreads)


可获得的数据集如下：
https://blog.csdn.net/Threelights/article/details/88680540
目录
    torchvision.datasets
    MNIST
    Fashion-MNIST
    KMNIST
    EMNIST
    FakeData
    COCO
    Captions
    Detection
    LSUN
    ImageFolder
    DatasetFolder
    Imagenet-12
    CIFAR
    STL10
    SVHN
    PhotoTour
    SBU
    Flickr
    VOC
    Cityscapes

Parameters:
    root (string) –  存在 mnist/processed/training.pt 和 mnist/processed/test.pt 的数据集根目录。
    train (bool, optional) – 如果为True，从 training.pt 创建数据，否则从 test.pt 创建数据。
    download (bool, optional) – 如果为true，则从 Internet 下载数据集并将其放在根目录中。 如果已下载数据集，则不会再次下载。
    transform (callable, optional) –  一个函数/转换，它接收PIL图像并返回转换后的版本。 例如，transforms.RandomCrop
    target_transform (callable, optional) – 接收目标并对其进行转换的函数/转换。