# Metadata
#=========
__author__ = 'Luis Domingues'

# Description
#============
# Library used for directory operations

# Notes
#======
#

# Known issues/enhancements
#==========================
#

#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import os as os
import getpass as getpass
import lib_path_ops

#----------------------------------------------------------------------------------------
# INPUTS
#----------------------------------------------------------------------------------------
# To be replaced by configfile


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def clean_dir(dir_path):
    """
    Function that cleans dir_path of any subdirs and files
    """
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))


def get_username():
    """
    Function that returns the username of a given session
    """
    return getpass.getuser()


def listdir(path):
    """
    Function that list the contents of a given directory.
    """
    result = []
    try:
        result = os.listdir(path)
    except:
        print("Could not open <%s>" %path)
    return result

def create_dir(root_dir, dir_name):
    """
    Function that creates a directory in root_dir
    :param root_dir: the directory root
    :param dir_name: the name of the directory
    :return:
    """
    d = None
    try:
        d = lib_path_ops.join_paths(root_dir, dir_name)
        os.mkdir(d)
    except OSError:
        print ("Could not create directory in {}.".format(root_dir))
    return d


#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass