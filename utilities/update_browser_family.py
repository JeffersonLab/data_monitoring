#! /apps/bin/python3
# coding:utf-8

import MySQLdb
from glob import glob
import os
from datetime import datetime
from datetime import timedelta
import subprocess

numprocesses_running = int(subprocess.check_output(["echo `ps all -u gluex | grep update_browser_family.py | grep -v grep | wc -l`"], shell=True))
if numprocesses_running > 2:
    print('[Error] too many processes', numprocesses_running)
    exit(0)

ignore_path = '/group/halld/www/halldweb/html/data_monitoring/utilities/'

# Time string for updating ignore.txt at the end of this code.
time_str = 'time_stamp ' + (datetime.now() + timedelta(minutes=-3)).strftime('%Y-%m-%d %H:%M') + '\n'

ignore_list2 = []  # for new ignore_time_stamp.txt
ignore_list2.append("# Following directive specifies 'time_stamp'.\n")
ignore_list2.append("# Files whose time stamp is smaller than the specified value will be ignored in update_browser_family.py.\n")
ignore_list2.append("# Format: YYYY-mm-dd HH:MM\n")
ignore_list2.append("# Empty lines and lines starting with '#' will be skipped.\n\n")
ignore_list2.append(time_str)

# Sets ignore_list and time_stamp
with open(ignore_path + 'ignore_runperiod.txt') as f:
    ignore_list0 = f.readlines()

with open(ignore_path + 'ignore_time_stamp.txt') as f:
    ignore_list1 = f.readlines()


time_stamp = -1.0
ignore_list = []
for x in ignore_list0:
    if len(x.strip()) == 0 or x.strip().startswith('#'):
        continue
    ignore_list.append(x.strip())

for x in ignore_list1:
    if len(x.strip()) == 0 or x.strip().startswith('#'):
        continue
    if x.split()[0] == 'time_stamp':
        time_stamp = datetime.strptime(x.split()[1] + ' ' + x.split()[2], '%Y-%m-%d %H:%M').timestamp()
    else:
        ignore_list.append(x.strip())

# database access
dbhost = 'hallddb.jlab.org'
dbuser = 'monbrowser'
dbname = 'BrowserFamily'
dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)

for x in glob('/work/halld2/data_monitoring/RunPeriod-*'):
    runp = x.split('/')[-1]
    if runp in ignore_list: continue
    if os.stat(x).st_mtime > time_stamp:
        sql = "INSERT IGNORE INTO RunPeriods (Location_ID, Name) VALUES (1, '" + runp + "')"
        print(x, sql)
        dbcursor.execute(sql)

    # Retrieves runpID.
    dbcursor.execute("SELECT ID FROM RunPeriods WHERE Name='" + x.split('/')[-1] + "'")
    runpID = dbcursor.fetchone()['ID']

    for y in glob(x + '/*_ver??'):
        ver = y.split('/')[-1]
        ver_type = ver.split('_')[0]
        ver_num = int(ver.split('_ver')[1])
        if ver_type == 'mc': continue  ## added to avoid crash (9-Aug-2021)
        if os.stat(y).st_mtime > time_stamp:
            sql = "INSERT IGNORE INTO Versions (RunPeriod_ID, Type, VersionNumber) VALUES (%d, '" % runpID + ver_type + "', %d)" % ver_num
            print(y, sql)
            dbcursor.execute(sql)

        # Retrieves verID.
        dbcursor.execute("SELECT ID FROM Versions WHERE RunPeriod_ID=%d" % runpID + " and Type='" + ver_type + "' and VersionNumber=%d" % ver_num)
        verID = dbcursor.fetchone()['ID']

        for z in glob(y + '/Run*'):
            runnum = int(z.split('/')[-1].split('Run')[1])
            if os.stat(z).st_mtime > time_stamp:
                sql = "INSERT IGNORE INTO Runs (RunNumber, Version_ID) VALUES (%d, %d)" % (runnum, verID)
                print(z, sql)
                dbcursor.execute(sql)

            # Retrieves runID.
            dbcursor.execute("SELECT * FROM Runs WHERE Version_ID=%d" % verID + " and RunNumber=%d" % runnum)
            runID = dbcursor.fetchone()['ID']

            for w in glob(z + '/*.png'):
                if os.stat(w).st_mtime < time_stamp: continue
                dbcursor.execute("SELECT * FROM PlotTypes WHERE binary FileName='" + w.split('/')[-1] + "'")
                type_list = dbcursor.fetchall()
                if len(type_list) != 1: continue
                sql = "INSERT IGNORE INTO Plots (Run_ID, PlotType_ID) VALUES (%d, %d)" % (runID, int(type_list[0]['ID']))
                print(w, sql)
                dbcursor.execute(sql)


dbcnx.commit()
dbcnx.close()


## Updates time_stamp in ignore_time_stamp.txt.
with open(ignore_path + 'ignore_time_stamp.txt', 'w') as f:
    f.writelines(ignore_list2)
print('[ignore_time_stamp.txt updated]', time_str)
