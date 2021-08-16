#! /apps/bin/python3
# coding:utf-8

import MySQLdb


# database access
dbhost = 'hallddb.jlab.org'
dbuser = 'monbrowser'
dbname = 'BrowserFamily'
dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)


dbcursor.execute("SELECT Name FROM PlotCategories")
category_list = [x['Name'] for x in dbcursor.fetchall()]

print('\nInput a new category name:')
category_name = input()

if category_name != category_name.upper():
  print("\nLower cases cannot be used for category names.")
  exit(0)
if category_name in category_list:
  print("\nThis name already exists.")
  exit(0)

sql = "INSERT INTO PlotCategories (Name) VALUES ('" + category_name + "')"
print(sql)
dbcursor.execute(sql)

dbcnx.commit()
dbcnx.close()
