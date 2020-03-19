# Scripts for Hall D data monitoring

See `/group/halld/www/halldweb/html/data_monitoring/`.

## [Plot Browser](https://halldweb.jlab.org/data_monitoring/Plot_Browser.html)

## [Run Browser](https://halldweb.jlab.org/cgi-bin/data_monitoring/monitoring/runBrowser.py)

A symbolic link `/group/halld/www/halldweb/htbin/data_monitoring/monitoring/runBrowser.py` should be prepared which points to `/group/halld/www/halldweb/html/data_monitoring/htbin/data_monitoring/monitoring/runBrowser.py`.

## Cron scripts
### `email/montoring_update.py` for sending out monitoring update plots
### `utilities/update_browser_family.py` for updating database for Plot Browser

crontab for gluex@jlabl5

```
#
# ccdb sqlite version management
#     create new versions
0 0 * * * /home/gluex/bin/ccdb_sqlite_create.sh 
#     delete old versions
0 0 * * * cd /group/halld/Software/calib/ccdb_sqlite ; find . \( \( -atime +7 -not -name \*07.sqlite -not -name \*14.sqlite -not -name \*21.sqlite -not -name \*28.sqlite \) -o \( -atime +30 -not -name \*07.sqlite \) -o -atime +365 \) -exec rm {} \;
#
# update ccdb users from NIS tables
#
0 0 * * * /home/gluex/bin/ccdb_update_users.sh
#
# send out monitoring update plots
#
MAILTO="keigo@jlab.org"
0  5 * * * /group/halld/www/halldweb/html/data_monitoring/email/monitoring_update.py ; cd /home/gluex/simple_email_list/lists/monitoring_update ; ../../scripts/simple_email_list.pl
0 17 * * * /group/halld/www/halldweb/html/data_monitoring/email/monitoring_update.py ; cd /home/gluex/simple_email_list/lists/monitoring_update ; ../../scripts/simple_email_list.pl

# Updates database.
*/5  *  *  *  *  /group/halld/www/halldweb/html/data_monitoring/utilities/update_browser_family.py >> /group/halld/www/halldweb/html/data_monitoring/utilities/cron.log 2>&1
```
