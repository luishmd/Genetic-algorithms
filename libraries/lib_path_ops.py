# Metadata
#=========
__author__ = 'Luis Domingues'

# Description
#============
# Library that provides path operations

# Notes
#======
#

# Known issues/enhancements
#==========================
#

#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import os.path as lib_path


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def get_abs_path(path):
    """
    Function that returns a normalized absolutized version of the pathname path
    """
    abs_path = lib_path.abspath(path)
    return abs_path


def get_real_path(path):
    """
    Function that returns the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system).
    """
    real_path = lib_path.realpath(path)
    return real_path


def get_relative_path(path, start_path=""):
    """
    Function that returns a relative filepath to path either from the current directory or from an optional start directory.
    This is a path computation: the filesystem is not accessed to confirm the existence or nature of path or start
    """
    if start_path:
        rel_path = lib_path.relpath(path, start_path)
    else:
        rel_path = lib_path.relpath(path)
    return rel_path


def get_root_path(abs_path, base_path):
    #Function that returns the root path of an absolute path:
    #    abs_path = 'C:\Users\luisd\Repos\svn_coding_repo\trunk\training\libraries'
    #    base_path = ./trunk/training/databases
    #    return = 'C:\\Users\\luisd\\Repos\\svn_coding_repo'
    root_path_list = abs_path.split(get_relative_path(base_path))
    return get_abs_path(root_path_list[0])


def join_paths(path_1, path_2):
    """
    Function joins one or more path components intelligently
    """
    a = lib_path.join(path_1, path_2)
    return a


#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass