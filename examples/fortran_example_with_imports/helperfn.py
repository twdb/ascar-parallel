"""
Extra helper functions for fortran example.
This file needs to be in the same folder as the fortran_example_with_imports.py 

OR This needs to be made into a module and installed 
"""
import os
import shutil
from subprocess import Popen


def create_input(path, ndir, value):
    """
    Create n random input files in diff directories
    """
    dirname = os.path.join(path, 'dir_%s' % ndir)
    os.makedirs(dirname)
    filename = os.path.join(dirname, 'fcount.in.txt')
    with open(filename, 'w') as f:
        f.write('%s' % value)
        
    return dirname


def runfortran(ndir, value, path, exe_path):
    
    dirname = create_input(path, ndir, value)
    os.makedirs(dirname)
        
    pwd = os.getcwd()
    shutil.copy(exe_path, os.path.join(dirname, 'fcount'))
    os.chdir(dirname)
    p = Popen('./fcount').wait()
    os.chdir(pwd)

    filename = os.path.join(dirname, 'fcount.out.txt')
    result = None
    with open(filename) as f:
        result = float(f.read().split()[-1])

    return result

