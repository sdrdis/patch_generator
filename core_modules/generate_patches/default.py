import math
import numpy as np
import random
import scipy.misc
import scipy.ndimage
from os.path import join
import time

def array_pad(arr, _pad, mode, **kwargs):
    pad = _pad
    for i in range(len(arr.shape) - len(pad)):
        pad.append((0, 0))
    return np.pad(arr, pad, mode, **kwargs)

def extract_padded(arr_np, patch):
    decal_y = max(0, -patch[0])
    decal_x = max(0, -patch[2])
    pad = [(decal_y, max(0, patch[1] - arr_np.shape[0])), (decal_x, max(0, patch[3] - arr_np.shape[1]))]
    arr_np = array_pad(arr_np, pad, 'constant', constant_values=(0))
    return arr_np[patch[0]+decal_y:patch[1]+decal_y, patch[2]+decal_x:patch[3]+decal_x]


def generate(patch_i, item_data, subfolder_patches_path, params, thread_i, postprocessing_modules, postprocessing_params):
    prefix = '(:thread_i)_'
    if ('prefix' in params):
        prefix = params['prefix']

    patch_ratio = 2.0
    if ('patch_ratio' in params):
        patch_ratio = params['patch_ratio']

    patch_shape = params['shape']

    patch_margin = int(math.ceil(math.sqrt(2) * np.max(patch_shape) / 2))
    if ('patch_margin' in params):
        patch_margin = params['patch_margin']

    X_original = item_data['X']
    complementary_X = item_data['complementary_X']
    y_original = item_data['y']

    X = X_original.copy()
    y = y_original.copy()


    pad = [(0, max(0, patch_shape[0] - X.shape[0])), (0, max(0, patch_shape[1] - X.shape[1]))]

    X = array_pad(X, pad, 'constant', constant_values=(0))
    y = array_pad(y, pad, 'constant', constant_values=(0))

    nb_patches_to_acquire = int(math.ceil(((X.shape[0] * X.shape[1]) / (patch_shape[0] * patch_shape[1])) * patch_ratio))


    for i in range(nb_patches_to_acquire):
        patch_y = int(round(random.uniform(0, X.shape[0] - patch_shape[0])))
        patch_x = int(round(random.uniform(0, X.shape[1] - patch_shape[1])))

        patch = [patch_y, patch_y + patch_shape[0], patch_x, patch_x + patch_shape[1]]

        larger_patch = [patch[0] - patch_margin, patch[1] + patch_margin,
                        patch[2] - patch_margin, patch[3] + patch_margin]

        ex_X = extract_padded(X, larger_patch)
        ex_y = extract_padded(y, larger_patch).astype(float)
        ex_complementary_X = complementary_X.copy()

        for i in range(len(postprocessing_modules)):
            ex_X, ex_y, ex_complementary_X = postprocessing_modules[i].process(ex_X, ex_y, ex_complementary_X, postprocessing_params[i])


        ex_X = ex_X[patch_margin:-patch_margin, patch_margin:-patch_margin]
        ex_y = ex_y[patch_margin:-patch_margin, patch_margin:-patch_margin]


        if (ex_y.shape[0] != patch_shape[0] or ex_y.shape[1] != patch_shape[1]):
            print('DEBUG NEEDED!', patch_i, ex_y.shape, y.shape, patch_shape, '#'*30)
            #continue

        patch_prefix = prefix.replace('(:thread_i)', str(thread_i))
        scipy.misc.imsave(join(subfolder_patches_path, patch_prefix + str(patch_i) + '_X.png'), ex_X)
        if (len(complementary_X) > 0):
            np.savez_compressed(join(subfolder_patches_path, patch_prefix + str(patch_i) + '_comp_X.npz'), complementary_X=complementary_X)

        np.savez_compressed(join(subfolder_patches_path, patch_prefix + str(patch_i) + '_y.npz'), y=ex_y)
        patch_i += 1

    return patch_i