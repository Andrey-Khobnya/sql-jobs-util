# SQL-Jobs-Util 

SQL-Jobs-Util is the simple tool to execute SQL jobs for data migration and/or data 
transfer between multiple database servers. It allows execute chains of SQL queries 
using results of previous queries as parameters for following queries.

Chains of SQL queries are grouped into *tasks*. Each task is executed in separate 
transaction if database server supports transactions. One query is one *step* of  
task. Step can use result of previous step as query parameters. Steps are executed 
recursively. It means that if query returns several rows of result step will be 
executed several times, one for each row. Input parameters of current step are sent 
to next step if query of current step doesn't return any result. Also there are steps 
which does not execute any SQL query but transform data and send it to following 
steps. Tasks are grouped into *jobs*. Each job is contained in separate JSON file 
and must serve one purpose.

## Installation

Run as administrator:

```bash
$ python setup.py install
```

Or you can do it in your [virtualenv](http://www.virtualenv.org/en/latest/)

Than install drivers for database servers you use. Use drivers which provide PEP 249  
support. For example, for MySQL you can use:

```bash
$ pip install python-mysql
```

## Usage

```bash
$ sql_jobs_run <path_to_job> <params_in_json> [<path_to_job2> <params_in_json2> ...]
```

Parameters in JSON format. 

## How to write jobs

See examples below. Note that it is necessary to use placeholders supported by specific 
driver. Also you can use special placeholder ?* that expanded in several placeholders 
depending on the number of parameters. SQL-Jobs-Util provide this type of placeholder 
for drivers *MySQLdb*, *psycopg2*, *sqlite3* and *ibm_db*. If you would like to use 
any other drivers you should define standard placeholder in *placeholder* property for 
particular database in *databases* section of job file.

## Job examples 

Simple job for copy one parent and several child records from one database to another:

```javascript
{
	"title": "Just copy `entity` from db `A` to db `B`",
	"databases": {
		"db_A": {
			"type": "MySQLdb",
			"parameters": {
				"host": "172.168.0.1",
				"user": "root",
				"passwd": "password",
				"db": "a",
				"charset": "utf8"
			}
		},
		"db_B": {
			"type": "MySQLdb",
			"parameters": {
				"host": "172.168.0.2",
				"user": "root",
				"passwd": "password",
				"db": "b",
				"charset": "utf8"
			}
		}
	},
	"tasks": [
		[
			{
				"database": "db_A",
				"query": "SELECT * FROM entities WHERE id = %(id)s"
			},
			{
				"database": "db_B",
				"query": "INSERT INTO entities VALUES (?*)"				
			}
		],
		[
			{
				"database": "db_A",
				"query": "SELECT * FROM properties WHERE entity_id = %(id)s"
			},
			{
				"database": "db_B",
				"query": "INSERT INTO properties VALUES (?*)"				
			}
		]
	]
}
```

```bash
$ sql_jobs_run simple_copy_job1.json "{\"id\": \"2\"}"
```

Example with simple data transformation.

calculate_crc_job.json:

```javascript
{
	"title": "Calculate CRC-32 of first column of `entity` of db `A` and insert into `hashes` of db `B` and db `C`",
	"databases": {
		"db_A": {
			"type": "MySQLdb",
			"parameters": {
				"host": "172.168.0.1",
				"user": "root",
				"passwd": "password",
				"db": "a",
				"charset": "utf8"
			}
		},
		"db_B": {
			"type": "MySQLdb",
			"parameters": {
				"host": "172.168.0.2",
				"user": "root",
				"passwd": "password",
				"db": "b",
				"charset": "utf8"
			}
		},
		"db_C": {
			"type": "MySQLdb",
			"parameters": {
				"host": "172.168.0.3",
				"user": "root",
				"passwd": "password",
				"db": "c",
				"charset": "utf8"
			}
		}
	},
	"tasks": [
		[
			{
				"database": "db_A",
				"query": "SELECT * FROM entities WHERE id = %(id)s"
			},
			{
				"transform": "calculate_crc"
			},
			{
				"database": "db_B",
				"query": "INSERT INTO hashes VALUES (?*)"				
			},
			{
				"database": "db_C",
				"query": "INSERT INTO hashes VALUES (?*)"				
			}
		]
	]
}
```

calculate_crc.py:

```python
""" Transformer for calculating CRC of second column """
import zlib

def transform(row):
    return (row[0], '%X' % zlib.crc32(row[1]))
```
