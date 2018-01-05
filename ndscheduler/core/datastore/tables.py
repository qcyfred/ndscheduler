"""Define database schemas."""

import sqlalchemy

from ndscheduler import settings
from ndscheduler import utils

METADATA = sqlalchemy.MetaData()

#
# Jobs
# It's defined by apscheduler library.
#

#
# Executions
#
EXECUTIONS = sqlalchemy.Table(
    settings.EXECUTIONS_TABLENAME, METADATA,
    sqlalchemy.Column('eid', sqlalchemy.Unicode(191, _warn_on_bytestring=False), primary_key=True),
    sqlalchemy.Column('hostname', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('pid', sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column('state', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('scheduled_time', sqlalchemy.DateTime(timezone=True), nullable=False,
                      default=utils.get_current_datetime),
    sqlalchemy.Column('updated_time', sqlalchemy.DateTime(timezone=True),
                      default=utils.get_current_datetime, onupdate=utils.get_current_datetime),
    sqlalchemy.Column('description', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('result', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('job_id', sqlalchemy.Text, nullable=False),
    sqlalchemy.Column('task_id', sqlalchemy.Text, nullable=True))

#
# Audit logs
#
AUDIT_LOGS = sqlalchemy.Table(
    settings.AUDIT_LOGS_TABLENAME, METADATA,
    sqlalchemy.Column('job_id', sqlalchemy.Text, nullable=False),
    sqlalchemy.Column('job_name', sqlalchemy.Text, nullable=False),
    sqlalchemy.Column('event', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('user', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('created_time', sqlalchemy.DateTime(timezone=True), nullable=False,
                      default=utils.get_current_datetime),
    sqlalchemy.Column('description', sqlalchemy.Text, nullable=True))



# #
# # 执行结果
# # 按列存放
# # 日期、任务id、任务名称、执行参数、返回值（TEXT）、执行状态
# #
# EXECUTION_RESULTS = sqlalchemy.Table(
#     'execution_results', METADATA,
#     sqlalchemy.Column('eid', sqlalchemy.Unicode(191, _warn_on_bytestring=False), primary_key=True),
#     sqlalchemy.Column('hostname', sqlalchemy.Text, nullable=True),
#     sqlalchemy.Column('pid', sqlalchemy.Integer, nullable=True),
#     sqlalchemy.Column('state', sqlalchemy.Integer, nullable=False),
#     sqlalchemy.Column('scheduled_time', sqlalchemy.DateTime(timezone=True), nullable=False,
#                       default=utils.get_current_datetime),
#     sqlalchemy.Column('updated_time', sqlalchemy.DateTime(timezone=True),
#                       default=utils.get_current_datetime, onupdate=utils.get_current_datetime),
#     sqlalchemy.Column('description', sqlalchemy.Text, nullable=True),
#     sqlalchemy.Column('result', sqlalchemy.Text, nullable=True),
#     sqlalchemy.Column('job_params', sqlalchemy.Text, nullable=True),
#     sqlalchemy.Column('job_id', sqlalchemy.Text, nullable=False),
#     sqlalchemy.Column('task_id', sqlalchemy.Text, nullable=True))
#
#
# # 执行时软件打印的LOG
# EXECUTIONS_LOGS = sqlalchemy.Table(
#     'execution_logs', METADATA,
#     sqlalchemy.Column('eid', sqlalchemy.Unicode(191, _warn_on_bytestring=False), primary_key=True),
#     sqlalchemy.Column('hostname', sqlalchemy.Text, nullable=True),
#     sqlalchemy.Column('pid', sqlalchemy.Integer, nullable=True),
#     sqlalchemy.Column('log_level', sqlalchemy.Text, nullable=False),
#     sqlalchemy.Column('log_time', sqlalchemy.DateTime(timezone=True), nullable=False,
#                       default=utils.get_current_datetime),
#     sqlalchemy.Column('job_name', sqlalchemy.Text, nullable=True),
#     sqlalchemy.Column('job_id', sqlalchemy.Text, nullable=False),
#     sqlalchemy.Column('task_id', sqlalchemy.Text, nullable=True),
#     sqlalchemy.Column('task_name', sqlalchemy.Text, nullable=True)
# )