#!/usr/bin/env python3

import json
from os import listdir
from os.path import isfile, join
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='labelme coco dataset normalizer')
parser.add_argument("-a", "--annotations", default="annotations")
parser.add_argument("-r", "--results-dir", help="where to write the updated annotations files", default="merged")
cmdline_args = parser.parse_args()

results_dir = cmdline_args.results_dir

Path(results_dir).mkdir(parents=True, exist_ok=True)

dirs = listdir( cmdline_args.annotations )

afiles = [f for f in dirs if isfile(join(cmdline_args.annotations, f))]

print(afiles)

examples_dict = { }

# make dict of annotations files
for fname in afiles:
    if not fname.endswith(".json"):
        continue
    print(f'adding {fname}')
    with open(join(cmdline_args.annotations, fname), 'r') as f:
        examples_dict[fname] = json.load(f)
        
def findAllCategories(edict):
    allcats = set()
    for (fname, dataset) in edict.items():
        categories = dataset['categories']
        for c in categories:
            #{"supercategory": "chair", "id": 1, "name": "chair"}
            id = c['id']
            name = c['name']
            allcats.add(name)
    return allcats
            
all_categories = sorted(list(findAllCategories(examples_dict)))
#{'standing', 'face', 'head', 'chair', 'head-of-bed', 'sitting-up', 'foot-of-bed', 'sit-lie-transition', 'falling', 'fallen', 'lying-down', 'sitting-on-edge-of-bed', 'sitting', 'bed', 'lamp', 'getting-up', 'dresser', 'wheelchair', 'fan', 'stand-sit-transition'}

categories_index = dict(zip(all_categories, range(1,len(all_categories)+1)))

master_categories_list = [ ]
for (name, index) in categories_index.items():
    master_categories_list.append({"supercategory": name, "name": name, "id": index})

print(categories_index)

def remapCategory(c):
    return categories_index[c]

# mutates the annotations objects to renumber the categories
def renumberCategories(afpath, outpath):
    with open(afpath, 'r') as f:
        if not afpath.endswith(".json"):
            return
        print(f'renumberCategories loading {afpath}')
        dataset = json.load(f)
    categories = dataset['categories']
    remappings = {}
    for c in categories:
        #{"supercategory": "chair", "id": 1, "name": "chair"}
        id = c['id']
        name = c['name']
        newid = remapCategory(name)
        remappings[id] = newid
        c['id'] = newid
    print('remappings = ', remappings)
    dataset['categories'] = master_categories_list
    for a in dataset['annotations']:
        a['category_id'] = remappings[a['category_id']]
    with open(outpath, 'w') as out:
        json.dump(dataset,out)

tasks = []
datasets  = []
for filename in afiles:
    inpath = join(cmdline_args.annotations, filename)
    outpath = join(results_dir, filename)
    print(f"remapping {inpath} to {outpath}")
    renumberCategories(inpath, outpath)
    fprefix = filename.replace('.json', '')
    fname = filename
    datasets.append(f"register_coco_instances('task-{fprefix}', {{}}, WORKDIR+'/annotations/{fname}', WORKDIR+'/images/{fprefix}')")
    tasks.append(f'task-{fprefix}')

# list detectron dataset declarations
print('\n'.join(sorted(datasets)))

train_str = "cfg.DATASETS.TRAIN = ("
for task in sorted(tasks):
    train_str += f"'{task}',"
train_str += ")"
print(train_str)



