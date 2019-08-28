#pylint: disable=broad-except
'''
Created on Mar 14, 2019
@author: erik.kniaz
'''
import os
import pylint.lint

#used for local dry runs.
#runs against all python files in repo.
try:
    pylint.lint.Run(['--rcfile=python/.pylintrc', 'python'])
except Exception as error:
    pylint.lint.Run([os.getcwd()])
