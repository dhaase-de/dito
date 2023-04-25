"""
`dito` is yet another toolbox for the daily work with OpenCV under Python.

It provides convenience wrappers for frequently used image-related
functionalities in OpenCV and NumPy, as well as additional functionality built
on top of them.

All submodules are imported and can be accessed directly through the `dito`
namespace. For example, `dito.io.load` can be accessed as `dito.load`.
"""

__version__ = "2.9.1.dev0"


from dito.analysis import *
from dito.conversion import *
from dito.core import *
from dito.data import *
from dito.draw import *
from dito.exceptions import *
from dito.highgui import *
from dito.inspection import *
from dito.io import *
from dito.parallel import *
from dito.processing import *
from dito.utils import *
from dito.visual import *
