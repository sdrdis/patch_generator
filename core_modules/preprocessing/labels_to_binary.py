from skimage.morphology import disk
import skimage.morphology
import numpy as np

def get_channels(item_data, params):
    classes = item_data['classes']
    nb_classes = len(classes)

    skip_classes = None
    if ('skip_classes' in params):
        skip_classes = params['skip_classes']

    only_classes = None
    if ('only_classes' in params):
        only_classes = params['only_classes']

    channels = []
    for class_i in range(nb_classes):
        classname = classes[class_i]
        add_class = True
        if (only_classes is not None and classname not in only_classes):
            add_class = False
        if (skip_classes is not None and classname in skip_classes):
            add_class = False
        if (add_class):
            channels.append(class_i)

    return channels


def process(item_data, params):
    remove_borders = None
    if ('remove_borders' in params):
        remove_borders = params['remove_borders']

    name = '(:class) binarized'
    if ('name' in params):
        name = params['name']

    channels = get_channels(item_data, params)

    labels_np = item_data['labels']

    binary_np = labels_np[:,:,channels] > 0

    for i in channels:
        classname = item_data['classes'][i]
        item_data['y_names'].append(name.replace('(:class)', classname))

    if (remove_borders is not None):
        for i in range(len(channels)):
            borders_np = (skimage.morphology.dilation(labels_np[:,:,i], selem=disk(remove_borders)) - skimage.morphology.erosion(labels_np[:,:,i], selem=disk(remove_borders))) > 0
            binary_np[:,:,i] = np.logical_and(binary_np[:,:,i], np.logical_not(borders_np))

    item_data['y'].append(binary_np)