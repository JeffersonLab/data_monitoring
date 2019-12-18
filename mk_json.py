#! /usr/bin/env python
# coding:utf-8

from glob import glob
import json

list0 = []
for x in sorted(glob('/work/halld2/data_monitoring/RunPeriod-*')):
  dict0 = {'RunPeriod':x.split('/')[-1]}
  ver_list = []
  for y in glob(x + '/*'):
    dict1 = {'Version':y.split('/')[-1]}
    runlist = []
    for z in glob(y + '/Run*'):
      runlist.append(z.split('/')[-1])
    dict1['Runs'] = sorted(runlist)
    if dict1['Runs']:
      ver_list.append(dict1)
  dict0['Versions'] = ver_list
  list0.append(dict0)

with open('test.json', 'w') as f:
  f.write(json.dumps(list0))
