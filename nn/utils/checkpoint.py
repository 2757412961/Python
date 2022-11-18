# -*- coding: utf-8 -*-
import torch
import torch.nn as nn

# fake variable
epoch, model, loss, optimizer, PATH, Net, args, kwargs, TheOptimizerClass = None

# save
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
    # ...
}, PATH)

# load
model = Net(*args, **kwargs)
optimizer = TheOptimizerClass(*args, **kwargs)

checkpoint = torch.load(PATH)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']

model.train()
# model.eval()
