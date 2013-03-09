"""
    sqljobs.runner
    ~~~~~~~~~

    This module implements cli, data parsing and validation.

    :copyright: (c) 2013 by Andrey Khobnya.
    :license: MIT, see LICENSE for more details.
"""
from itertools import izip
import simplejson
import validictory

import messages
from json import job_schema
from executor import execute

def run(args):
    if (len(args) == 0) or (len(args) % 2 == 1):
        print(messages.HELP_STRING)
        return
    iterator = iter(args)
    jobs = izip(iterator, iterator)
    for job_path, params_json in jobs:
        try:
            job = simplejson.loads(file_get_contents(job_path))
            validictory.validate(job, job_schema)
            params = simplejson.loads(params_json)
            execute(job, params)
        except Exception, error:
            print(error)
       
    
def file_get_contents(filename):
    with open(filename) as f:
        return f.read()