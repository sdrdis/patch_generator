import numpy as np
import scipy.misc
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def process(item_data, params):
    im_np = item_data['X']
    if (len(im_np.shape) > 2):
        item_data['X'] = rgb2gray(im_np)
