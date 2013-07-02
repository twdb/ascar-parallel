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
    def __init__(self, n_cpus):
        self.n_cpus = n_cpus

    def __enter__(self):
        "Start IPython Parallel Engines"
        print 'test'
        # Check if we are on the cluster Ascar
        if platform.uname()[1].split('.')[0] == 'ascar':
            #start SGE cluster
            if not self.n_cpus:
                self.n_cpus = ASCAR_DEFAULT_NCPUS

            cluster_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            print 'Starting parallel engine and clients on Ascar with ' + str(self.n_cpus) + ' cpus'
            p1 = Popen(['ipcluster', 'start', '--profile=sge', '--cluster-id=' + cluster_id, '-n ' + str(self.n_cpus), '--daemonize'])

            #need to wait till engines are started and connection file is created.
            home_dir = os.path.expanduser('~')
            connection_file = home_dir + '/.config/ipython/profile_sge/security/ipcontroller-' + cluster_id + '-client.json'
            print '... checking for connection file: ', connection_file
            while not os.path.isfile(connection_file):
                print '... waiting for 5 secs for parallel engines to start'
                sleep(5)

            parallel_client = Client(profile=profile_name)
            self.cluster_id = cluster_id
            self.connection_file = connection_file

        else:
            #start local multicore cluster
            if not self.n_cpus:
                self.n_cpus = cpu_count() - 1 #windows doesn't behave well if you use all available cpus

            print 'Starting parallel engine and clients on localhost with ' + str(self.n_cpus) + ' cpus'
            #p1 = Popen(['ipcluster', 'start', '-n ' + str(self.n_cpus)])
            p1 = Popen(['ipcluster', 'start', '-n ' + str(self.n_cpus), '--daemonize'])
            print '... waiting for 5 secs to ensure that all engines are available'
            sleep(5)
            parallel_client = Client()

        lview = parallel_client.load_balanced_view()
        lview.block = True

        return lview

    def __exit__(self, type, value, traceback):
        "Shut down cluster and cleanup temp files once program is complete"
        print 'Shutting down parallel engines'
        # close parallel engine
        if platform.uname()[1].split('.')[0] == 'ascar':
            p1 = Popen(['ipcluster', 'start', '--profile=sge', '--cluster-id=' + self.cluster_id])
            print 'Cleaning up temp files'
            os.remove(self.connection_file)
            os.remove(os.path.join(self.pwd, 'sge_controller'))
            os.remove(os.path.join(self.pwd, 'sge_engine'))
        else:
            p2 = Popen(['ipcluster', 'stop'])



