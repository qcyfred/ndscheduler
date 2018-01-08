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

'''configure the log'''
import logging
import logging.handlers

infile = 'mylogs/ct_fund_job2.log'
handler = logging.handlers.RotatingFileHandler(infile, mode='a', maxBytes=500*1024*1024, backupCount=3)
fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class CreateProcessJob(job.JobBase):

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': '配置任务信息',
            'arguments': [
                # argument1
                {'type': 'dict', 'description': '在 tasks.yaml [任务列表配置文件] 中的任务名'}

            ],
            'example_arguments': '[{\"task_name\": \"task1\"}]'
        }

    def run(self, kw_dict, *args, **kwargs):

        try:
            with open('tasks.yaml', 'r', encoding='utf-8') as f:
                tasks_dict = yaml.load(f.read())
        except Exception as e:
            with open('tasks.yaml', 'r') as f:
                tasks_dict = yaml.load(f.read())

        task_name = kw_dict.get('task_name')
        task_dict = tasks_dict[task_name]
        logger.info(task_dict)
        logger.info('Now is ready to run task %s' % task_dict['name'])

        # 即将启动的任务的输入参数
        task_params = task_dict.get('params')
        if task_params is None:
            task_params = {}

        # 即将启动的任务所在路径（到dir一层）
        env_path = task_dict.get('path_dir')
        sys.path.append(env_path)

        # 模块名（文件名以.py结束）
        o = import_module(task_dict['file_name'].split('.py')[0])
        o.start_task(**task_params)

        logger.info(('Task %s has been finished.' % task_name))

        # 删掉刚刚引入的包，确保每次都是最新的
        sys.path.remove(env_path)
        del o

        return [json.dumps(task_dict)]



if __name__ == "__main__":
    # You can easily test this job here
    job = CreateProcessJob.create_test_instance()
    job.run()
