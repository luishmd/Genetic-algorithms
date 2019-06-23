# Metadata
#=========
__author__ = 'Luis Domingues'

# Description
#============
# Library used for general read/write operations

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
import os.path as ospath
import shutil




#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def is_file_empty(file, verbose=False):
    """
    Function that tests whether the file is empty. True if yes, otherwise False.
    """
    result = False
    try:
        if os.stat(file).st_size == 0:
            result = True
    except:
        if verbose:
            print("Invalid file <%s>" %str(file))
        else:
            pass
    return result


def get_files_complete_names_with_extensions(dir_path, file_names=['*.'], file_extensions=[".*"], verbose=False):
    """
    Function that returns a list contaning the complete files names with extensions (e.g. ['C:/Users/luisd/Repos/sandbox_2/branches/gPB_Releases/gPB11/Library/gML/gML Auxiliary Correlations.gPJ-PB'] )
    """
    result = []
    try:
        # Get files to handle
        files_names = os.listdir(dir_path)
        try:
            assert files_names != None
            # There are files
            for file in files_names:
                name, extension = ospath.splitext(file)
                if (".*" in file_extensions) or (extension in file_extensions):
                    if ("*." in file_names) or (name in file_names):
                        file_complete_name = ospath.join(dir_path, file)
                        result.append(file_complete_name)
        except AssertionError:
            if verbose:
                print("Directory <{}> is empty".format(dir_path))
            else:
                pass
    except:
        if verbose:
            print("Could not find directory <{}>".format(dir_path))
        else:
            pass
    return result


def get_files_names_without_extensions(dir_path, file_extensions=[".*"], verbose=False):
    """
    Function that returns a list contaning the files names without extensions (e.g. ['gML Auxiliary Correlations'] )
    """
    result = []
    try:
        # Directory exists
        files_names = os.listdir(dir_path)
        try:
            assert files_names
            # There are files
            for file in files_names:
                name, extension = ospath.splitext(file)
                if extension in file_extensions or ".*" in file_extensions:
                    result.append(name)
        except AssertionError:
            if verbose:
                print("Directory <%s> is empty" %dir_path)
            else:
                pass
    except:
        if verbose:
            print("Could not find directory <%s>" %dir_path)
        else:
            pass
    return result


def get_files_pointers(dir_path, file_extensions=[".*"], verbose=False):
    """
    Function that returns the file pointer to each of the file with an extention in file_entensions
    """
    pointers_list = []
    files = get_files_complete_names_with_extensions(dir_path, file_extensions)
    for file in files:
        try:
            f = open(file,"r")
            pointers_list.append(f)
        except IOError:
            if verbose:
                print("Could not open file: <%s>" %str(file))
            else:
                pass
    return pointers_list


def write_to_file(file_object, what_to_write, verbose=False):
    """
    Function that writes what_to_write to a file
    """
    try:
        file_object.write(what_to_write)
        return file_object
    except:
        if verbose:
            print("Could not write to file <%s>.") %file_object
        else:
            pass
        return 1


def open_file(path, mode, verbose=False):
    """
    Function that opens a file and returns a file handle
    """
    try:
        f = open(path, mode)
        return f
    except:
        if verbose:
            print("Could not open file <%s>.") % path
        else:
            pass
        return 1

def close_file(file_handle, verbose=False):
    """
    Function that closes a file
    """
    try:
        file_handle.close()
        return 0
    except:
        if verbose:
            print("Could not close file <%s>.") % str(file_handle)
        else:
            pass
        return 1

def delete_file(path, verbose=False):
        """
        Function that deletes a file
        """
        try:
            os.remove(path)
            return 0
        except:
            if verbose:
                print("Could not delete file <%s>.") % path
            else:
                pass
            return 1


def copy_file(path_source, path_sink, verbose=False):
    """
    Function that copies a file from a source to a sink directory and renames it, if needed
    """
    try:
        shutil.copy(path_source, path_sink)
        return 0
    except:
        if verbose:
            print("Could not copy file <{}>.".format(path_source))
        else:
            pass
        return None



#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass

