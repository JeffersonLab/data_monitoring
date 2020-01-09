#! /apps/bin/python3
# coding:utf-8

import MySQLdb
import sys
import cgitb
cgitb.enable()
import os
os.environ["RCDB_HOME"] = "/group/halld/www/halldweb/html/rcdb_home"
sys.path.append("/group/halld/www/halldweb/html/rcdb_home/python")
import rcdb

db = rcdb.RCDBProvider("mysql://rcdb@hallddb/rcdb")
dbhost = "hallddb.jlab.org"
dbuser = 'datmon'
dbname = 'data_monitoring'
conn = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)

query = ''
RunPeriod = ''
RunMin = 0
RunMax = 99999

for x in sys.argv[1].split('&'):
    if x.startswith('query='):
        query = x.split('=')[1].replace('%3E', '>').replace('%20', ' ')
    elif x.startswith('RunP='):
        RunPeriod = x.split('=')[1]
    elif x.startswith('minRunNum='):
        RunMin = int(x.split('=')[1])
    elif x.startswith('maxRunNum='):
        RunMax = int(x.split('=')[1])

if RunMin == 0 and RunMax == 99999:
    if RunPeriod == "RunPeriod-2019-11":
        RunMin = 70000
        RunMax = 79999
    elif RunPeriod == "RunPeriod-2019-01":
        RunMin = 60000
        RunMax = 69999
    elif RunPeriod == "RunPeriod-2018-08":
        RunMin = 50000
        RunMax = 59999
    elif RunPeriod == "RunPeriod-2018-01":
        RunMin = 40000
        RunMax = 49999
    elif RunPeriod == "RunPeriod-2017-01":
        RunMin = 30000
        RunMax = 39999
    elif RunPeriod == "RunPeriod-2016-10":
        RunMin = 20000
        RunMin = 29999
    elif RunPeriod == "RunPeriod-2016-02":
        RunMin = 10000
        RunMax = 19999

run_list = db.select_runs(query, run_min=RunMin, run_max=RunMax)
if len(run_list) == 0:
    print('NaN')
else:
    print('_'.join([str(x.number) for x in run_list]))

conn.close()
