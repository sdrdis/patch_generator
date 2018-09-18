import scipy.misc
from os.path import join
import os.path
import json
import numpy as np
import skimage.draw

def get_image(image_path):
    return scipy.misc.imread(image_path)

def get_labels_image(labels_path):
    return scipy.misc.imread(labels_path), ['class']

def get_labels_json(labels_path, shape):
    with open(labels_path, 'r') as f:
        data = json.load(f)

    labels_np = np.zeros((shape[0], shape[1], len(data)), dtype='uint64')
    cls_i = -1
    classes = []
    for cls in data:
        classes.append(cls)
        cls_i += 1
        label_i = 0
        for instance in range(len(data[cls])):
            label_i += 1
            for group_coordinates in data[cls][instance]['coordinates']:
                r = []
                c = []
                for p in group_coordinates:
                    c.append(p[0])
                    r.append(p[1])
                r = np.array(r)
                c = np.array(c)

                rr, cc = skimage.draw.polygon(r, c, shape)
                labels_np[rr, cc, cls_i] = label_i
    return labels_np, classes

def get_labels(labels_path, shape):
    _, ext = os.path.splitext(labels_path)
    if (ext == '.json'):
        return get_labels_json(labels_path, shape)
    else:
        return get_labels_image(labels_path)

def load_item(item_id, item, path):
    image_path = join(path, item['image'])
    labels_path = join(path, item['labels'])

    im_np = get_image(image_path)
    labels_np, classes = get_labels(labels_path, im_np.shape)

    return {'X': im_np, 'y': [], 'y_names': [], 'labels': labels_np, 'classes': classes}