"""Base class for a job."""

import json
import logging
import os
import socket

from ndscheduler import constants
from ndscheduler import utils
from ndscheduler.core import scheduler_manager

logger = logging.getLogger(__name__)


class JobBase:

    def __init__(self, job_id, execution_id):
        self.job_id = job_id
        self.execution_id = execution_id

    @classmethod
    def create_test_instance(cls):
        """Creates an instance of this class for testing."""
        return cls(None, None)

    @classmethod
    def get_scheduled_description(cls):
        hostname = socket.gethostname()
        pid = os.getpid()
        return 'hostname: %s | pid: %s' % (hostname, pid)

    @classmethod
    def get_scheduled_error_description(cls):
        hostname = socket.gethostname()
        pid = os.getpid()
        return 'hostname: %s | pid: %s' % (hostname, pid)

    @classmethod
    def get_running_description(cls):
        hostname = socket.gethostname()
        pid = os.getpid()
        return 'hostname: %s | pid: %s' % (hostname, pid)

    @classmethod
    def get_failed_description(cls):
        hostname = socket.gethostname()
        pid = os.getpid()
        return 'hostname: %s | pid: %s' % (hostname, pid)

    @classmethod
    def get_succeeded_description(cls, result=None):
        hostname = socket.gethostname()
        pid = os.getpid()
        return 'hostname: %s | pid: %s' % (hostname, pid)

    @classmethod
    def get_scheduled_error_result(cls):
        return utils.get_stacktrace()

    @classmethod
    def get_failed_result(cls):
        return utils.get_stacktrace()

    @classmethod
    def meta_info(cls):
        """Returns meta info for this job class.

        For example:
            {
                'job_class_string': 'myscheduler.jobs.myjob.MyJob',
                'arguments': [
                    {'type': 'string', 'description': 'name of this channel'},
                    {'type': 'string', 'description': 'what this channel does'},
                    {'type': 'int', 'description': 'created year'}
                ],
                'example_arguments': '["music channel", "it's an awesome channel", 1997]',
                'notes': 'need to specify environment variable API_KEY first'
            }
        The arguments property should be consistent with the run() method.

        This info will be used in web ui for explaining what kind of arguments is needed for a job.

        You should override this function if you want to make your scheduler web ui informative :)

        :return: meta info for this job class.
        :rtype: dict
        """
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'arguments': [],
            'example_arguments': '',
            'notes': ''
        }

    @classmethod
    def run_job(cls, job_id, execution_id, *args, **kwargs):
        """Wrapper to run this job.

        It updates the execution state, i.e., running, succeeded or failed.

        :param str job_id: Job id.
        :param str execution_id: Execution id.
        :param args:
        :param kwargs:
        """
        scheduler = scheduler_manager.SchedulerManager.get_instance()
        datastore = scheduler.get_datastore()
        try:
            datastore.update_execution(execution_id, state=constants.EXECUTION_STATUS_RUNNING,
                                       hostname=socket.gethostname(), pid=os.getpid(),
                                       description=cls.get_running_description())
            job = cls(job_id, execution_id)

            # 这里要写日志

            result = job.run(*args, **kwargs)
            result_json = json.dumps(result, indent=4, sort_keys=True)
            s = ''
            if isinstance(result, list):
                if len(result) == 1:
                    result_item = json.loads(result[0])
                    for k, v in result_item.items():
                        s += '%s: %s\n' % (k, v)
                    s = s[:-1]
            datastore.update_execution(execution_id, state=constants.EXECUTION_STATUS_SUCCEEDED,
                                       description=cls.get_succeeded_description(result),
                                       result=s)
            # 这里要写更新execution_results的函数
            # 这里要写日志
        except Exception as e:
            logger.exception(e)
            datastore.update_execution(execution_id,
                                       state=constants.EXECUTION_STATUS_FAILED,
                                       description=cls.get_failed_description(),
                                       result=cls.get_failed_result())
            # 这里要写更新execution_results的函数
            # 这里要写日志

    def run(self, *args, **kwargs):
        """The "main" function for a job.

        Any subclass has to implement this function.

        The return value of this function will be stored in the database as json formatted string
        and will be shown for each execution in web ui.

        :param args:
        :param kwargs:
        :return: None or json serializable object.
        """
        raise NotImplementedError('Please implement this function')
