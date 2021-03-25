# cocoutil
Some simple coco dataset manipulation utilities

# unify-categories.py
If you have several COCO format datasets which have different sets of  category labels and id numbers, this renumbers the category id numbers and
writes new annotation.json files so you can train with the datasets in a framework like Detectron2. 

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

