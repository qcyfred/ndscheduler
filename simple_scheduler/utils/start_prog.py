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
import sys
import json


'''configure the log'''
import logging
import logging.handlers

infile = 'start_prog.log'
handler = logging.handlers.RotatingFileHandler(infile, mode='a', maxBytes=500*1024*1024, backupCount=3)
fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi


path = '软件启动信息.xlsx'
df = pd.read_excel(path)

param_str = sys.argv[1:][0]
params = json.loads(param_str.replace('$', '"'))
print(params)

task_group = params.get('task_group', -1)


df_to_start = df.query("task_group == @task_group")
try:
    for i in range(len(df_to_start)):

        d = df_to_start.iloc[i, :].to_dict()

        x = int(d['x'])
        y = int(d['y'])
        dx = int(d['dx'])
        dy = int(d['dy'])

        si = win32process.STARTUPINFO()
        si.dwX, si.dwY = [x, y]
        xySize = [dx, dy]
        si.dwXSize, si.dwYSize = xySize
        si.dwFlags ^= STARTF_USEPOSITION | STARTF_USESIZE

        if pd.isnull(d['params']):
            cmd_line = """%s"""%d['path']
        else:
            cmd_line = """%s %s"""%(d['path'], d['params'])
        
        logger.info(cmd_line)

        params = (None, cmd_line, None , None , 0 ,  16 , None , None ,si )
        hProcess, hThread, dwProcessId, dwThreadId = win32process.CreateProcess(*params)

        # 如果不是cmd程序，还要调用Move，否则就结束
        # # 新进程的时候，能得到pid，已经有进程了，得到的不是pid…
        logger.info('hProcess %d, hThread %d, dwProcessId %d, dwThreadId %d' % (hProcess, hThread, dwProcessId, dwThreadId))

        time.sleep(int(d['sleep_time']))

        if d['is_cmd'] == 'y':
            pass # 因为cmd可以启动时指定位置
        else:

            # 得到当前handle、pid、窗口名称的信息
            window_info_df = window_name_utils.get_window_info()

            if d['use_caption'] == 'n': # 用pid
                # 有些已经打开了的程序，再用createProcess得到的pid，不是它本身的pid…
                hwnd = window_info_df.loc[window_info_df['pid']==dwProcessId, 'handle'].values[0]

            elif d['use_caption'] == 'y':
                logger.info('通过窗口名称获得handle')
                
                handles = window_info_df.loc[window_info_df['caption']==d['caption'], 'handle'].values

                if len(handles) == 1: # 唯一标题，直接根据hwnd移动
                    hwnd = handles[0]

                elif len(handles) > 1: # 标题名字有重复的，根据 createProcess 得到的pid， 再找handle， 移动
                    # 先假设这个pid只会有一个handle
                    hwnd = window_info_df.loc[(window_info_df['pid'] == dwProcessId) & (
                    (window_info_df['caption'] == d['caption'])), 'handle'].values[0]

            # ========
            ShowWindow(hwnd, SW_RESTORE)  # 1. 还原 # 有些窗口不能还原?!!!
            time.sleep(1)
            MoveWindow(hwnd, x, y, dx, dy, True)  # 2. 移动

            if d['need_max'] == 'y':
                time.sleep(1)
                ShowWindow(hwnd, SW_MAXIMIZE)  # 最大化

except Exception as e:
    logger.error(e)

