# setup.py

from setuptools import setup, find_packages

setup(
    name='solver_arena',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'highspy',
        'psutil',
        'gurobipy',
    ],
    entry_points={
    },
    description='A library to run and compare optimization models',
    author='Javier Berga García',
    author_email='pataq21@gmail.com',
    url='https://github.com/pataq21/SolverArena',
)
