#! /apps/bin/python3
# coding:utf-8

import MySQLdb


# database access
dbhost = 'hallddb.jlab.org'
dbuser = 'monbrowser'
dbname = 'BrowserFamily'
dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)


dbcursor.execute("SELECT FileName FROM PlotTypes")
file_name_list = [x['FileName'] for x in dbcursor.fetchall()]
dbcursor.execute("SELECT Name FROM PlotCategories")
category_list = [x['Name'] for x in dbcursor.fetchall()]
dbcursor.execute("SELECT Name FROM RunPeriods")
runp_list = [x['Name'] for x in dbcursor.fetchall()]

while True:
  while True:
    print('\nInput Run Period [eg.) RunPeriod-2022-05]:')
    runp = input()
    if not runp in runp_list:
      print("\nNo such run periods.")
    else:
      break

  while True:
    print('\nSelect category [' + ' '.join(category_list) + ']:')
    plot_category_name = input()
    if plot_category_name not in category_list:
      print("\nNo such category.")
    else:
      break

  dbcursor.execute("SELECT FileName FROM PlotTypes WHERE ID IN (SELECT PlotType_ID FROM Plots WHERE PlotType_ID IN (SELECT ID FROM PlotTypes WHERE PlotCategory_ID IN (SELECT ID FROM PlotCategories WHERE Name='" + plot_category_name + "')) AND RUN_ID IN (SELECT ID FROM Runs WHERE Version_ID IN (SELECT ID FROM Versions WHERE RunPeriod_ID IN (SELECT ID FROM RunPeriods WHERE Name='" + runp + "'))))")
  filenames = [x['FileName'] for x in dbcursor.fetchall()]

  if len(filenames) == 0:
    print('\nNo .png files found in DB. Exit..')
    exit(0)
  else:
    print('\nFollowing files are found in DB (for Run Period: ' + runp + ' and category: ' + plot_category_name + '):')
    print(filenames)
    print('\nAre you sure to delete these entries from DB? [y/n]')
    answer = input()
    if answer.startswith('y'):
      break
    else:
      exit(0)


dbcursor.execute("DELETE FROM Plots WHERE PlotType_ID IN (SELECT ID FROM PlotTypes WHERE PlotCategory_ID IN (SELECT ID FROM PlotCategories WHERE Name='" + plot_category_name + "')) AND RUN_ID IN (SELECT ID FROM Runs WHERE Version_ID IN (SELECT ID FROM Versions WHERE RunPeriod_ID IN (SELECT ID FROM RunPeriods WHERE Name='" + runp + "')))")

dbcnx.commit()
dbcnx.close()
