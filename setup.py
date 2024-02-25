import os.path
import re


try:
    # setuptools has wheel support (command "bdist_wheel"), but is not in the standard library
    import setuptools
    print("==> using module 'setuptools'")
    setup = setuptools.setup
except ImportError:
    # fallback option without wheel support
    import distutils.core
    print("==> module 'setuptools' not found, falling back to 'distutils'")
    setup = distutils.core.setup


##
## preparations
##


# package dirs
package_name = "dito"
package_dir = os.path.abspath(os.path.dirname(__file__))
source_dir = os.path.join(package_dir, package_name)


# read version number from text file
version_filename = os.path.join(source_dir, "__init__.py")
with open(version_filename, "r") as f:
    for line in f:
        match = re.match(r"__version__\s*=\s*['\"]([a-zA-Z0-9-_.]+)['\"]", line)
        if match is not None:
            version = match.group(1)
            break
    else:
        # end of file, version was not found
        raise RuntimeError("Could not parse version number from file '{}'".format(version_filename))


##
## main call
##


setup(
    name=package_name,
    version=version,
    description="Yet another toolbox for the daily work with OpenCV under Python",
    author="Daniel Haase",
    url="https://github.com/dhaase-de/dito",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    packages=[package_name],
    package_data={package_name: [
        "resources/colormaps/*.png",
        "resources/colormaps/colorbrewer/LICENSE.txt",
        "resources/colormaps/colorbrewer/colorbrewer.json",
        "resources/colormaps/colorbrewer/*.png",
        "resources/fonts/*/LICENSE.txt",
        "resources/fonts/scientifica/*.png",
        "resources/fonts/source_code_pro/*.png",
        "resources/fonts/terminus/*.png",
        "resources/images/*.png",
    ]},
    scripts=[
        "bin/dito_czi_to_npy.py",
        "bin/dito_images_to_video.py",
        "bin/dito_pinfo.py",
    ],
)
