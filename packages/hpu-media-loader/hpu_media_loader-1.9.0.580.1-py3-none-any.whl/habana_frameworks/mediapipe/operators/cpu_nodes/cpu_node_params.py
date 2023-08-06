
generic_in0_keys = []
generic_in1_keys = ["input"]
generic_in2_keys = ["input0", "input1"]
generic_in4_keys = ["input0", "input1", "input2", "input3"]
generic_in10_keys = ["input0", "input1", "input2", "input3", "input4",
                     "input5", "input6", "input7", "input8", "input9"]

empty_params = {}

media_constant_params = {
    'data': None,
    'layout': '',
    'shape': [1]
}

media_func_params = {
    'func': None,
    'shape': [1],
    'seed': 0,
    # 'unique_number': 0, this will be populated by framework can be used with seed to get unique seed
    'priv_params': {}  # user defined params can be passed here
}

media_ext_cpu_op_params = {
    'impl': None,
    'seed': 0,
    'shape': [1],
    # 'unique_number': 0, this will be populated by framework can be used with seed to get unique seed
    'priv_params': {}  # user defined params can be passed here
}

random_biased_crop_params = {
    'patch_size': [0, 0, 0],  # do not share batch_size
    'over_sampling': 0.33,
    'num_channels': 1,
    'seed': 0,
    'num_workers': 1,
    'cache_bboxes': False
}

basic_crop_params = {
    'patch_size': [0, 0, 0],  # do not share batch_size
    'num_channels': 1,
    'center_crop': False
}

zoom_in_keys = ["input0", "input1", ""]
zoom_params = {
    'patch_size': [0, 0, 0],  # do not share batch_size
    'num_channels': 1,
    'priv_params': {}  # user defined params can be passed here
}

random_flip_in_keys = ["input", "predicate"]
random_flip_cpu_params = {
    'horizontal': 0,
    'vertical': 0,
    'depthwise': 0
}

random_bernoulli_in_keys = ["probability"]
random_bernoulli_params = {
    'seed': 100
}

random_uniform_in_keys = ["seed"]
random_uniform_params = {
    'seed': 0,
    'low': 0,
    'high': 1
}

random_normal_in_keys = ["stddev", "input"]
random_normal_params = {
    'seed': 0,
    'mean': 0,
    'stddev': 0
}

constant_params = {
    'constant': 0
}

where_in_keys = ["perdicate", "input0", "input1"]

# this is duplicate params which needs to be removed once kernels get fixed
crop_params = {
    'crop_w': 100,
    'crop_h': 100,
    'crop_d': 0,
    'crop_pos_x': 0.,
    'crop_pos_y': 0.,
    'crop_pos_z': 0,
    'pad_val': 0,
}
