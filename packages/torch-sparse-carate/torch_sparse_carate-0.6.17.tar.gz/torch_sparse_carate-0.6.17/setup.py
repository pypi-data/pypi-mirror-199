import glob
import os
import os.path as osp
import platform
import sys
from itertools import product


from setuptools import find_packages, setup


__version__ = '0.6.17'
URL = "https://codeberg.org/sail.black/pytorch_sparse_carate.git"


install_requires = [
    'scipy',
    'torch'
]

test_requires = [
    'pytest',
    'pytest-cov',
]

# work-around hipify abs paths
include_package_data = True

setup(
    name='torch_sparse_carate',
    version=__version__,
    description=('PyTorch Extension Library of Optimized Autograd Sparse '
                 'Matrix Operations'),
    author='Julian M. Kleber',
    url=URL,
    author_email='julian.kleber@sail.black',
    download_url=f'{URL}/archive/{__version__}.tar.gz',
    keywords=[
        'pytorch',
        'sparse',
        'sparse-matrices',
        'autograd',
    ],
    python_requires='>=3.7',
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
    packages=find_packages(),
    include_package_data=include_package_data,
)
