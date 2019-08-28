#pylint: disable=bare-except,invalid-name
'''
Created on Feb 28, 2019

@author: erik.kniaz
'''

import functools
import os
import ntpath


class TagDecorator():
    '''
    Class to create tags
    '''

    def __init__(self, tag_name):
        self.functions = []
        self.tag_name = tag_name

    def __str__(self):
        return "<TagDecorator {tag_name}>".format(tag_name=self.tag_name)

    def __call__(self, funtion):
        self.functions.append(funtion)
        return funtion

    def invoke(self, *args, **kwargs):
        '''
        runs the functions locally
        '''
        return [f(*args, **kwargs) for f in self.functions]




@functools.lru_cache(maxsize=None)  # memoization
def get_func_tag(tag_name):
    '''
    initalizes the tag name
    '''
    return TagDecorator(tag_name)




#List of tag names
smoke = get_func_tag('smoke')
unit = get_func_tag("unit")
functional = get_func_tag("functional")
regression = get_func_tag("regression")



def group_tags():
    '''
    Groups all decorators of the same tag name into test sets.
    '''

    def find_files_in_folder(path, path_list, extension, sub_folders=True):
        '''
        Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)

        path:        Base directory to find files
        pathList:    A list that stores all paths
        extension:   File extension to find
        subFolders:  Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder
        '''

        try:   # Trapping a OSError:  File permissions problem I believe
            for entry in os.scandir(path):
                if entry.is_file() and entry.path.endswith(extension):
                    path_list.append(entry.path)
                elif entry.is_dir() and sub_folders:   # if its a directory, then repeat process as a nested function
                    path_list = find_files_in_folder(entry.path, path_list, extension, sub_folders)
        except OSError:
            print('Cannot access ' + path +'. Probably a permissions error')

        return path_list


    try:
        current = os.getcwd()
        dir_name = os.path.abspath(current)
        extension = ".py"

        #save the path to all the python files
        path_list = []
        path_list = find_files_in_folder(dir_name, path_list, extension, True)
        path_list.remove(os.path.join(current, "decorators.py"))
        path_list.remove(os.path.join(current, "test_set_runner.py"))
    except:
        dir_name = r'pypyke'
        extension = ".py"

        #save the path to all the python files
        path_list = []
        path_list = find_files_in_folder(dir_name, path_list, extension, True)


    #parse each file and save each function and its decorators
    tags = ["@smoke", "@unit", "@functional", "@regression"]
    func_names = []
    for py_file in path_list:
        count = 0
        lines = open(py_file).readlines()
        for line in lines:
            count += 1
            for tag in tags:
                if tag in line:
                    index = count
                    while "@" in lines[index]:
                        index += 1
                    save_line = index
                    if "def" in lines[save_line]:
                        func_names.append((tag, (ntpath.basename(py_file)[:-3], lines[save_line].replace("def ", "").replace(":\n", ""))))

    func_names = list(set(func_names))

    #move each function into a test set to be run
    smoke_tests = []
    unit_tests = []
    functional_tests = []
    regression_tests = []

    for function in func_names:
        if function[0] == "@smoke":
            smoke_tests.append(function[1])
        elif function[0] == "@unit":
            unit_tests.append(function[1])
        elif function[0] == "@functional":
            functional_tests.append(function[1])
        elif function[0] == "@regression":
            regression_tests.append(function[1])

    return smoke_tests, unit_tests, functional_tests, regression_tests
