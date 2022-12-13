from collections import OrderedDict
from ConvRNN import CGRU_cell, CLSTM_cell

""" 16 32 64
convlstm_encoder_params = [
    [
        OrderedDict({'conv1_leaky_1': [2, 16, 3, 1, 1]}),
        OrderedDict({'conv2_leaky_1': [32, 32, 3, 2, 1]}),
        OrderedDict({'conv3_leaky_1': [32, 32, 3, 2, 1]}),
    ],
    [
        CLSTM_cell(shape=(432, 432), input_channels=16, filter_size=5, num_features=32),
        CLSTM_cell(shape=(216, 216), input_channels=32, filter_size=5, num_features=32),
        CLSTM_cell(shape=(108, 108), input_channels=32, filter_size=5, num_features=64)
    ]
]

convlstm_decoder_params = [
    [
        OrderedDict({'deconv1_leaky_1': [64, 64, 4, 2, 1]}),
        OrderedDict({'deconv2_leaky_1': [32, 32, 4, 2, 1]}),
        OrderedDict({
            'conv3_leaky_1': [32, 16, 3, 1, 1],
            'conv4_leaky_1': [16, 1, 1, 1, 0]
        }),
    ],
    [
        CLSTM_cell(shape=(108, 108), input_channels=64, filter_size=5, num_features=64),
        CLSTM_cell(shape=(216, 216), input_channels=64, filter_size=5, num_features=32),
        CLSTM_cell(shape=(432, 432), input_channels=32, filter_size=5, num_features=32),
    ]
]
"""
# build model
# in_channels=v[0], out_channels=v[1], kernel_size=v[2], stride=v[3], padding=v[4]
convlstm_encoder_params = [
    [
        OrderedDict({'conv1_leaky_1': [27, 16, 3, 1, 1]}),
        OrderedDict({'conv2_leaky_1': [24, 24, 3, 2, 1]}),
    ],
    [
        CLSTM_cell(shape=(432, 432), input_channels=16, filter_size=5, num_features=24),
        CLSTM_cell(shape=(216, 216), input_channels=24, filter_size=5, num_features=32),
    ]
]

convlstm_decoder_params = [
    [
        OrderedDict({'deconv2_leaky_1': [32, 32, 4, 2, 1]}),
        OrderedDict({
            'conv3_leaky_1': [24, 16, 3, 1, 1],
            'conv4_leaky_1': [16, 1, 1, 1, 0]
        }),
    ],
    [
        CLSTM_cell(shape=(216, 216), input_channels=32, filter_size=5, num_features=32),
        CLSTM_cell(shape=(432, 432), input_channels=32, filter_size=5, num_features=24),
    ]
]

convgru_encoder_params = [
    [
        OrderedDict({'conv1_leaky_1': [1, 16, 3, 1, 1]}),
        OrderedDict({'conv2_leaky_1': [64, 64, 3, 2, 1]}),
        OrderedDict({'conv3_leaky_1': [96, 96, 3, 2, 1]}),
    ],

    [
        CGRU_cell(shape=(64, 64), input_channels=16, filter_size=5, num_features=64),
        CGRU_cell(shape=(32, 32), input_channels=64, filter_size=5, num_features=96),
        CGRU_cell(shape=(16, 16), input_channels=96, filter_size=5, num_features=96)
    ]
]

convgru_decoder_params = [
    [
        OrderedDict({'deconv1_leaky_1': [96, 96, 4, 2, 1]}),
        OrderedDict({'deconv2_leaky_1': [96, 96, 4, 2, 1]}),
        OrderedDict({
            'conv3_leaky_1': [64, 16, 3, 1, 1],
            'conv4_leaky_1': [16, 1, 1, 1, 0]
        }),
    ],

    [
        CGRU_cell(shape=(16, 16), input_channels=96, filter_size=5, num_features=96),
        CGRU_cell(shape=(32, 32), input_channels=96, filter_size=5, num_features=96),
        CGRU_cell(shape=(64, 64), input_channels=96, filter_size=5, num_features=64),
    ]
]
