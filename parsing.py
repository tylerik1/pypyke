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





def group_tags(logger):
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
        except OSError as e:
            print(e)
            print('Cannot access ' + path +'. Probably a permissions error')

        return path_list


    try:
        current = os.getcwd()
        dir_name = os.path.abspath(current)
        extension = ".py"

        #save the path to all the python files
        path_list = []
        path_list = find_files_in_folder(dir_name, path_list, extension, True)
        if os.path.join(current, "test_set_runner.py") in path_list:
            path_list.remove(os.path.join(current, "test_set_runner.py"))
        if os.path.join(current, "parsing.py") in path_list:
            path_list.remove(os.path.join(current, "parsing.py"))


    except Exception as e:
        logger.info("hit an exception while trying to save path to python files")
        logger.info(e)
        pass



    #parse each file and save each function and its decorators
    func_names = []
    tags = []
    for py_file in path_list:
        count = 0
        lines = open(py_file, encoding="utf8").readlines()
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
                        if 'architecture' in py_file:
                            func_names.append((str, (py_file.split('architecture')[1].replace('\\', ".").strip('.')[:-3], lines[save_line].replace("def ", "").replace(":\n", ""))))
                        if 'infrastructure' in py_file:
                            func_names.append((str, (py_file.split('infrastructure')[1].replace('\\', ".").strip('.')[:-3], lines[save_line].replace("def ", "").replace(":\n", ""))))

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


    #All tests that are marked with a tag will be added to the code coverage suite.
    tmp_code_coverage_list = []
    for function in func_names:
        #exclude tests marked bulk_parallel_process from code coverage suite
        if function[0] == 'bulk_parallel_process':
            continue
        tmp_code_coverage_list.append(function[1])
    test_list['code_coverage'] = set(tmp_code_coverage_list)

    return test_list









def get_functions(logger, function):
    '''
    Returns the file that which the function belongs to.  Does not return functions in helper files.
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
        except OSError as e:
            print(e)
            print('Cannot access ' + path +'. Probably a permissions error')

        return path_list


    try:
        current = os.getcwd()
        dir_name = os.path.abspath(current)
        extension = ".py"

        #save the path to all the python files
        path_list = []
        path_list = find_files_in_folder(dir_name, path_list, extension, True)
        if os.path.join(current, "test_set_runner.py") in path_list:
            path_list.remove(os.path.join(current, "test_set_runner.py"))
        if os.path.join(current, "parsing.py") in path_list:
            path_list.remove(os.path.join(current, "parsing.py"))


    except Exception as e:
        logger.info("hit an exception while trying to save path to python files")
        logger.info(e)
        pass

    func_names = []
    for py_file in path_list:
        lines = open(py_file, encoding="utf8").readlines()
        for line in lines:
            if 'def ' in line:
                if 'architecture' in py_file:
                    func_names.append(((py_file.split('architecture')[1].replace('\\', ".").strip('.')[:-3], line.replace("def ", "").replace(":\n", ""))))
                if 'infrastructure' in py_file:
                    func_names.append(
                        ((py_file.split('infrastructure')[1].replace('\\', ".").strip('.')[:-3], line.replace("def ", "").replace(":\n", ""))))


    for func in func_names:
        if function+'(' in func[1]:
            if '_helpers' in func[0]:
                continue
            return func[0].split('.')[1] + '.' + function



    logger.info('Unable to locate file for function: ' + function)
    logger.info('Check to make sure the function is spelled correctly.')

    return False




