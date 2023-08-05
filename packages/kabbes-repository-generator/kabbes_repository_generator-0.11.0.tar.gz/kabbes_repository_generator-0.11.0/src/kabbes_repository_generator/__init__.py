import os
import dir_ops as do

_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 

from .RepositoryGenerator import RepositoryGenerator
from .Client import Client
