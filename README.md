# cocoutil
Some simple coco dataset manipulation utilities

# unify-categories.py
If you have several COCO format datasets which have different sets of  category labels and id numbers, this finds all common category names and renumbers the category id numbers in each file to be consistent, as well as having the same number of categories as every other annotation file. 

Writes new copies of the annotation.json files with categories renumbered to a common standard and same number of categories in each file,  to the output directory so you can train with the datasets in a framework like Detectron2. 

Args are:

--annotations The directory with COCO annotations.json files
--results-dir  Where to write the new copies of (renumbered) annotations.json files

Usage:
```bash
python unify-categories.py  --help
usage: unify-categories.py [-h] [-a ANNOTATIONS] [-r RESULTS_DIR]

labelme coco dataset normalizer

optional arguments:
  -h, --help            show this help message and exit
  -a ANNOTATIONS, --annotations ANNOTATIONS
  -r RESULTS_DIR, --results-dir RESULTS_DIR
                        where to write the updated annotations files
                     
```

