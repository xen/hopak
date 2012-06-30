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


def find_widget_template(widget_path_list, dirname, names):
    if os.path.isdir(dirname) and dirname.endswith("widgets"):
        widget_path_list.append(dirname)


def widgets_path():

    widget_path_list = []
    for cur_path in sys.path:
        os.path.walk(cur_path, find_widget_template, widget_path_list)
    return widget_path_list


def file_resolve(field, name, ypath):
    choicesf = field.get(name, None)

    if choicesf is None:
        return

    if not (isinstance(choicesf, basestring) and \
        choicesf.startswith("@")):
        return

    # try to open csv file
    choices_file = open(os.path.join(os.path.dirname(ypath), choicesf[1:]))
    choices = []
    for line in choices_file:
        line = line.decode("utf-8")
        key, val = line.split("\t", 1)
        choices.append((key, val))

    field[name] = choices

def form_dict(form):
    ret = {}
    for key, val in form:
        container = ret
        while '__' in key:
            ckey, key = key.split('__', 1)
            if ckey.isdigit():
                ckey = int(ckey)
            _container = container.get(ckey, {})
            container[ckey] = _container
            container = _container

        container[key] = val

    return ret

