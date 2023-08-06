# shutil_extra
extra utils

# Build/Upload
```sh
# build
python setup.py sdist
# upload
twine upload ./dist/shutil_extra-x.x.x.tar.gz
```

# Usage

## dirtree
```python
from shutil_extra.dirtree import generate_dirtree

tree_cnf = f'''
folder1
    folder2_1,folder2_2
        folder3_1->folder4
        folder3_2->folder4->folder5_1,folder5_2
        folder3_3->folder4
        folder3_4->folder4
'''

# without post_handle
generate_dirtree('./folder_tree', tree_cnf)

# with post_handle
def post_handle(dirname, dirpath):
    # do something after dir generated
    if dirname == 'folder4':
        with open(os.path.join(dirpath, 'data.txt'), 'w') as f:
            f.writelines('hello world')

generate_dirtree('./folder_tree', tree_cnf, post_handle=post_handle)
```