import numpy as np

def _std_im(im_np, nb=4, epsilon=0.001):
    sel_im_np = im_np[:, :]
    sel_im_np -= np.mean(sel_im_np)
    sel_im_np /= (np.std(sel_im_np) + epsilon) * nb
    sel_im_np[sel_im_np < -1] = -1
    sel_im_np[sel_im_np > 1] = 1
    return sel_im_np

def standardize_im(im_np, nb=4):
    im_np = im_np.astype(float)
    if (len(im_np.shape) == 3):
        for i in range(im_np.shape[2]):
            im_np[:,:,i] = _std_im(im_np[:,:,i], nb)
    else:
        im_np = _std_im(im_np, nb)
    im_np += 1
    im_np *= 127
    return im_np.astype('uint8')

def process(item_data, params):
    std = 4
    if ('std' in params):
        std = params['std']

    item_data['X'] = standardize_im(item_data['X'], std)