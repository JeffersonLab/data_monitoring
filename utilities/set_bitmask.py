#! /apps/bin/python3
# coding:utf-8

import MySQLdb
from glob import glob
import os
import subprocess


# database access
dbhost = 'hallddb.jlab.org'
dbuser = 'monbrowser'
dbname = 'BrowserFamily'
dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)

# There are 2 HistMacro_Matching_TOF2.png in figure_titles, but I don't care.
with open('/group/halld/www/halldweb/htbin/data_monitoring/monitoring/figure_titles') as f:
  l0 = f.readlines()

l1 = [[x.split(',')[0].strip(), x.split(',')[-1].strip()] for x in l0]

for x in l1:
  dbcursor.execute("SELECT * FROM PlotTypes WHERE FileName='%s'" % x[0])
  ID = dbcursor.fetchone()['ID']
  sql = "UPDATE PlotTypes SET bitmask = b'" + x[1] + "' WHERE ID = %d" % ID
  print(sql)
  dbcursor.execute(sql)


dbcnx.commit()
dbcnx.close()
