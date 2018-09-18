# The patch_generator utility

## In short

Python framework that allows you to generate patches from images and apply on them various data augmentation techniques. The framework emphasis is extendability: every part of the process can be redefined by the user. The generated patches can be then be easily used for machine learning and deep learning endeavours, such as image classification, semantic segmentation and so on.

## How to install

You must have installed python 3.6 and pip.

1. Download the framework by cloning this github project or by clicking here
2. Install dependencies writen in the `requirement.txt` file manually or by running `pip install -r requirements.txt` in the shell.

## General process

The patch_generator utility takes as input a folder containing images and labels and outputs extracted patches in another folder.

The input folder should separate the samples into subfolders (training, validation, test…). An example of structure is:

- Training 
    - im_1.png 
    - mask_1.png 
    - im_2.png 
    - mask_2.png 
    - …
- Validation 
    - …
- Test 
    - … 

The generated folder will also contain these subfolders and patches will be placed to the corresponding subfolder of the images they are extracted from.

The process can be separated into 4 steps:
1. Group by item: it allows users to specify the file organization by indicating how to group files by items. For instance, each item can consist of an image and a json file with instances locations. Another way of organizing each item is to have an image, a semantic image, an instance image.
2. Load item: for each item, it loads the file paths grouped by the previous step. One of the main product is a 3D matrix of size (w, h, c), w being the width of the image, h being the height of the image, and c being the number of classes. Each element of the matrix will be a boolean (for semantic segmentation) or a number (for instance segmentation). 
3. Preprocessings: Indicates how to preprocess each item before dividing it into patches. For instance, images and labels can be resized on this step. 
4. Generate patches: Indicates how to divide an image into different patches. 
5. Post processings: Indicates how to post-process each patch (allowing to apply data augmentation techniques on them).


This entire process can be entirely customized using a configuration file that we will describe now.

A single script exists for generating the patches : “generate.py”. When calling this script, the user must indicate as a parameter a json configuration file. For instance:

`python generate.py configs/config.json`

This configuration file indicates the input folder, the output folder and describes how to execute all steps described earlier.

The minimum configuration file only needs three keys:

  
```
{
  "default": "semantic_segmentation",
  "path": "@path_1",
  "path_patches": "@path_2",
}
```
  

The default key indicates the default configuration file. The default configuration file defines all default values, and these default values are extended by the defined configuration file. Here, the semantic_segmentation value indicates that the default configuration file is located at `default_configs/semantic_segmentation.json`.

The path key defines where the input folder is. The path_patches key indicates in which folder the patches must be generated.

In order to have an overview of all available keys, we can take a look at the default configuration file located at default_configs/semantic_segmentation.json:

```
{
  "nb_threads": 1,
  "skip_subfolders": [],
  "group_by_item": {
    "module": "core_modules.group_by_item.default"
  },
  "load_item": {
    "module": "core_modules.load_item.default"
  },
  "preprocessings": {
    "1_get_labels": {
      "module": "core_modules.preprocessing.labels_to_binary"
    },
    "2_format_y": {
      "module": "core_modules.preprocessing.merge_y"
    }
  },
  "generate_patches": {
    "module": "core_modules.generate_patches.default",
    "params": {
      "shape": [256, 256]
    }
  },
  "post_processings": {
    "1_random_rotation": {
      "module": "core_modules.post_processing.random_rotation"
    },
    "2_binarize": {
      "module": "core_modules.post_processing.binarize"
    }
  }
}
```
  

There are several defined keys:

- `nb_threads`: indicates the number of threads used for the patch generation. It can greatly accelerate the generation process but also use more resources.
- `skip_subfolders`: indicates which subfolders to skip in the input folder.
- `group_by_item`: indicates the module and parameters for the first step of the process. More details will be given later.
- `load_item`: indicates the module and parameters for the second step of the process. More details will be given later.
- `preprocessings`: indicates the different preprocessings applied on a item before dividing it into different patches. More details will be given later.
- `generate_patches`: indicates the module and parameters for the patch generation step. More details will be given later.
- `post_processing`: indicates the different post processings applied on a patch (allowing data augmentation for instance). More details will be given later.


When a configuration key expects a module, such as group_by_item or load_item, two subkeys can be defined:

- `module`: (mandatory) defines which python module to load (the path is written in a similar way than if it were imported from generate.py).
- `params`: (optional) indicates parameters passed to the module.
  

### The group_by_item key

The group_by_item key indicates how to group files by item. It will call the group_by_item method of the defined module:

- Parameters: 
    - `path`: subfolder path.
    - `params`: parameters passed to the module.

- Expected output: 
    - A dictionary of dictionaries. The structure of the dictionary is the following: dict[file_id][file_type] where file_id is a file identifier and file_type is the file type. The value is the name of the file. 

  

For instance, if an item has an image defined at image_1.png and its associated labels defined at labels_1.json, a possible generated dictionary is:

```
{
  "1": {
    "image": "image_1.png",
    "labels": "labels_1.json"
  }
}
```

There are 4 common keys (some are optionals, other could be defined depending on the use case):

- `image`: the image filename.
- `labels`: the labels filename: the file contains either semantic classes or semantic + instances classes.
- `instances`: the instances filename. If the labels file format contains only classes, instances ids can be added this way.
- `infos`: the additional information filename. Sometimes, additional information than images are available. They can be added through this key.

### The load_item key

The load_item key indicates how to load the files of each item. It will call the load_item method of the defined module:

- Parameters: 
    - `item_id`: ID of the item
    - `item`: informations given by group_by_item
    - `path`: subfolder path
    - `params`: parameters passed to the module

- Expected output: 
    - A dictionary with the following keys: 
        - `X`: contains the image
        - `complementary_X`: empty array, can be used to include complementary information.
        - `y`: empty array, must be filled during the preprocessing process to indicate what the learning target.
        - `y_names`: empty array, optional, used for identifying the different layers in y.
        - `labels`: 3D matrix of size (w, h, c), w being the width of the image, h being the height of the image, and c being the number of classes. Each element of the matrix will be a boolean (for semantic segmentation) or a number (for instance segmentation).
        - `classes`: if available, class names. Used for identifying different layers in labels.
        - `infos`: Additional information given by the infos file.
        - `ignore`: defaults to false. Can be modified later to true if the user wants to skip this sample during the generation.

### The preprocessing key

The preprocessing key allows apply preprocessing on the output given by load_item before the patch generation process.

It is a dictionary where each value is a module (and parameters) and each key has the form “NUM_TITLE”, NUM being a number (or float) and TITLE being a title for the preprocessing.

On the preprocessing step, each module will be executed from the key which has the lowest NUM to the one with the highest NUM. Such an organization allows to have preprocessing steps in the default configuration file but still being able to replace or add an additional preprocessing anywhere in the process.

For example, let’s say that default configuration file is as follows:

```
{
  ...
  "preprocessing": {
    "1_resize": {...},
    "2_add_label": {...}
  }
}
```

The user can replace the preprocessing defined on `1_resize` by adding a `1_resize` key in the preprocessing key of his configuration file. The preprocess can also be deleted by setting the value of `preprocessing.1_resize` to `null` in the configuration file.

The user can add a preprocessing before `1_resize` with by defining a key starting with 0: for instance `0_custom`. The user can add a preprocess between `1_resize` and `2_add_label` by adding a `1.5_custom` key for instance. The user can add a processing after `2_add_label` by adding a configuration key starting by a 3.

The process method of each specified module is called:

- Parameters: 
    - `item_data`: output of load_item
    - `params`: parameters passed to the module
- Output: 
    - `None`: the modules must directly modify item_data.

### The generate_patches key

This is where patches are generated. The method generate of the defined module is called:

- Parameters: 
    - `patch_i`: the current patch identifier
    - `item_data`: the data created by load_item and modified by the preprocessing methods.
    - `subfolder_patches_path`: the patch subfolder
    - `params`: parameters passed to the module
- Output: 
    - `patch_i`: the patch identifier after generating patches.

About `patch_i`: this variable is initialized at 0. The recommended way to use it is to increment it everytime a patch is generated.

### The post_processings key

The post_processing key allows apply post processing on the generated patches.

It is a dictionary containing different modules and it is organized in a similar way than the preprocessing key.

For example, let’s say that default configuration file is as follows:

The process method of each specified module is called:
- Parameters:ex_X, ex_y, ex_complementary_X, params
    - `ex_X`: The patch's image
    - `ex_y`: The patch's target
    - `ex_complementary_X`: The patch's complementary information
    - `params`: parameters passed to the module
- Output:
    - `ex_X`: The patch's post-processed image
    - `ex_y`: The patch's post-processed target
    - `ex_complementary_X`: The patch's post-processed complementary information