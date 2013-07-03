#!/usr/bin/env python
"""fortran ascar parallel example.

Usage:
    fortran_example.py <nfiles> [-n <ncpu>]

Options:
    -h --help   Show this screen
    <nfiles>    number of input files to create and run
    -n          Number of cpu's to use. Default is max cpu - 1 on local or 64 on ascar

    NOTE: you must compile fcount.f -> gfortran fcount.f -o fcount before this will work 
"""

from docopt import docopt
from ascar_parallel import StartCluster
from time import time
import numpy as np
import os
import shutil
from helperfn import runfortran

def runfortran(ndir, value, path, exe_path):
    import os
    import shutil
    from subprocess import Popen
    
    dirname = os.path.join(path, 'dir_%s' % ndir)
    os.makedirs(dirname)
    filename = os.path.join(dirname, 'fcount.in.txt')
    with open(filename, 'w') as f:
        f.write('%s' % value)
        
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


if __name__ == '__main__':
    if not os.path.isfile('fcount'):
        import sys
        print 'NOTE: you must compile fcount.f -> `gfortran fcount.f -o fcount` before this will work' 
        sys.exit()

    arguments = docopt(__doc__)
    
    ncpu = None
    if arguments['-n']:
        ncpu = arguments['<ncpu>']

    nfiles = int(arguments['<nfiles>'])

    abs_path = os.path.join(os.getcwd(), 'output')
    exe_path = os.path.join(os.getcwd(), 'fcount')
    #remove everything in path directory
    if os.path.isdir(abs_path):
        shutil.rmtree(abs_path)
    runs = range(nfiles)
    values = []
    serial_paths = []
    parallel_paths = []
    exe_paths = []

    for run in runs:
        values.append(int(np.random.random()*1000000000))
        serial_paths.append(os.path.join(abs_path, 'serial'))
        parallel_paths.append(os.path.join(abs_path, 'parallel'))
        exe_paths.append(exe_path)

    print 'Starting Serial Run -----------------------------'
    start = time()
    serial_result = map(runfortran, runs, values, serial_paths, exe_paths)
    serial_time = time() - start

    parallel_result = None
    start = time()
    with StartCluster(ncpu) as lview:
        parallel_result = lview.map(runfortran, runs, values, parallel_paths, exe_paths)
    parallel_time = time() - start

    if serial_result == parallel_result:
        print 'serial_time = %s' % serial_time
        print 'parallel_time = %s' % parallel_time
        print 'Note: parallel_time includes time to start up and stop cluster'
        print 'mean value of results is ', np.mean(parallel_result)
    else:
        print 'results do not match'
