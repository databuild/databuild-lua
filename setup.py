import os
from setuptools import setup, find_packages
import subprocess

VERSION = "0.0.1"


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('requirements.txt').splitlines()

pypi_requirements = [req for req in requirements if not req.startswith('http')]
dependency_links = [req for req in requirements if req.startswith('http')]

tests_requirements = read('test-requirements.txt').splitlines()

# Temporary fix until databuild gets released
subprocess.call(["pip", "install", "--quiet", "https://github.com/databuild/databuild/archive/master.zip"])

setup(
    name="databuild_lua",
    version=VERSION,
    description="Lua Environment Plugin for Databuild",
    long_description=read('README.rst'),
    url='https://github.com/databuild/databuild-lua',
    license='BSD',
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    install_requires=pypi_requirements,
    dependency_links=dependency_links,
    tests_require=tests_requirements,
)
