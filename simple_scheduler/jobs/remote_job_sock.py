# coding: utf-8
"""A starter to start task.
version 2.0
"""
from __future__ import print_function
from __future__ import with_statement
from ndscheduler import job
import yaml
import sys
from importlib import import_module
import json
import socket
import json
from urllib.parse import quote
from urllib.parse import unquote

'''configure the log'''
import logging
import logging.handlers

infile = 'mylogs/remote_job.log'
handler = logging.handlers.RotatingFileHandler(infile, mode='a', maxBytes=500*1024*1024, backupCount=3)
fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RemoteJobSock(job.JobBase):

    # socket client端
    def send_msg(self, ip_addr, port, msg):

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip_addr, port))
            client.settimeout(5)
            client.sendall(quote(msg).encode('utf-8'))

        except Exception as e:
            logger.error(e)
            raise e
        finally:
            client.close()

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': '配置任务信息',
            'arguments': [
                # argument1
                {'type': 'dict', 'description': '在 remote_tasks.yaml [任务列表配置文件] 中的任务名'}

            ],
            'example_arguments': '[{\"task_name\": \"remote_task1\"}]'
        }

    def run(self, kw_dict, *args, **kwargs):

        try:
            with open('remote_tasks.yaml', 'r', encoding='utf-8') as f:
                tasks_dict = yaml.load(f.read())
        except Exception as e:
            with open('remote_tasks.yaml', 'r') as f:
                tasks_dict = yaml.load(f.read())

        task_name = kw_dict.get('task_name')
        task_dict = tasks_dict[task_name]
        logger.info(task_dict)
        logger.info('[%s] Now is ready to send msg.' % task_dict['name'])

        # 即将启动的任务的输入参数
        params = task_dict.get('params')
        msg = params.get('msg')

        remote_ip = task_dict.get('remote_ip')
        remote_port = task_dict.get('remote_port')
        self.send_msg(remote_ip, remote_port, json.dumps(msg))

        logger.info(('[%s] Msg has been sent.' % task_name))

        return [json.dumps(task_dict)]



if __name__ == "__main__":
    # You can easily test this job here
    job = RemoteJobSock.create_test_instance()
    job.run()
