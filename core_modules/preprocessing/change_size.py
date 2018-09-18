import numpy as np
import scipy.misc

def process(item_data, params):
    size = params['size']
    item_data['X'] = scipy.misc.imresize(item_data['X'], size)
    y = []
    if isinstance(item_data['y'], (list,)):
        for j in range(len(item_data['y'])):
            y.append(scipy.misc.imresize(item_data['y'][j].astype(float), size))
    else:
        for j in range(item_data['y'].shape[2]):
            y.append(scipy.misc.imresize(item_data['y'][:,:,j].astype(float), size))
        y = np.array(y)
        y = np.moveaxis(y, 0, 2)
        y = y > 0.5
    item_data['y'] = y