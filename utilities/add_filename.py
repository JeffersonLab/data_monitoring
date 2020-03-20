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

while True:
  while True:
    print('\nInput filename [*.png]:')
    filename = input()
    if not filename.endswith('.png'):
      print("\nThe filename does not end with '.png'.")
    elif filename in file_name_list:
      print("\nThis file is already registered in the database.")
      exit(0)
    else:
      break

  print('\nInput display name [eg.) FCAL Invariant Mass]:')
  display_name = input()

  while True:
    print('\nSelect category [' + ' '.join(category_list) + ']:')
    plot_category_name = input()
    if plot_category_name not in category_list:
      print("\nNo such category.")
    else:
      break

  print('\nIs the following info. correct? [y/n]')
  print('[filename    ]', filename)
  print('[display name]', display_name)
  print('[category    ]', plot_category_name)
  answer = input()
  if answer.startswith('y'):
    break


dbcursor.execute("SELECT ID FROM PlotCategories WHERE Name='" + plot_category_name + "'")
ID = dbcursor.fetchone()['ID']

sql = "INSERT INTO PlotTypes (FileName, DisplayName, PlotCategory_ID) VALUES ('" + filename + "', '" + display_name + "', " + str(ID) + ")"
print(sql)
dbcursor.execute(sql)

dbcnx.commit()
dbcnx.close()
