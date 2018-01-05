# coding: utf-8

import os
import win32process
import win32event
from ctypes import *
from win32gui import *
from win32con import *
import time
import pandas as pd
import datetime
import window_name_utils
import threading
import socket
import json
from urllib.parse import quote
from urllib.parse import unquote


'''configure the log'''
import logging
import logging.handlers
import ctypes
infile = 'remote_sock_server.log'
handler = logging.handlers.RotatingFileHandler(infile, mode='a', maxBytes=500*1024*1024, backupCount=3)
fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



# IP和端口。注意防火墙。
local_ip = '10.180.90.236'
local_port = 43218

# 隐藏窗口
whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((local_ip, local_port))
server.listen(5)

admin_filter = {
    'localhost': '本机',
    '127.0.0.1': '本机',
    '10.180.90.236': '本机',
    '10.180.10.91': '远程 Windows Server'
}

while 1:

    conn, addr = server.accept()

    msg = unquote(conn.recv(1024).decode('utf-8'))  # json格式的str

    peer_name = conn.getpeername()  # peer_name是个tuple，peer_name[0]是ip，peer_name[1]是端口号
    now_dt = str(datetime.datetime.now())
    
    # logger.error('Environment variable SIMPLE_SCHEDULER_SLACK_URL is not specified. '
    #                      'So we cannot send slack message.')

    logger.info( '%s, visitor: %s:%s' % (now_dt, peer_name[0], peer_name[1])  ) # sock_name

    params = json.loads(msg)
    msg_type = params['msg_type']

    # 管理员权限验证
    if peer_name[0] in admin_filter.keys():
        logger.info(params)

        # 1. 运行普通py脚本的msg
        if 'run_py' == msg_type:
            # t = threading.Thread(target=start_py_prog, args=(params,))
            # t.start()

            logger.info('执行py文件')
            # remote_py_file_path = params['remote_py_file_path']
            remote_py_file_path = 'start_prog.py'

            command = '''start cmd /k " python {remote_py_file_path} "{extra_param}" && exit"'''
            param_json_str = json.dumps(params)
            param_json_str = param_json_str.replace('"', '$')
            command = command.format(**{'remote_py_file_path': remote_py_file_path,
                                        'extra_param': param_json_str})
            
            logger.info(command)
            os.system(command)

