#! /usr/bin/env python
# coding:utf-8

from glob import glob
import json

list0 = []
for x in glob('/work/halld2/data_monitoring/*'):
  dict0 = {'RunPeriod':x.split('/')[-1]}
  ver_list = []
  for y in glob(x + '/*'):
    dict1 = {'Version':y.split('/')[-1]}
    runlist = []
    for z in glob(y + '/*'):
      runlist.append(z.split('/')[-1])
    dict1['Runs'] = runlist
  ver_list.append(dict1)
  dict0['Versions'] = ver_list
  list0.append(dict0)

print list0

fw = open('test.json', 'w')
json.dump(list0, fw, indent = 4)
