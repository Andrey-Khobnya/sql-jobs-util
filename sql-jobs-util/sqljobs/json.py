"""
    sqljobs.json
    ~~~~~~~~~

    This module contains json schema to validate jobs.

    :copyright: (c) 2013 by Andrey Khobnya.
    :license: MIT, see LICENSE for more details.
"""
job_schema = {
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,
            'required': True
        },
        'databases': {
            'type': 'object',
            'patternProperties': {
                '.*': {
                    'type': 'object',
                    'properties': {
                        'type': {
                            'type': 'string',
                            'required': True
                        },
                        'parameters': {
                            'type': 'object',
                        },
                        'placeholder': {
                            'type': 'string',
                            'minLength': 1,
                            'required': False
                        }
                    }
                }
            },
            'required': True
        },
        'tasks': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': [
                        {
                            'type': 'object',
                            'properties': {
                                'database': {'type': 'string', 'required': True},
                                'query': {'type': 'string', 'required': True}
                            }
                        },
                        {
                            'type': 'object',
                            'properties': {
                                'transform': {'type': 'string', 'required': True}
                            }
                         }
                    ]
                }
            }
        }
    }
}