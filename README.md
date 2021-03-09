Python Package `dito`
=====================

`dito` is yet another toolbox for the daily work with [OpenCV](https://opencv.org/) under Python.


Status
------

![Tests](https://github.com/dhaase-de/dito/workflows/Tests/badge.svg)
[![PyPI Version](https://img.shields.io/pypi/v/dito.svg)](https://pypi.python.org/pypi/dito/)
[![License](https://img.shields.io/github/license/dhaase-de/dito.svg)](LICENSE.txt)


Installation
------------

For production:
* either install via `pip install --upgrade dito`, **or**
* [download wheel from PyPI](https://pypi.org/project/dito/#files) and install it via `pip install dito-x.y.z-py3-none-any.whl`

For development:
1. clone this repository, **and**
2. run `scripts/build_install_dev.sh` (which is equivalent to `python3 setup.py develop --user`)


Tests
-----

Use `scripts/run_tests.sh` to run all unit tests.


Changelog
=========

2.0.0 (2021-03-09)
------------------

* initial release, based in large parts on [`dh.image`](https://github.com/dhaase-de/dh-python-dh)