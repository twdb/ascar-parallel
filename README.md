parallel-examples
=================

Examples of parallel code using ipython on ascar

setting up ascar (one time stuff)
---------------------------------

* Edit your ~/.bashrc or ~/.bash_profile to include the correct version of python

	We have two versions of python installed on ascar. Enthought Canopy and Continuum's Anaconda.
	Currently Enthought Canopy has a working version of the GIS python modules, Anaconda does not.

	**ONLY USE ONE OF THE BELOW**

	To activate Enthought Canopy use the following <code> source /share/apps/enthought/User/bin/activate</code>
	To activate Continuum Anaconda use the following <code> export PATH="/share/apps/anaconda-1.6/bin:$PATH </code>

	**Currently I have only tested Canopy with the parallel code**


* setup your basic parallel ipython environment
  * <code>$ ipython profile create sge --parallel </code>
  * Edit ~/.config/ipython/profile_sge/ipcontroller_config.py, adding the line:

		<code> c.HubFactory.ip = '*' </code>

		to instruct the controller to listen on all interfaces.

  * Edit ~/.config/ipython/profile_sge/ipcluster_config.py, adding the lines:

		<code> c.IPClusterEngines.engine_launcher_class = 'SGEEngineSetLauncher'</code>

		<code> c.IPClusterStart.controller_launcher_class = 'SGEControllerLauncher'</code>

		<code> c.SGELauncher.queue = 'all.q'</code>


	at this point you should be able to start a cluster using

	<code>$ ipcluster start -n 10 --profile=sge --cluster-id=test </code>

	check that is started using

	<code>$ qstat</code>

	and stop it using

	<code>$ ipcluster stop --profile=sge --cluster-id=test </code>


installing ascar-parallel
-------------------------

This package ascar-parallel does some of the boiler-plate of starting and stopping the cluster for you.

It is already installed on the canopy python but for reference, to install:

<code>$ git clone git@github.com:twdb/ascar-parallel.git </code>

<code>$ cd ascar-parallel </code>

<code>$ python setup.py install </code>


using ascar parallel
--------------------

in your code use the following:

```python
from ascar_parallel import StartCluster

with StartCluster(8) as lview:
	lview.map(myfunc, <args>)
```

more details in the examples folder


common issues
-------------

* imports
	The simplest way to make imported packages available to all the compute engines you can import them inside the function you are parallelizing, i.e.

	```python
	from ascar_parallel import StartCluster

	def myfunc(a,b):
		import numpy as np
		return np.sqrt(a+b)

	a_list = range(5)
	b_list = range(5)
	with StartCluster(8) as lview:
		lview.map(myfunc, a_list, b_list)
	```

	if you are defining a bunch of helper functions for myfunc, then these will not be available on the compute engines. You can do one of two things.

	* define the functions inside myfunc:

	```python
	def myfunc(a,b)
		def helperfunc(c,d):
			stuff

		<statements>
	```

	* put the helper functions inside another file/module and then import them. This is the prefered way

	```python
	def myfunc(a,b)
		from mymodule import helperfunc
		<statements>
	```

* files:
	ascar has four main shared folders:
	* /home - user home directories, this is backed up. **DO NOT SAVE MODEL RESULTS HERE**
	* /share/swr - this is backed up. About 500GB of space currently available
	* /share/work - this is **not** backed up. About 7TB of space currently available
	* /share/apps - this is a good place to put software and executable code (i.e. fortran etc). You can then add this to your path so that executables are available from all the compute engines.