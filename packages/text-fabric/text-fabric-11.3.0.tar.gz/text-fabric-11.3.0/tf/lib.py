"""
# Uitility functions

Read and write TF node sets from/to file.
"""

import pickle
import gzip
from .parameters import PICKLE_PROTOCOL, GZIP_LEVEL
from .core.helpers import console
from .core.files import expanduser as ex, fileExists, dirMake, splitPath


def writeSets(sets, dest):
    """Writes a dictionary of named sets to file.

    The dictionary will be written as a gzipped, pickled data structure.

    Intended use: if you have constructed custom node sets that you want to use
    in search templates that run in the TF browser.

    Parameters
    ----------
    sets: dict of sets
        The keys are names for the values, which are sets of nodes.
    dest: string
        A file path. You may use `~` to refer to your home directory.
        The result will be written from this file.

    Returns
    -------
    boolean
        `True` if all went well, `False` otherwise.
    """

    destPath = ex(dest)
    (baseDir, fileName) = splitPath(destPath)

    dirMake(baseDir)

    with gzip.open(destPath, "wb", compresslevel=GZIP_LEVEL) as f:
        pickle.dump(sets, f, protocol=PICKLE_PROTOCOL)
    return True


def readSets(source):
    """Reads a dictionary of named sets from file.

    This is used by the TF browser, when the user has passed a
    `--sets=fileName` argument to it.

    Parameters
    ----------
    source: string
        A file path. You may use `~` to refer to your home directory.
        This file must contain a gzipped, pickled data structure.

    Returns
    -------
    data | boolean
        The data structure contained in the file if all went well, False otherwise.

    """

    sourcePath = ex(source)
    if not fileExists(sourcePath):
        console(f'Sets file "{source}" does not exist.')
        return False
    with gzip.open(sourcePath, "rb") as f:
        sets = pickle.load(f)
    return sets
