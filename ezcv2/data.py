import os.path

import ezcv2.io


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datafiles")
DATA_FILENAMES = {
    "PM5544": os.path.join(DATA_DIR, "images", "PM5544.png")        
}


def pm5544():
    return ezcv2.io.load(filename=DATA_FILENAMES["PM5544"])
