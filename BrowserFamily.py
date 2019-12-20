#! /usr/bin/env python3
# coding:utf-8

import MySQLdb
import json

# database access
dbhost = 'hallddb.jlab.org'
dbuser = 'monbrowser'
dbname = 'BrowserFamily'
dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)

list0 = []
dbcursor.execute("SELECT * FROM RunPeriods")
runp_tup = dbcursor.fetchall()
for x in sorted(runp_tup, key=lambda x: x['Name'], reverse=False):
    dict0 = {'RunPeriod': x['Name']}
    ver_list = []
    dbcursor.execute("SELECT * FROM Versions where RunPeriod_ID=%d" % x['ID'])
    ver_tup = dbcursor.fetchall()
    for y in sorted(ver_tup, key=lambda x: x['Type'] + '%02d' % x['VersionNumber'], reverse=False):
        dict1 = {'Version': y['Type'] + '_ver%02d' % y['VersionNumber']}
        runlist = []
        dbcursor.execute("SELECT * FROM Runs where Version_ID=%d" % y['ID'])
        run_tup = dbcursor.fetchall()
        for z in sorted(run_tup, key=lambda x: x['RunNumber'], reverse=False):
            runlist.append('Run%06d' % z['RunNumber'])
        dict1['Runs'] = runlist
        if dict1['Runs']:
            ver_list.append(dict1)
    dict0['Versions'] = ver_list
    list0.append(dict0)

dbcnx.close()

with open('test2.json', 'w') as f:
    f.write(json.dumps(list0))
