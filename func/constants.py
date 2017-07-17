import os

SHELL_STATUS_STOP = 0
SHELL_STATUS_RUN = 1

#获取当前系统平台用户根目录
HISTORY_PATH = os.path.expanduser('~') + os.sep + '.my_Python_shell_history'