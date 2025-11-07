from os import listdir
from os.path import isfile, join, isdir
def folder_names(directory):
    folders = [f for f in listdir(directory) if isdir(join(directory, f))]
    return folders

def file_names(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    return files

