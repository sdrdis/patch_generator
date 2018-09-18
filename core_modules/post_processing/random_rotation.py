import random
import numpy as np
import scipy.misc

def process(ex_X, ex_y, ex_complementary_X, params):
    flip_lr = True
    if ('flip_lr' in params):
        flip_lr = params['flip_lr']

    flip_ud = True
    if ('flip_ud' in params):
        flip_ud = params['flip_ud']

    rot_90 = False
    if ('rot_90' in params):
        rot_90 = params['rot_90']

    arbitrary_angle = True
    if ('arbitrary_angle' in params):
        arbitrary_angle = params['arbitrary_angle']

    if (flip_lr):
        if (random.randint(0, 1) == 1):
            ex_X = np.fliplr(ex_X)
            ex_y = np.fliplr(ex_y)

    if (flip_ud):
        if (random.randint(0, 1) == 1):
            ex_X = np.flipud(ex_X)
            ex_y = np.flipud(ex_y)

    if (rot_90):
        rot_90_nb = random.randint(0, 3)
        ex_X = np.rot90(ex_X, rot_90_nb)
        ex_y = np.rot90(ex_y, rot_90_nb)

    if (arbitrary_angle != False):
        from_angle = 0
        to_angle = 360
        if (arbitrary_angle != True):
            from_angle, to_angle = arbitrary_angle[0], arbitrary_angle[1]
        angle = random.uniform(from_angle, to_angle)
        ex_X = scipy.misc.imrotate(ex_X, angle)
        ex_y_arr = []
        for j in range(ex_y.shape[2]):
            ex_y_arr.append(scipy.misc.imrotate(ex_y[:, :, j], angle))
        ex_y = np.moveaxis(np.array(ex_y_arr), 0, 2)
        ex_y = ex_y.astype(float) / 255.0

    return ex_X, ex_y, ex_complementary_X