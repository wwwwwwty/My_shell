from .constants import *

def ls(args):
    def print_files(files):
        filestr = ''
        whitespace = '     '
        for file in files:
            filestr += str(file)
            filestr += whitespace
        print(filestr)

    if len(args) > 0:
        filelist = os.listdir(args[0])
        print_files(filelist)
    else:
        filelist = os.listdir(os.getcwd())
        print_files(filelist)
    return SHELL_STATUS_RUN