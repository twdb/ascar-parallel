import os
import shutil
import datetime
import platform
from subprocess import Popen
from multiprocessing import cpu_count
from time import sleep
from IPython.parallel import Client

ASCAR_DEFAULT_NCPUS = 64

class StartCluster():
    def __init__(self, n_cpus, imports=None):
        self.n_cpus = n_cpus
        self.imports = imports

    def __enter__(self):
        "Start IPython Parallel Engines"
        # Check if we are on the cluster Ascar
        if platform.uname()[1].split('.')[0] == 'ascar':
            #start SGE cluster
            if not self.n_cpus:
                self.n_cpus = ASCAR_DEFAULT_NCPUS

            cluster_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

            print 'Starting parallel engine and clients on Ascar with ' + str(self.n_cpus) + ' cpus'
            print 'cluster-id = ',cluster_id
            p1 = Popen(['ipcluster', 'start', '--profile=sge', '--cluster-id=' + cluster_id, '-n ' + str(self.n_cpus), '--daemonize'])

            #need to wait till engines are started and connection file is created.
            print '... checking for connection file: '
            while not self._cluster_started(cluster_id):
                print '... waiting for 5 secs for parallel engines to start'
                sleep(5)

            rc = Client(profile='sge', cluster_id=cluster_id)
            self.cluster_id = cluster_id
            self.pwd = os.getcwd()

        else:
            #start local multicore cluster
            if not self.n_cpus:
                self.n_cpus = cpu_count() - 1 #windows doesn't behave well if you use all available cpus

            print 'Starting parallel engine and clients on localhost with ' + str(self.n_cpus) + ' cpus'
            p1 = Popen(['ipcluster', 'start', '-n ' + str(self.n_cpus), '--daemonize'])
            print '... waiting for 5 secs to ensure that all engines are available'
            sleep(5)
            rc = Client()

        lview = rc.load_balanced_view()
        lview.block = True

        return lview


    def __exit__(self, type, value, traceback):
        "Shut down cluster and cleanup temp files once program is complete"
        print 'Shutting down parallel engines'
        # close parallel engine
        if platform.uname()[1].split('.')[0] == 'ascar':
            p1 = Popen(['ipcluster', 'stop', '--profile=sge', '--cluster-id=' + self.cluster_id])
            print 'Cleaning up temp files'
            os.remove(self.connection_files[0])
            os.remove(self.connection_files[1])
            os.remove(os.path.join(self.pwd, 'sge_controller'))
            os.remove(os.path.join(self.pwd, 'sge_engines'))
        else:
            p2 = Popen(['ipcluster', 'stop'])


    def _cluster_started(self, cluster_id):
        home_dir = os.path.expanduser('~')
        started = False
        self.connection_files = [home_dir + '/.config/ipython/profile_sge/security/ipcontroller-' + cluster_id + '-client.json',
                                 home_dir + '/.config/ipython/profile_sge/security/ipcontroller-' + cluster_id + '-engine.json',
            ]
        if os.path.isfile(self.connection_files[0]):
            if os.path.isfile(self.connection_files[1]):
                started = True

        return started


