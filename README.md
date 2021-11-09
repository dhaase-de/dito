Python Package `dito`
=====================

`dito` is yet another toolbox for the daily work with [OpenCV](https://opencv.org/) under Python.


Status
------

[![Tests (subset)](https://github.com/dhaase-de/dito/actions/workflows/tests-subset.yml/badge.svg)](https://github.com/dhaase-de/dito/actions/workflows/tests-subset.yml)
[![Tests (full)](https://github.com/dhaase-de/dito/actions/workflows/tests-full.yml/badge.svg)](https://github.com/dhaase-de/dito/actions/workflows/tests-full.yml)
[![PyPI Version](https://img.shields.io/pypi/v/dito.svg)](https://pypi.python.org/pypi/dito/)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/dito.svg)](https://pypi.python.org/pypi/dito/)
[![License](https://img.shields.io/github/license/dhaase-de/dito.svg)](LICENSE.txt)


Requirements
------------

* [Python 3](https://www.python.org/)
* [NumPy](https://numpy.org/)
* [OpenCV](https://opencv.org/)

See `requirements.txt` for version details.


Installation
------------

For production:
* either install via `pip install --upgrade dito`, **or**
* [download wheel from PyPI](https://pypi.org/project/dito/#files) and install it via `pip install dito-x.y.z-py3-none-any.whl`

For development:
1. clone this repository via `git clone https://github.com/dhaase-de/dito.git`, **and**
2. run `scripts/build_install_dev.sh` (which is equivalent to `python3 setup.py develop --user`)


Tests
-----

Use `scripts/run_tests.sh` to run all unit tests.
This is equivalent to `python3 -m dito.tests --verbose`.


Changelog
---------

### v2.5.0 (2021-10-21) - QoL Update ###
* added funtion `draw_symbol` with support for various symbols
* added ColorBrewer colormaps
* added `mp_starmap` as an easy-to-use wrapper for parallel processing tasks
* added `Slider` class for easy-to-use OpenCV trackbar abstractions (namely `ChoiceSlider`, `BoolSlider`, `IntegerSlider`, and `FloatSlider`)
* added aliases for morphological operations and helper functions (`dilate`, `erode`, `tophat`, `morpho_op_kernel`, ...)
* added commonly needed padding and cropping wrappers (`center_pad_to`, `center_crop_to`, `center_pad_crop_to`)
* added `PaddedImageIndexer` which provides padded images when indexed beyond the image bounds
* added `astack` to automatically stack images into an image of a given aspect ratio
* improved `pinfo` (support for multiple possibly named images, filenames, short/extended infos, wrapper script `dito_pinfo.py`, ...)
* added `dog` for getting the Difference-of-Gaussian of an image and its interactive version `dog_interactive`
* added several more helper functions and improvements (e.g., `load_multiple`, `create_colormap`, raise of `dito.QkeyException`, ...)

### v2.4.0 (2021-07-13) - Contour Update ###
* added support for contour finding and handling (`Contour`, `ContourList`, `ContourFinder`, `VoronoiPartition`)
* added aliases for color conversion (`convert_color`, `bgr_to_hsv`, `hsv_to_bgr`)
* added efficient gamma function (`gamma`)
* added several more helper functions and improvements (`grid`, `gaussian_blur`, `is_(integer|float|bool)_(dtype|image)`, `save_tmp`, ...)

### v2.3.0 (2021-05-26) - Text Update II ###
* improved text drawing (e.g. margin, padding, border, rotation, alignment, support for ANSI escape sequences, greek alphabet, outline background mode, width shrinking)
* added some helper functions (which were needed for improved text drawing), e.g. `insert`, `constant_image`, `rotate*`, `dilate`, `pad`

### v2.2.0 (2021-04-09) - Text Update ###
* added/improved support for other (optional) image showing engines (`IPython`, `matplotlib.pyplot`, `pygame`)
* added support for bitmap font handling (class `MonospaceBitmapFont`)
* added bitmap fonts "Scientifica", "Source Code Pro", "Tamzen", and "Terminus"
* changed `text` to use bitmap fonts instead of OpenCV's font handling and improved text drawing functionality (e.g., support for opacity, color, absolute positioning)
* added many smaller improvements and fixes (e.g., `colorize` working with custom colormaps for OpenCV<3.3.0)
* added several helper functions (e.g., `as_channels`)

### v2.1.0 (2021-03-14) - IO Update ###
* added `MultiShow` as extension of `show` which can also interactively re-show or save images
* added `VideoSaver`and script `dito_images_to_video.py`
* extended other IO functionality (`CachedImageLoader`, `.npy` support for `save` and `load`, and `encode`)
* added synthetic image generators (`checkerboard`, `background_checkerboard`, `random_image`)
* added several helper functions (e.g., `now_str`, `human_bytes`)
* fixed some minor issues (e.g., handling of empty dirs in `mkdir`)

### v2.0.0 (2021-03-09) - Initial Version ###
* initial release, based in large parts on [`dh.image`](https://github.com/dhaase-de/dh-python-dh)
