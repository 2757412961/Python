# -*- coding: utf-8 -*-
import torch

# fake variable
model, PATH, Net, args, kwargs = None

# 3.跨device（cpu/gpu）来save/load模型
'''
比如模型是在GPU上训练的，现在要load到cpu上。或者反之，或者在CPU上训练，在GPU上load。这三种情况下，save的方法是一样的：
'''

torch.save(model.state_dict(), PATH)

'''
而load的方法就不一样了：
'''

###############Save on GPU, Load on GPU #########
device = torch.device("cuda")
model = Net(*args, **kwargs)
model.load_state_dict(torch.load(PATH))
model.to(device)
# 确保在输入给网络的tensor上调用input = input.to(device)

###############Save on GPU, Load on CPU #########
device = torch.device('cpu')
model = Net(*args, **kwargs)
model.load_state_dict(torch.load(PATH, map_location=device))

###############Save on CPU, Load on GPU #########
device = torch.device("cuda")
model = Net(*args, **kwargs)
model.load_state_dict(torch.load(PATH, map_location="cuda:0"))  # Choose whatever GPU device number you want
model.to(device)
# 确保在输入给网络的tensor上调用input = input.to(device)
