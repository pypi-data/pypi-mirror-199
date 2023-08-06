import os
import setuptools


def get_readme():

    with open('README.md', 'r') as f:
        return f.read()


def get_version_info():

    version_path = os.path.join('smiles_encoder', 'version.py')
    file_vars = {}
    with open(version_path, 'r') as f:
        exec(f.read(), file_vars)
    f.close()
    return file_vars['__version__']


VERSION = get_version_info()


setuptools.setup(
    name='smiles-encoder',
    version=VERSION,
    description=('One-hot encoding for simple molecular-input line-entry '
                 'system (SMILES) strings'),
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/tjkessler/smiles-encoder',
    author='Travis Kessler',
    author_email='travis.j.kessler@gmail.com',
    license='MIT',
    packages=['smiles_encoder'],
    install_requires=[],
    zip_safe=False
)
