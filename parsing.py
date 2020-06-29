#pylint: disable=bare-except,invalid-name
'''
Created on Feb 28, 2019

@author: erik.kniaz
'''

from functools import wraps
import os
import ntpath
import re

def tag(*args, **kwargs):
    """Decorator that adds attributes to classes or functions
    for use with the Attribute (-a) plugin.
    """
    def wrap_ob(ob):
        for name in args:
            setattr(ob, name, True)
        for name, value in kwargs:
            setattr(ob, name, value)
        return ob
    return wrap_ob





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
        path_list.remove(os.path.join(current, "parsing.py"))
    except:
        dir_name = r'pypyke'
        extension = ".py"

        #save the path to all the python files
        path_list = []
        path_list = find_files_in_folder(dir_name, path_list, extension, True)


    #parse each file and save each function and its decorators
    func_names = []
    tags = []
    for py_file in path_list:
        count = 0
        lines = open(py_file).readlines()
        for line in lines:
            count += 1
            #if tag is commented out, skip it
            if "#@tag(" in line:
                continue
            if "@tag(" in line:
                index = count
                result = re.findall("'([^']*)'", line)
                if not result:
                    result = re.findall('"([^"]*)"', line)
                for str in result:
                    tags.append(str)
                    while "@" in lines[index]:
                        index += 1
                    save_line = index
                    if "def" in lines[save_line]:
                        #func_names.append((str, (ntpath.basename(py_file)[:-3], lines[save_line].replace("def ", "").replace(":\n", ""))))
                        func_names.append((str, (py_file.split('architecture')[1].replace('\\', ".").strip('.')[:-3], lines[save_line].replace("def ", "").replace(":\n", ""))))

    tag_set = list(set(tags))
    func_names = list(set(func_names))


    test_list = {}

    for i, tag in enumerate(tag_set):
        test_list[tag] = i

    for tag in tag_set:
        temp_list = []
        for function in func_names:
            if function[0] == tag:
                temp_list.append(function[1])
        test_list[tag] = temp_list

    return test_list