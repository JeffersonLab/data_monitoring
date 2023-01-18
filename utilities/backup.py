#! /apps/bin/python3
# coding:utf-8

import os
import subprocess
from datetime import datetime
import shutil

def main():
  mydir = '/group/halld/www/halldweb/html/data_monitoring/utilities/'
  os.chdir(mydir)

  backup_shell_script = mydir + 'backup.sh'

  output_dir = '/cache/halld/home/gluex/browser_family_backups/'
  output_file = output_dir + datetime.now().strftime('%Y%m%d_%H%M.sql')

  tmp_file = 'tmp_MYDUMP.sql'

  if os.path.exists(tmp_file):
    os.remove(tmp_file)

  subprocess.call([backup_shell_script])
  shutil.move(tmp_file, output_file)


if __name__ == '__main__':
  main()
