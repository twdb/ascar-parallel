"""
ascar-parallel
------------

package to deal with some common functions of parallel runs on ascar cluster as well as examples
"""

from setuptools import setup, find_packages

setup(
    name='ascar',
    version='0.1',
    author='Dharhas Pothina',
    author_email='dharhas.pothina@twdb.texas.gov',
    description='Ascar parallel utils',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'docopt>=0.6',
        'ipython>=0.13.2',
    ],
)
