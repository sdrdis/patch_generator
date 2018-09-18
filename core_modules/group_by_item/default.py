import os
from os.path import join, isfile
import re

def get_id_from_item(filename, filename_to_type):
    file_id = None
    sel_key = None
    for key in filename_to_type:
        if (sel_key is not None and len(key) <= len(sel_key)):
            continue
        m = re.search(key, filename)
        if (m is not None):
            file_id = m.group(1)
            sel_key = key

    if (sel_key is not None):
        file_type = filename_to_type[sel_key]
    else:
        raise Exception('No file type associed to filename ' + filename + '. Define this in the filename_to_type parameter key of group_by_item module.')

    return file_id, file_type

def group_by_item(path, params):
    if ('filename_to_type' not in params):
        params['filename_to_type'] = {
            "(.*).png": 'image',
            "(.*).jpg": 'image',
            "(.*).jpeg": 'image',
            "(.*).bmp": 'image',
            "(.*).tif": 'image',
            "(.*)_labels.png": 'labels',
            "(.*)_labels.tif": 'labels'
        }
    items = {}
    for filename in os.listdir(path):
        filepath = join(path, filename)
        if (isfile(filepath)):
            file_id, file_type = get_id_from_item(filename, params['filename_to_type'])
            if (file_id is None):
                continue
            if (file_id not in items):
                items[file_id] = {}

            items[file_id][file_type] = filename

    return items
