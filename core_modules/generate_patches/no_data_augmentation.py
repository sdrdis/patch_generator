import math
import numpy as np
import random
import scipy.misc
import scipy.ndimage
from os.path import join

def generate(patch_i, item_data, subfolder_patches_path, params, prefix=''):
    X = item_data['X']
    complementary_X = item_data['complementary_X']
    y = item_data['y']

    scipy.misc.imsave(join(subfolder_patches_path, prefix + str(patch_i) + '_X.png'), X)
    if (len(complementary_X) > 0):
        np.savez_compressed(join(subfolder_patches_path, prefix + str(patch_i) + '_comp_X.npz'), complementary_X=complementary_X)
    np.savez_compressed(join(subfolder_patches_path, prefix + str(patch_i) + '_y.npz'), y=y)
    patch_i += 1


    return patch_i