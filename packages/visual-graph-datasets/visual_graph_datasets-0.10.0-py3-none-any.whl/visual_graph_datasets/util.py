import json
import os
import pathlib
import logging
import difflib
import subprocess
import importlib.util
import typing as t

import click
import jinja2 as j2
import numpy as np

from visual_graph_datasets.config import HOME_PATH, FOLDER_PATH, CONFIG_PATH
from visual_graph_datasets.config import Config

PATH = pathlib.Path(__file__).parent.absolute()
TEMPLATES_PATH = os.path.join(PATH, 'templates')
TEMPLATE_ENV = j2.Environment(
    loader=j2.FileSystemLoader(TEMPLATES_PATH)
)
TEMPLATE_ENV.globals.update({
    'os': os
})

VERSION_PATH = os.path.join(PATH, 'VERSION')

NULL_LOGGER = logging.Logger('null')
NULL_LOGGER.addHandler(logging.NullHandler())


def get_version() -> str:
    """
    Reads the version file and returns the version string in the format "MAJOR.MINOR.PATCH"

    :return: the version string
    """
    with open(VERSION_PATH, mode='r') as file:
        content = file.read()

    version_string = content.replace(' ', '').replace('\n', '')
    return version_string


def dynamic_import(module_path: str, name: str = 'module'):
    """
    Given an absolute path ``module_path`` to a python module, this function will dynamically import that
    module and return the module object, which can be used to access the contents of that module.

    :param str module_path: The absolute path to the module to be imported
    :param str name: The string name to be assigned to that module

    :returns: The module object
    """
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def get_dataset_path(dataset_name: str, datasets_path=Config().get_datasets_path()) -> str:
    """
    Returns the absolute path to the dataset folder identified by the given ``dataset_name``

    :param dataset_name: The string name of the dataset whose absolute folder path is to be retrieved
    :return: The absolute folder path of the dataset
    """
    if not os.path.exists(datasets_path):
        raise FileNotFoundError(f'The datasets root folder does not yet exist. This indicates that no '
                                f'datasets have been downloaded yet or that the wrong root path is '
                                f'configured.')

    dataset_path = os.path.join(datasets_path, dataset_name)

    # The primary value of this function is supposed to be that we immediately check if this datasets even
    # exists and then raise an error instead of that happening at some other point in the user code.
    if not os.path.exists(dataset_path):
        dataset_names: t.List[str] = os.listdir(datasets_path)
        similarities = [(name, difflib.SequenceMatcher(None, dataset_name, name).ratio())
                        for name in dataset_names]
        similarities = sorted(similarities, key=lambda tupl: tupl[1], reverse=True)
        raise FileNotFoundError(f'There is no dataset of the name "{dataset_name}" in the root dataset '
                                f'folder "{datasets_path}"! '
                                f'Did you mean: "{similarities[0][0]}"?')

    return dataset_path


def merge_optional_lists(*args) -> t.List[t.Any]:
    """
    Given a list of arguments, this function will merge all the arguments which are of the type "list" and
    will simply ignore all other arguments, including None values.

    :param args:
    :return: the merged list
    """
    merged = []
    for arg in args:
        if isinstance(arg, list):
            merged += arg

    return merged


def merge_nested_dicts(original: dict, update: dict) -> dict:
    """
    Merges the new values of the ``update`` dict into the ``original`` dict in a nested manner.

    That means that the merge is executed separately for all nested sub dictionary structures with
    the same key. If a key does not exist in the original dict but in the update, the key is added to the
    original as is. If the update has a non-dict value where the original has a dict value at the same key,
    the original version is overwritten with the update version.

    Note: Does not perform copies! Updating of mutable objects may result in references being shared by the
    two input dictionaries in the end.

    :param original: The original dict to be modified
    :param update: the update dict containing the new values to be added to the original.

    :returns: the merged version of the original dict
    """
    for key, value in update.items():

        if key in original:
            if isinstance(original[key], dict) and isinstance(update[key], dict):
                merge_nested_dicts(original[key], update[key])
            else:
                original[key] = value

        else:
            original[key] = value

    return original


def ensure_folder(path: str) -> None:
    # This is probably the easiest if we do a recursive approach...

    parent_path = os.path.dirname(path)
    # If the path exists then that's nice and we don't need to do anything at all
    if os.path.exists(path):
        return
    # This is the base case of the recursion: The immediate parent folder exists but the given path does
    # not, which means to fix this we can simply create a new folder
    elif not os.path.exists(path) and os.path.exists(parent_path):
        os.mkdir(path)
    # Otherwise more of the nested structure does not exist yet and we enter the recursion
    else:
        ensure_folder(parent_path)
        os.mkdir(path)


# https://stackoverflow.com/questions/434597
def open_editor(path: str, config=Config()):

    platform_id = config.get_platform()
    if platform_id == 'Darwin':
        subprocess.run(['open', path], check=True)
    elif platform_id == 'Windows':
        os.startfile(path)
    else:
        subprocess.run(['xdg-open', path], check=True)


def sanitize_input(string: str):
    return string.lower().replace('\n', '').replace(' ', '')


# == CUSTOM JINJA FILTERS ==

def j2_filter_bold(value: str):
    return click.style(value, bold=True)


def j2_filter_fg(value: str, color: str):
    return click.style(value, fg=color)


TEMPLATE_ENV.filters['bold'] = j2_filter_bold
TEMPLATE_ENV.filters['fg'] = j2_filter_fg


# == COMMAND LINE UTILITIES ==
# The following sections deals with additional implementations for the "click" command line library
# which is used to implement the CLI in this project

class JsonListParamType(click.ParamType):

    name = 'json_list'

    def convert(self, value, param, ctx):
        if isinstance(value, list):
            return list

        # Given the value we will simply attempt to json decode it and if it does not work we know that
        # it is not a valid json string.
        try:
            loaded = json.loads(value)

            # Even if the conversion is successful, there is still the option that the actual content of
            # the string is not actually a list.
            if not isinstance(loaded, list):
                self.fail(f'The content of the given JSON string does not represent a list!')

            return loaded

        except Exception:
            self.fail(f'The given value is not a valid JSON string!')


JSON_LIST = JsonListParamType()


class JsonArrayParamType(JsonListParamType):

    name = 'json_array'

    def convert(self, value, param, ctx):
        if isinstance(value, np.ndarray):
            return value

        # The method of the parent class will completely deal with loading the json string as a list
        # already.
        loaded = super(JsonArrayParamType, self).convert(value, param, ctx)

        # Now we just need to try and convert it into a numpy array
        try:
            array = np.array(loaded)

            return array

        except Exception as e:
            self.fail(f'The given list cannot be loaded as a numpy array due to the following error: {exc}')


JSON_ARRAY = JsonArrayParamType()


class JsonDictParamType(click.ParamType):

    name = 'json_dict'

    def convert(self, value, param, ctx):
        if isinstance(value, dict):
            return value

        try:
            loaded = json.loads(value)

            # Even if the conversion is successful, there is still the option that the actual content of
            # the string is not actually a dict.
            if not isinstance(loaded, dict):
                self.fail(f'The content of the given JSON string does not represent a dictionary!')

            return loaded

        except Exception:
            self.fail(f'The given value is not a valid JSON string!')


JSON_DICT = JsonDictParamType
