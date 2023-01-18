#! /usr/bin/env bash

mysqldump -h hallddb -u monbrowser BrowserFamily > tmp_MYDUMP.sql

##  Thomas created a database 'BrowserFamily' on the server 'hallddb.jlab.org'
##
##  The following command dumps the database.
##  $ mysqldump -h hallddb -u monbrowser BrowserFamily > MYDUMP.sql
##
##  To recover ..
##  $ mysql -h hallddb -u monbrowser BrowserFamily < MYDUMP.sql
##
##  # where the cron is working?
##  gluex@ifarm1901
