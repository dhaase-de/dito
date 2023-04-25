Python Package `dito`
=====================

`dito` is yet another toolbox for the daily work with [OpenCV](https://opencv.org/) under Python.

It provides convenience wrappers for frequently used image-related functionalities in OpenCV and NumPy, as well as additional functionality built on top of them.


Status
------

[![PyPI Version](https://img.shields.io/pypi/v/dito.svg)](https://pypi.python.org/pypi/dito/#files)
[![GitHub last commit](https://img.shields.io/github/last-commit/dhaase-de/dito)](https://github.com/dhaase-de/dito/commits/main)
[![GitHub commits since tagged version](https://img.shields.io/github/commits-since/dhaase-de/dito/latest/main)](https://github.com/dhaase-de/dito/commits/main)
[![Tests (subset)](https://github.com/dhaase-de/dito/actions/workflows/tests-subset.yml/badge.svg)](https://github.com/dhaase-de/dito/actions/workflows/tests-subset.yml)
[![Tests (full)](https://github.com/dhaase-de/dito/actions/workflows/tests-full.yml/badge.svg)](https://github.com/dhaase-de/dito/actions/workflows/tests-full.yml)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/dito.svg)](https://pypi.python.org/pypi/dito/)
[![License](https://img.shields.io/github/license/dhaase-de/dito.svg)](LICENSE.txt)


Documentation
-------------

API documentation is available online at [https://dhaase-de.github.io/dito/](https://dhaase-de.github.io/dito/).

To build the documentation locally (into the subdir `docs/`), run

    pip install -r requirements_build.txt
    ./scripts/build_docs.sh


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

### v2.9.0 (2023-04-19) - QoL Update II ###
* added convenience image difference functions `clipped_diff`, `abs_diff`, `shifted_diff`
* added convenience constant color overlay function `overlay_constant`
* added support for `pathlib` filenames
* added Qt6 image conversion
* improved `pinfo` (minimal mode, wrapper script change, bugfix)
* fixed NumPy-related issues

### v2.8.0 (2022-04-05) - PCA Update ###
* added PCA and NMF-based texture models
* added load/save support for the `.npz` format
* added `split_channels`

### v2.7.0 (2022-02-16) - Misc Update ###
* added clahe wrapper
* added argument `keep_color_dimension` to `as_gray`
* fixed `stack` not working for float64 images
* started refactoring some old tests

### v2.6.0 (2021-12-19) - Data Update ###
* added test image generator
* added USC-SIPI test image 4.1.07 (jelly beans)
* minor improvements and fixes

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
