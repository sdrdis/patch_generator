import common
import argparse
import os
from os.path import join, isdir, isfile
import threading
import time
import random
import sys

sys.path.append('.')


parser = argparse.ArgumentParser(description='Generate patches')
parser.add_argument('config_filepath', type=str, help='Configuration file')

args = parser.parse_args()

config = common.load_json(args.config_filepath)

if ('default' in config):
    default_filename = config['default']
    default_config = common.load_json(join('default_configs', default_filename + '.json'))
    config = common.dict_merge(config, default_config)

group_by_item_module = __import__(config['group_by_item']['module'], fromlist=[''])
group_by_item_module_params = common.get_params_module(config['group_by_item'])
load_item_module = __import__(config['load_item']['module'], fromlist=[''])
load_item_module_params = common.get_params_module(config['load_item'])
generate_patches_module = __import__(config['generate_patches']['module'], fromlist=[''])

preprocessing_modules, preprocessing_params = common.get_processes_list(config['preprocessings'])
postprocessing_modules, postprocessing_params = common.get_processes_list(config['post_processings'])

path_from = config['path']
path_patches = config['path_patches']
nb_threads = config['nb_threads']

all_items = []
for subfolder in os.listdir(path_from):
    if (subfolder in config['skip_subfolders']):
        continue
    subfolder_path = join(path_from, subfolder)
    subfolder_patches_path = join(path_patches, subfolder)
    if (not(isdir(subfolder_patches_path))):
        os.makedirs(subfolder_patches_path)

    if isdir(subfolder_path):
        print ('Processing subfolder:', subfolder)
        items = group_by_item_module.group_by_item(subfolder_path, group_by_item_module_params)
        for item in items:
            all_items.append([subfolder_path, subfolder_patches_path, item, items[item]])



class ProcessThread(threading.Thread):
    all_items = None
    item_i = 0

    def run(self):
        patch_i = 0
        while(ProcessThread.item_i < len(all_items)):
            time.sleep(random.uniform(0.25, 0.75))
            item_data = all_items[ProcessThread.item_i]
            ProcessThread.item_i += 1
            item = item_data[2]
            print('Processing item:', item, ProcessThread.item_i, '/', len(all_items))
            subfolder_path = item_data[0]
            subfolder_patches_path = item_data[1]
            item_infos = item_data[3]
            item_data = load_item_module.load_item(
                item,
                item_infos,
                subfolder_path,
                load_item_module_params
            )
            for i in range(len(preprocessing_modules)):
                preprocessing_module = preprocessing_modules[i]
                preprocessing_param = preprocessing_params[i]
                preprocessing_module.process(item_data, preprocessing_param)

            if (item_data['ignore']):
                continue

            patch_i = generate_patches_module.generate(
                patch_i,
                item_data,
                subfolder_patches_path,
                config['generate_patches']['params'],
                self.thread_id,
                postprocessing_modules,
                postprocessing_params
            )


ProcessThread.all_items = all_items
for i in range(config['nb_threads']):
    thread = ProcessThread(name = "Thread-{}".format(i))
    thread.thread_id = i
    if (config['nb_threads'] == 1):
        thread.run()
    else:
        thread.start()