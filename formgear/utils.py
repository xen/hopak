import sys
import logging
import os.path
import re


def find_yaml(yaml_list, dirname, names):
    """
    Callback for `yamls_files` function
    dirname - current directory name, that `yamls_files` walks
    names - list of dirs and files in the `dirname` directory
    yaml_list - accumulator from caller of callback function, 
                in this variable we agrigrate obtained files 
    """
    for name in names:
        path_to_file = os.path.join(dirname, name)
        if os.path.isfile(path_to_file):
            if ".yaml" in name:
                yaml_list[re.sub("\.yaml", "", name, 1)] = path_to_file


def yamls_files():
    """
    Searching yaml files in sys.path.
    Return the dict like:
        {'yourfilename' : '/absolute/path/to/your/yourfilename.yaml'
         ...
         ...
        }
    """
    yaml_list = {}
    for cur_path in sys.path:
        os.path.walk(cur_path, find_yaml, yaml_list)

    logging.info("obtained yaml files %r" % (yaml_list,))
    return yaml_list
