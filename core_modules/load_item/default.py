import scipy.misc
from os.path import join
import os.path
import json
import numpy as np

def get_image(image_path):
    return scipy.misc.imread(image_path)

def get_labels(labels_path, instances_path, params):
    from_class_i = None
    to_class_i = None
    classes_names = None
    classes = None
    if ('from_class_i' in params):
        from_class_i = params['from_class_i']
    if ('to_class_i' in params):
        to_class_i = params['to_class_i']
    if ('classes' in params):
        classes = params['classes']
    if ('classes_names' in params):
        class_names = params['classes_names']

    sem_np = scipy.misc.imread(labels_path)
    if (from_class_i is None):
        from_class_i = sem_np.min()
    if (to_class_i is None):
        to_class_i = sem_np.max()

    if (classes is None):
        classes = np.arange(from_class_i, to_class_i + 1)
    else:
        classes = np.array(classes)

    if (classes_names is None):
        classes_names = classes.astype('str')

    labels_np = np.zeros((sem_np.shape[0], sem_np.shape[1], classes.shape[0]), dtype='bool')

    cls_i = 0
    for cls in classes:
        labels_np[:,:,cls_i] = sem_np == cls
        cls_i += 1

    if (instances_path is None):
        return labels_np, classes_names
    else:
        ins_np = scipy.misc.imread(instances_path)
        labels_np = labels_np.astype('uint64')
        labels_np *= ins_np[:,:,np.newaxis].astype('uint64')
        return labels_np, classes_names

def load_item(item_id, item, path, params):


    image_path = join(path, item['image'])
    labels_path = join(path, item['labels'])
    instances_path = None
    if ('instances' in item):
        instances_path = join(path, item['instances'])
    infos = None
    if ('infos' in item):
        with open(join(path, item['infos']), 'r') as f:
            infos = json.load(f)


    im_np = get_image(image_path)
    labels_np, classes = get_labels(labels_path, instances_path, params)

    if (len(labels_np.shape) > 2):
        if (np.min(np.min(labels_np, 2) == np.max(labels_np, 2))):
            labels_np = labels_np[:,:,0:1]

    return {'X': im_np, 'complementary_X': {}, 'y': [], 'y_names': [], 'labels': labels_np, 'classes': classes, 'infos': infos, 'ignore': False}