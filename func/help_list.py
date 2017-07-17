from .constants import *
import sys
sys.path.append("..")
from shell import built_in_cmds

def help_list(args):
    print('You can use the following command:')
    # for cmd in built_in_cmds:
    #     print(cmd)
    print(built_in_cmds)
    return SHELL_STATUS_RUN
