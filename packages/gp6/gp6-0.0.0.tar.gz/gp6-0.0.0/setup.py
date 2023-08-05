from setuptools import setup

setup(
    name='gp6',
    version='0.0.0',    
    description='Code for Gaussian Processes aimed at late time cosmological reconstruction',
    url='https://github.com/reggiebernardo/gp6',
    author='Reginald Christian Bernardo',
    author_email='reginaldchristianbernardo@gmail.com',
    license='MIT license',
    packages=['gp6'],
    install_requires=['numpy', 'scipy', 'math'],
)