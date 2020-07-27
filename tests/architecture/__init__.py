'''
Created on Apr 1, 2019

@author: erik.kniaz
'''
import os
import pkgutil
from tests.architecture.add_to_cart import *
from tests.architecture.credit_card import *

__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
