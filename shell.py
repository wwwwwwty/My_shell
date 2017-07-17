import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform
from func import * 

built_in_cmds = {}

def tokenize(string):
    #分割string
    return shlex.split(string)

def preprocess(tokens):
    processed_token = []
    for token in tokens:
        if token.startswith('$'): #请求环境变零
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token

def handler_kill(signum, frame):
    #直接引发异常
    raise OSError("Killed!")

def execute(cmd_tokens):
    with open(HISTORY_PATH, 'a') as history_file:
        history_file.write(' '.join(cmd_tokens) + os.linesep) #os.linesep为当前平台终止符

    if cmd_tokens:
        #获取命令
        cmd_name = cmd_tokens[0]
        #获取命令参数
        cmd_args = cmd_tokens[1:]

        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_args)

        signal.signal(signal.SIGINT, handler_kill)

        if platform.system() != "Windows":
            #Unix平台,调用子进程执行命令
            p = subprocess.Popen(cmd_tokens)
            #等待子进程终止运行
            p.communicate()
        else:
            #Windows平台
            command = ""
            command = ' '.join(cmd_tokens)
            #执行cmd
            os.system(command)

    return SHELL_STATUS_RUN

def display_cmd_prompt():
    #获取当前用户名
    user = getpass.getuser()
    #获取password
    hostname = socket.gethostname()
    #获取当前工作路径
    cwd = os.getcwd()
    #获取最低一层目录名
    base_dir = os.path.basename(cwd)
    #如处于根目录下，则用~代替
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'
    #输出命令提示符
    if platform.system() != 'Windows':
        sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m] $ " % (user, hostname, base_dir)) #\033[显示方式;前景色;背景色m字符串 0默认1粗体4下划线5闪烁
    else:
        sys.stdout.write("[%s@%s %s]$ " % (user, hostname, base_dir))
    sys.stdout.flush()

def ignore_signals():
    if platform.system() != "Windows":
        #忽略Ctrl-Z
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    #忽略Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        display_cmd_prompt()
        ignore_signals()

        try:
            #读取命令
            cmd = sys.stdin.readline()
            #拆分命令，返回一个命令＋参数的list
            cmd_tokens = tokenize(cmd)
            #预处理，替换环境变量
            cmd_tokens = preprocess(cmd_tokens)
            #执行命令，返回shell状态
            status = execute(cmd_tokens)
        except:
            _, err, _ = sys.exc_info()
            print(err)

def register_command(name, func):
    """
    注册命令，使命令与相应的处理函数建立映射关系
    @param name: 命令名
    @param func: 函数名
    """
    built_in_cmds[name] = func

def init():
    """
    注册所有的命令
    """
    register_command("cd", cd)
    register_command("exit", exit)
    register_command("getenv", getenv)
    register_command("history", history)
    register_command("ls", ls)
    #register_command("help", help_list)
    print('Welcome to use wuwty shell! You can use the following command:')
    for cmd in built_in_cmds:
        print(cmd) 

def main():
    #初始化，建立命令和处理函数的关系
    init()
    shell_loop()

if __name__ == "__main__":
    main()
    