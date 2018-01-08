# coding: utf-8
"""A starter to start task."""
from __future__ import print_function
from __future__ import with_statement
from ndscheduler import job
import yaml
import os
import json


class CtFundJob(job.JobBase):

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

        # config_path = 'E:/src/ndscheduler/simple_scheduler/'
        try:
            with open('tasks.yaml', 'r', encoding='utf-8') as f:
                tasks_dict = yaml.load(f.read())
        except Exception as e:
            with open('tasks.yaml', 'r') as f:
                tasks_dict = yaml.load(f.read())

        task_name = kw_dict.get('task_name')
        task_dict = tasks_dict[task_name]
        print(task_dict)
        print('Now is ready to run task %s' % task_dict['name'])

        task_parmas = task_dict.get('params')
        if task_parmas is not None:
            param_json_str = json.dumps(task_parmas).replace('"', '$')
        else:
            param_json_str = ''

        if task_dict['finish_exit'] == False:
            command = '''start cmd /k "{driver}: & cd {path_dir} & python {py_file_name} "{params}""'''.format(
                driver=task_dict['driver'], path_dir=task_dict['path_dir'], py_file_name=task_dict['file_name'],
                params=param_json_str)
        else:
            command = '''start cmd /k "{driver}: & cd {path_dir} & python {py_file_name} "{params}" && exit"'''.format(
                driver=task_dict['driver'], path_dir=task_dict['path_dir'], py_file_name=task_dict['file_name'],
                params=param_json_str)

        status = os.system(command)
        return [json.dumps(task_dict)]
        # print(status)




if __name__ == "__main__":
    # You can easily test this job here
    job = CtFundJob.create_test_instance()
    job.run()
