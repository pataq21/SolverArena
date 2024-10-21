from setuptools import setup, find_packages

setup(
    name='solverarena',
    version='0.2.3',
    packages=find_packages(),
    install_requires=[
        'memory-profiler',
    ],
    extras_require={
        'highs': ['highspy'],
        'gurobi': ['gurobipy'],
        'scip': ['pyscipopt'],
        'ortools': ['ortools'],
        'all_solvers': ['highspy', 'gurobipy', 'pyscipopt', 'ortools']
    },
    description='A library to run and compare optimization models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Javier Berga García',
    author_email='pataq21@gmail.com',
    url='https://github.com/pataq21/SolverArena',
    license='MIT',
)
