import json
import numpy as np

def dict_merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                dict_merge(a[key], b[key], path + [str(key)])
        else:
            a[key] = b[key]
    return a

def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def get_ordered_keys(dict):
    keys = list(dict.keys())
    keys_ids = []
    for key in keys:
        keys_ids.append(float(key.split('_')[0]))
    idx = np.argsort(keys_ids)
    ordered_keys = np.array(keys)[idx]
    return ordered_keys

def get_params_module(dict):
    params = {}
    if ('params' in dict):
        params = dict['params']
    return params


def get_processes_list(config):
    pp_keys = get_ordered_keys(config)
    modules = []
    params = []
    for pp_key in pp_keys:
        process = config[pp_key]
        if (process is None):
            continue
        modules.append(__import__(process['module'], fromlist=['']))
        params.append(get_params_module(process))
    return modules, params

def array_pad(arr, _pad, mode, **kwargs):
    pad = _pad
    for i in range(len(arr.shape) - len(pad)):
        pad.append((0, 0))
    return np.pad(arr, pad, mode, **kwargs)

def get_param(params, key, default):
    if (key not in params):
        return default
    return params[key]