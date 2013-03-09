"""
    sqljobs.executor
    ~~~~~~~~~

    This module implements core of SQL-Jobs-Util.

    :copyright: (c) 2013 by Andrey Khobnya.
    :license: MIT, see LICENSE for more details.
"""
import imp
import os
import messages

def execute(job, params):
    """Execute job"""
    print(messages.JOB_STARTED % job['title'])
    dbs = ConnectionsHolder(job['databases'])
    for counter, task in enumerate(job['tasks']):
        print(messages.TASK_STARTED % counter)
        execute_task(task, params, 0, dbs)
        print(messages.COMMITING)
        dbs.commit_all()
        print(messages.TASK_COMPLETED % counter)
    print(messages.CLOSING_CONNECTIONS)
    dbs.close_all_connections()
    print(messages.JOB_COMPLETED % job['title'])

def execute_task(task, params, step_number, dbs):
    """Execute all steps of one task of job recursively"""
    step = task[step_number]
    if 'query' in step:
        cursor = dbs.get_connection(step['database']).cursor()
        cursor.execute(
            expand_multiparameter(step['query'], params, dbs.get_placeholder(step['database'])),
            params)
        if cursor.description is not None:
            print(messages.SELECTED_ROWS % cursor.rowcount)
            result = cursor.fetchall()
        else:
            print(messages.AFFECTED_ROWS % cursor.rowcount) 
            result = [params] # send params to next step
        cursor.close()
    elif 'transform' in step:
        script = imp.load_source(
            step['transform'],
            os.path.join(os.getcwd(), step['transform'] + '.py'))
        result = [script.transform(params)]
        print(messages.ROW_TRASFORMED)
    else:
        return
    # check if this is not the last step
    if step_number < len(task) - 1:
        # execute the next step for each row of result
        for row in result:
            execute_task(task, row, step_number + 1, dbs)

""" Multiparameter placeholder """
MULTIPARAM_PLACEHOLDER = '?*'

""" Standart placeholders for different DB drivers """
PLACEHOLDERS = {
    'MySQLdb': '%s',
    'psycopg2': '%s',
    'sqlite3': '?',
    'ibm_db': '%s',
    #TODO: Add more drivers
}

def expand_multiparameter(query, params, placeholder):
    """Replace multiparameter placeholder by sequence of parameters
    placeholders
    """
    if MULTIPARAM_PLACEHOLDER in query:
        return query.replace(
            MULTIPARAM_PLACEHOLDER,
            ','.join([placeholder] * len(params)))
    else:
        return query


class ConnectionsHolder:
    
    def __init__(self, dbs):
        self.dbs = dbs
        
    def get_connection(self, alias):
        if alias in self.dbs:
            if 'connection' not in self.dbs[alias]:
                driver = __import__(self.dbs[alias]['type'])
                self.dbs[alias]['connection'] = driver.connect(**self.dbs[alias]['parameters'])
            return self.dbs[alias]['connection']
        else:
            raise Exception(messages.DB_ALIAS_NOT_FOUND % alias)
    
    def commit_all(self):
        for db in self.dbs.values():
            if 'connection' in db:
                db['connection'].commit()   
        
    def close_all_connections(self):
        for db in self.dbs.values():
            if 'connection' in db:
                db['connection'].close()
        
    def get_placeholder(self, alias):
        if alias in self.dbs:
            if 'placeholder' not in self.dbs[alias]:
                if self.dbs[alias]['type'] in PLACEHOLDERS:
                    self.dbs[alias]['placeholder'] = PLACEHOLDERS[self.dbs[alias]['type']]
                else:
                    raise Exception(messages.DB_UNDEFINED_PLACEHOLDER % alias)
            return self.dbs[alias]['placeholder']
        else:
            raise Exception(messages.DB_ALIAS_NOT_FOUND % alias) 
        