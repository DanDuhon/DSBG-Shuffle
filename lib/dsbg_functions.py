import logging
import inspect
import platform
from os import path

from dsbg_classes import CustomAdapter


if platform.system() == "Windows":
    pathSep = "\\"
    windowsOs = True
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s|%(levelname)s|%(message)s", "%d/%m/%Y %H:%M:%S")
    fh = logging.FileHandler(path.dirname(path.realpath(__file__)) + "\\dsbg_shuffle_log.txt".replace("\\", pathSep), "w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    adapter = CustomAdapter(logger, {"caller": ""})
    logger.setLevel(logging.DEBUG)
else:
    pathSep = "/"
    windowsOs = False