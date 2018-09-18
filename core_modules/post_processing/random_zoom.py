import random
import numpy as np
import scipy.misc
import scipy.ndimage
import common

def zoom(im_np, zoom_factor):
    if (len(im_np.shape) == 2):
        return scipy.ndimage.interpolation.zoom(im_np, zoom_factor)
    else:
        new_im_np = []
        for i in range(im_np.shape[2]):
            new_im_np.append(scipy.ndimage.interpolation.zoom(im_np[:,:,i], zoom_factor))
        new_im_np = np.array(new_im_np)
        new_im_np = np.moveaxis(new_im_np, 0, 2)
        return new_im_np

def process(ex_X, ex_y, ex_complementary_X, params):
    zoom_var_min = None
    if ('zoom_var_min' in params):
        zoom_var_min = params['zoom_var_min']
    zoom_var_max = None
    if ('zoom_var_max' in params):
        zoom_var_max = params['zoom_var_max']

    patch_shape = ex_X.shape


    if (zoom_var_min is not None and zoom_var_max is not None):
        zoom_factor = random.uniform(zoom_var_min, zoom_var_max)
        zoom_X = [zoom_factor, zoom_factor]
        for i in range(len(ex_X.shape) - len(zoom_X)):
            zoom_X.append(1.0)

        zoom_y = [zoom_factor, zoom_factor]
        for i in range(len(ex_y.shape) - len(zoom_y)):
            zoom_y.append(1.0)

        initial_shape = ex_X.shape
        ex_X = zoom(ex_X, zoom_factor)
        ex_y = zoom(ex_y, zoom_factor)
        diff_shape = (ex_X.shape[0] - initial_shape[0], ex_X.shape[1] - initial_shape[1])
        hheight, hwidth = int(-diff_shape[0] / 2), int(-diff_shape[1] / 2)
        pad = [
            (max(0, hheight), max(0, -diff_shape[0] - hheight)),
            (max(0, hwidth), max(0, -diff_shape[1] - hwidth))
        ]

        ex_X = common.array_pad(ex_X, pad, 'constant', constant_values=(0))
        ex_y = common.array_pad(ex_y, pad, 'constant', constant_values=(0))

        ecy, ecx = int(ex_X.shape[0] / 2), int(ex_X.shape[1] / 2)
        from_y, from_x = ecy - int(patch_shape[0] / 2), ecx - int(patch_shape[1] / 2)
        ex_X = ex_X[from_y:from_y + patch_shape[0],from_x:from_x + patch_shape[1]]
        ex_y = ex_y[from_y:from_y + patch_shape[0],from_x:from_x + patch_shape[1]]
        ex_y = (ex_y > 0.5).astype(float)

    return ex_X, ex_y, ex_complementary_X