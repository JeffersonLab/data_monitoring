#!/bin/bash

date
source $HOME/env_monitoring_launch.sh
export PATH=/site/bin:${PATH} #because .login isn't executed, and need this path for SWIF
cd /group/halld/www/halldweb/html/data_monitoring/run_statistics/RunPeriod-2019-01/
python plot_rcdb3_WB.py


