import torch


class Net:
    None


class TheOptimizerClass:
    None


epoch = 00
model = torch.nn.Module()
loss = torch.nn.MSELoss()
optimizer = torch.optim.Adam()
PATH = './checkpoint.cp'

# save
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
    # ...
}, PATH)

# load
model = Net()  # Net(*args, **kwargs)
optimizer = TheOptimizerClass()  # TheOptimizerClass(*args, **kwargs)

checkpoint = torch.load(PATH)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']

model.train()
# model.eval()
