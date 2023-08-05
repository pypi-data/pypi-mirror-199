# filesystem_autocomplete

[![PyPI](https://img.shields.io/pypi/v/filesystem_autocomplete.svg?color=green)](https://pypi.org/project/filesystem_autocomplete)

![tests](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)

[![codecov](https://codecov.io/gh/chrishavlin/filesystem_autocomplete/branch/main/graph/badge.svg)](https://codecov.io/gh/chrishavlin/filesystem_autocomplete)

utility for recursively mapping files and subdirectories 

To use, import `walk_directory` then supply a starting directory:

```python 
>>> from filesystem_autocomplete import walk_directory
>>> dir_info = walk_directory(".")
```

The resulting object will contain attributes for all files and subdirectories. 

From a python shell or jupyter notebook, you can explore the file system using 
autocomplete. When evaluating, files will print their full path:

```
>>> dir_info.filesystem_autocomplete.filesystem_autocomplete_py
/home/chavlin/src/dxl/filesystem_autocomplete/filesystem_autocomplete/filesystem_autocomplete.py
```

directories will print their contents:

```
>>> dir_info.filesystem_autocomplete
Directory: /home/chavlin/src/dxl/filesystem_autocomplete/filesystem_autocomplete

Files:
__init__.py
filesystem_autocomplete.py

Subdirectories:
__pycache__
tests
```

To extract the full path for files: 
```
>>> dir_info.filesystem_autocomplete.filesystem_autocomplete_py.filepath
'/home/chavlin/src/dxl/filesystem_autocomplete/filesystem_autocomplete/filesystem_autocomplete.py'
```

and for directories:
```
>>> dir_info.filesystem_autocomplete.dirpath
'/home/chavlin/src/dxl/filesystem_autocomplete/filesystem_autocomplete'
```

## handling special characters

Since files and directories are stored as attributes, any invalid characters are 
replaced with underscores in the object. The full path string contains the original 
file.
