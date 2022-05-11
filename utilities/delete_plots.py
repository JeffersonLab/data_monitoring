#! /apps/bin/python3
# coding:utf-8

import MySQLdb


def delete_one_plot():
  # database access
  dbhost = 'hallddb.jlab.org'
  dbuser = 'monbrowser'
  dbname = 'BrowserFamily'
  dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
  dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)


  dbcursor.execute("SELECT FileName FROM PlotTypes")
  file_name_list = [x['FileName'] for x in dbcursor.fetchall()]
  dbcursor.execute("SELECT Name FROM RunPeriods")
  runp_list = [x['Name'] for x in dbcursor.fetchall()]

  while True:
    while True:
      print('\nInput Run Period [eg.) RunPeriod-2022-05]:')
      runp = input()
      if not runp in runp_list:
        print("\nNo such run period.")
      else:
        break

    while True:
      print('\nInput filename [eg.) bcal_occupancy.png]:')
      filename = input()
      if not filename in file_name_list:
        print("\nNo such filename.")
      else:
        break

    print('\n' + filename + ' for ' + runp + ' will be deleted.')
    print('\nAre you sure to delete this entry from DB? [y/n]')
    answer = input()
    if answer.startswith('y'):
      break
    else:
      exit(0)


  dbcursor.execute("DELETE FROM Plots WHERE PlotType_ID IN (SELECT ID FROM PlotTypes WHERE BINARY FileName='" + filename + "') AND RUN_ID IN (SELECT ID FROM Runs WHERE Version_ID IN (SELECT ID FROM Versions WHERE RunPeriod_ID IN (SELECT ID FROM RunPeriods WHERE Name='" + runp + "')))")

  dbcnx.commit()
  dbcnx.close()


def delete_one_category():
  # database access
  dbhost = 'hallddb.jlab.org'
  dbuser = 'monbrowser'
  dbname = 'BrowserFamily'
  dbcnx = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
  dbcursor = dbcnx.cursor(MySQLdb.cursors.DictCursor)


  dbcursor.execute("SELECT Name FROM PlotCategories")
  category_list = [x['Name'] for x in dbcursor.fetchall()]
  dbcursor.execute("SELECT Name FROM RunPeriods")
  runp_list = [x['Name'] for x in dbcursor.fetchall()]

  while True:
    while True:
      print('\nInput Run Period [eg.) RunPeriod-2022-05]:')
      runp = input()
      if not runp in runp_list:
        print("\nNo such run period.")
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


def main():
  func_flag = 0
  while True:
    print('\nWhich do you want to delete? Type 1 or 2.  [1: just one plot,  2: one category]:')
    str_func_flag = input()
    func_flag = int(str_func_flag)
    if func_flag != 1 and func_flag != 2:
      print("\nInvalid Type.")
    else:
      break

  if func_flag == 1:
    delete_one_plot()
  else:
    delete_one_category()


if __name__ == '__main__':
  main()
