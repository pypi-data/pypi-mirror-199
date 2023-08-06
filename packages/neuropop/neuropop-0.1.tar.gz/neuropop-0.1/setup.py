import setuptools
from setuptools import setup

install_deps = ['numpy>=1.20.0', 'scipy', 'natsort',
                'torch>=1.6']

docs_deps = [
        'sphinx>=3.0',
        'sphinxcontrib-apidoc',
        'sphinx_rtd_theme',
      ]

try:
    import torch
    a = torch.ones(2, 3)
    major_version, minor_version, _ = torch.__version__.split(".")
    if major_version == "2" or int(minor_version) >= 6:
        install_deps.remove("torch>=1.6")
except:
    pass

with open("README.md", "r") as fh:
    long_description = fh.read()
    
    
setup(
    name="neuropop",
    license="BSD",
    version="0.1",
    author="Marius Pachitariu and Carsen Stringer",
    author_email="stringerc@janelia.hhmi.org",
    description="analyses for neural populations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MouseLand/neuropop",
    setup_requires=[
      'pytest-runner',
      'setuptools_scm',
    ],
    packages=setuptools.find_packages(),
    use_scm_version=False,
    install_requires = install_deps,
    tests_require=[
      'pytest'
    ],
    extras_require = {
      'docs': docs_deps,
    },
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ),
)