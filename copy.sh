#!/bin/bash

cp Plot_Browser.html /group/halld/www/halldweb/html/data_monitoring/
rm -rf /group/halld/www/halldweb/html/data_monitoring/_static
cp -r _static /group/halld/www/halldweb/html/data_monitoring/
cp htbin/data_monitoring/monitoring/runBrowser.py /group/halld/www/halldweb/htbin/data_monitoring/monitoring/
cp ../my_sql_tables/add_filename.py /group/halld/www/halldweb/htbin/data_monitoring/monitoring/
