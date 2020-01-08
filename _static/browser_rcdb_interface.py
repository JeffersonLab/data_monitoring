import time
import glob
import rcdb
import os.path
import os
import re
import MySQLdb
import sys
import cgi
import cgitb
cgitb.enable()


os.environ["RCDB_HOME"] = "/group/halld/www/halldweb/html/rcdb_home"
sys.path.append("/group/halld/www/halldweb/html/rcdb_home/python")

#from os import listdir
#from os.path import isfile, join

db = rcdb.RCDBProvider("mysql://rcdb@hallddb/rcdb")

dbhost = "hallddb.jlab.org"
dbuser = 'datmon'
dbpass = ''
dbname = 'data_monitoring'

conn = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
curs = conn.cursor(MySQLdb.cursors.DictCursor)


def main(argv):

    query = ""
    RunPeriod = ""
    RunMin = 0
    RunMax = 99999
    if len(argv) != 0:
        query = argv[0]
        RunPeriod = argv[1]

    if(RunPeriod == "RunPeriod-2019-11"):
        RunMin = 70000
        RunMax = 79999
    elif(RunPeriod == "RunPeriod-2019-01"):
        RunMin = 60000
        RunMax = 69999
    elif(RunPeriod == "RunPeriod-2018-08"):
        RunMin = 50000
        RunMax = 59999
    elif(RunPeriod == "RunPeriod-2018-01"):
        RunMin = 40000
        RunMax = 49999
    elif(RunPeriod == "RunPeriod-2017-01"):
        RunMin = 30000
        RunMax = 39999
    elif(RunPeriod == "RunPeriod-2016-10"):
        RunMin = 20000
        RunMin = 29999
    elif(RunPeriod == "RunPeriod-2016-02"):
        RunMin = 10000
        RunMax = 19999
    else:
        RunMin = 0
        RunMax = 99999

    approvedRuns = []
    approvedRuns = db.select_runs(query, run_min=RunMin, run_max=RunMax)
    approvedRunsRev = approvedRuns[::-1]
    approvedList = ""

    for ar in approvedRuns:
        approvedList = approvedList+str(ar.number)+"_"
    approvedList = approvedList[:-1]

    print approvedList

    conn.close()


if __name__ == "__main__":
    main(sys.argv[1:])
