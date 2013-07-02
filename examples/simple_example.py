#!/usr/bin/env python
"""simple ascar parallel example.

Usage:
    simple_example.py [-n <ncpu>]

Options:
    -h --help   Show this screen
    -n          Number of cpu's to use. Default is max cpu - 1 on local or 64 on ascar
"""

from docopt import docopt
from ascar_parallel import StartCluster
from IPython.parallel import depend
from time import time

def myfunc(a,b):
    from time import sleep
    sleep(2)
    return a + b


if __name__ == '__main__':
    arguments = docopt(__doc__)

    ncpu = None
    if arguments['-n']:
        ncpu = arguments['<ncpu>']

    a = range(10)
    b = range(10)

    print 'Starting Serial Run -----------------------------'
    start = time()
    serial_result = map(myfunc, a, b)
    serial_time = time() - start

    parallel_result = None
    start = time()
    with StartCluster(ncpu) as lview:
        parallel_result = lview.map(myfunc, a, b)
    parallel_time = time() - start

    if serial_result == parallel_result:
        print 'serial_time = %s' % serial_time
        print 'parallel_time = %s' % parallel_time
        print 'Note: parallel_time includes time to start up and stop cluster'
    else:
        print 'results do not match'