#!/bin/bash

date
source $HOME/env_monitoring_launch.sh
export PATH=/site/bin:${PATH} #because .login isn't executed, and need this path for SWIF
cd /group/halld/www/halldweb/html/data_monitoring/run_statistics/RunPeriod-2019-11/
which python
/apps/bin/python plot_rcdb3_WB.py

