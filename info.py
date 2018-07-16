import argparse
import json
import os
import re
import sys
import yaml


def get_args():

    parser = argparse.ArgumentParser(
        usage='\n%(prog)s [options] file'
              '\n%(prog)s (-h | --help)')
    parser.add_argument("-j", "--json", action='store_true', default=False,
                        dest='boolean_j', help='Output to a json file')
    parser.add_argument("-y", "--yaml", action='store_true', default=False,
                        dest='boolean_y', help='Output to a yaml file')
    parser.add_argument(metavar='file', type=str,
                        dest='file', help='Filename')
    args = parser.parse_args()

    return args


def get_version():
    return sys.version.split(" ")[0]


def get_aliases():
    virt_env_all = os.popen('pyenv versions'
                            ' --bare').read().strip().split("\n")
    virt_env = os.popen('pyenv versions'
                        ' --bare --skip-aliases').read().strip().split("\n")
    list_aliases = []
    for i in virt_env_all:
        if i not in virt_env:
            list_aliases.append(i)
    return list_aliases


def get_versions():
    return os.popen('pyenv versions'
                    ' --bare --skip-aliases').read().strip().split("\n")


def get_virt_env():
    try:
        result = os.environ['VIRTUAL_ENV']
    except KeyError:
        result = "A virtual environment isn't used"
    return result


def get_virt_envs():
    virt_envs = os.popen('pyenv versions'
                        ' --bare --skip-aliases').read().strip().split("\n")
    pyenv = os.popen('whereis pyenv').read().strip()
    m = re.search("(^|\s)(\S*)bin\/pyenv", pyenv)
    pyenv_path = m.group(2) + "versions/"
    result_list = list(filter(lambda x: re.match(".*envs.*", x), virt_envs))
    return [pyenv_path + i for i in result_list]


def get_executable():
    return sys.executable


def get_pip_location():
    return os.popen('which pip').read().strip()


def get_python_path():
    return os.popen('echo $PYTHONPATH').read().strip()


def get_installed_modules():
    dict_modules = {}
    list_output = os.popen('pip freeze').read().strip().split("\n")
    for i in list_output:
        k, v = i.split("==")[0], i.split("==")[1]
        dict_modules[k] = v
    return dict_modules


def get_site_location():
    return sys.path[-1]


def write_to_json(data, filename):
    with open(filename + ".json", 'w') as outfile:
        json.dump(data, outfile)


def write_to_yaml(data, filename):
    with open(filename + ".yaml", 'w') as outfile:
        yaml.dump(json.loads(json.dumps(data)),
                  outfile, default_flow_style=False)


def process():
    result_dict = {
    "version": get_version(),
    "aliases": get_aliases(),
    "all_versions": get_versions(),
    "virt_env": get_virt_env(),
    "virt_envs": get_virt_envs(),
    "executable": get_executable(),
    "pip_location": get_pip_location(),
    "python_path": get_python_path(),
    "inst_modules": get_installed_modules(),
    "site_location": get_site_location()
    }
    args = get_args()
    dict_func = {
        write_to_json: args.boolean_j,
        write_to_yaml: args.boolean_y
    }
    for k, v in dict_func.items():
        if v:
            k(result_dict, args.file)


process()
