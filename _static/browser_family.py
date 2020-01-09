#! /apps/bin/python3
# coding:utf-8

import MySQLdb
import sys
import urllib.parse

dbhost = 'hallddb.jlab.org'
dbuser = 'monbrowser'
dbname = 'BrowserFamily'
dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)

qs = urllib.parse.parse_qs(sys.argv[1])
dbcursor.execute(qs['query'][0])
print(str(list(dbcursor.fetchall())).replace("'", '"'))

dbcnx.close()
