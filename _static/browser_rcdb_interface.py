#! /apps/bin/python3
# coding:utf-8

import MySQLdb
import sys
import urllib.parse
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

qs = urllib.parse.parse_qs(sys.argv[1])

if 'minRunNum' not in qs or 'maxRunNum' not in qs:
    if qs['RunP'][0] == "RunPeriod-2019-11":
        qs['minRunNum'] = ['70000']
        qs['maxRunNum'] = ['79999']
    elif qs['RunP'][0] == "RunPeriod-2019-01":
        qs['minRunNum'] = ['60000']
        qs['maxRunNum'] = ['69999']
    elif qs['RunP'][0] == "RunPeriod-2018-08":
        qs['minRunNum'] = ['50000']
        qs['maxRunNum'] = ['59999']
    elif qs['RunP'][0] == "RunPeriod-2018-01":
        qs['minRunNum'] = ['40000']
        qs['maxRunNum'] = ['49999']
    elif qs['RunP'][0] == "RunPeriod-2017-01":
        qs['minRunNum'] = ['30000']
        qs['maxRunNum'] = ['39999']
    elif qs['RunP'][0] == "RunPeriod-2016-10":
        qs['minRunNum'] = ['20000']
        qs['maxRunNum'] = ['29999']
    elif qs['RunP'][0] == "RunPeriod-2016-02":
        qs['minRunNum'] = ['10000']
        qs['maxRunNum'] = ['19999']

run_list = db.select_runs(qs['query'][0], run_min=int(qs['minRunNum'][0]), run_max=int(qs['maxRunNum'][0]))
if len(run_list) == 0:
    print('NaN')
else:
    print('_'.join([str(x.number) for x in run_list]))

conn.close()
