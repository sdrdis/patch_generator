import os
from os.path import join, isfile


def group_by_item(path, params):
    folders = params['folders']
    images_folder = folders['image']
    items = {}
    for filename in os.listdir(join(path, images_folder)):
        if (filename not in items):
            items[filename] = {}
        for file_type in folders:
            items[filename][file_type] = join(folders[file_type], filename)

    return items
