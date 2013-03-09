"""
    sqljobs.messages
    ~~~~~~~~~

    This module contains constants for text messages.

    :copyright: (c) 2013 by Andrey Khobnya.
    :license: MIT, see LICENSE for more details.
"""
HELP_STRING = 'Usage: sql_jobs_run <path_to_job> <params_in_json> [<path_to_job2> <params_in_json2> ...]'
JOB_STARTED = 'Executing job "%s":'
JOB_COMPLETED = 'Job "%s" has been completed'
TASK_STARTED = '  Executing task "%d":'
TASK_COMPLETED = '  Task "%d" has been completed'
ROW_TRASFORMED = '    row has been transformed'
DB_ALIAS_NOT_FOUND = 'Database with alias "%s" is not defined in "databases" section of job!'
DB_UNDEFINED_PLACEHOLDER = 'Undefined placeholder for database with alias "%s"'
SELECTED_ROWS = '    rows selected: %d '
AFFECTED_ROWS = '    rows affected: %d'
COMMITING = '    commiting all changes'
CLOSING_CONNECTIONS = '  Closing connections'