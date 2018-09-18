import numpy as np

def process(item_data, params):
    item_data['y'] = np.dstack(item_data['y'])