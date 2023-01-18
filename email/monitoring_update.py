#!/apps/bin/python3

import datetime
import os
os.environ["RCDB_HOME"] = "/u/home/gluex/rcdb/"
import sys
sys.path.append("/u/home/gluex/rcdb/python")
import rcdb

import time
import datetime
import urllib.parse

def main():
  db = rcdb.RCDBProvider("mysql://rcdb@hallddb/rcdb")

  # date and time for 24 hours previous
  beginTime = datetime.datetime.now() - datetime.timedelta(days=1) #days=1
  beginRun = 0
  CurrentPeriod = "RunPeriod-2023-01"

  # get first and last runs for the last 24 hours
  rcdb_query = r"daq_run=='PHYSICS_DIRC' and event_count > 500000 and collimator_diameter != 'Blocking'"
  rcdb_query_url = urllib.parse.quote(rcdb_query)
  runs = db.select_runs(rcdb_query, 120000, 129999)
  for run in runs:
    print(run.number)
    print(run.end_time)
    print(beginTime)
    if beginTime is None:
      continue
    if run.end_time > beginTime:
      beginRun = run.number
      break
  endRun = runs[-1].number

  # check for new runs
  if beginRun == 0:
    sys.exit()

  # Prepare text for email (text list: l0)
  l0 = ['https://halldweb.jlab.org/wiki/index.php/Online_Monitoring_Data_Validation\n\n']
  l0.append("Plot browser links for yesterday's runs (since %s)\n" % beginTime.strftime("%Y-%m-%d %H:%M:%S"))
  l0.append('[Runs included]  %d-%d\n' % (beginRun, endRun))
  l0.append('[RCDB query]     %s\n' % rcdb_query)
  l0.append("\n========\n")
  l0.append("Occupancy Macros:\n")

  # set list of histograms titles and names in this list
  hist_names = []
  hist_names.append(["CDC_occupancy", "CDC"])
  hist_names.append(["FDC_occupancy", "FDC"])
  hist_names.append(["FCAL_occupancy", "FCAL"])
  hist_names.append(["BCAL_occupancy", "BCAL"])
  hist_names.append(["PS_occupancy", "PS"])
  hist_names.append(["RF_TPOL_occupancy", "RF & TPOL"])
  hist_names.append(["ST_occupancy", "ST"])
  hist_names.append(["TAGGER_occupancy", "TAGGER"])
  hist_names.append(["TOF_occupancy", "TOF"])
  # hist_names.append(["FMWPC_occupancy", "FMWPC"])
  # hist_names.append(["CTOF_occupancy", "CTOF"])
  hist_names.append(["DigiHits_occupancy", "Hit Multiplicity"])
  # hist_names.append(["DIRC_occupancy", "DIRC South"])
  # hist_names.append(["DIRC_North_occupancy", "DIRC North"])
  # hist_names.append(["DIRC_hit", "DIRC Hits"])
  # hist_names.append(["DIRC_digihit", "DIRC DigiHits"])
  hist_names.append(["CCAL_occupancy", "CCAL occupancy"])
  hist_names.append(["ccal_cluster_et", "CCAL Cluster et"])
  hist_names.append(["ccal_cluster_space", "CCAL Cluster Space"])
  hist_names.append(["ccal_comp2", "CCAL Comp 2"])
  hist_names.append(["ccal_comp", "CCAL Comp"])
  hist_names.append(["ccal_dig_pedestal", "CCAL Digi Pedestal"])
  hist_names.append(["ccal_dig_pulse", "CCAL Digi Pulse"])
  hist_names.append(["ccal_hit_energy", "CCAL Hit Energy"])

  for hist in hist_names:
    l0.append("%s: https://halldweb.jlab.org/data_monitoring/Plot_Browser.html?minRunNum=%d&maxRunNum=%d&RunPeriod=%s&Version=rawdata_ver00&Plot=%s&rcdb_query=%s\n\n" % (hist[1], beginRun, endRun, CurrentPeriod, hist[0], rcdb_query_url))

  l0.append("\n========\n")
  l0.append("\n\n High Level Online Macros:\n")

  # set list of high_level titles and names in this list
  high_level_online_names = []
  high_level_online_names.append(["Beam", "HistMacro_Beam"])
  high_level_online_names.append(["Kinematics", "HistMacro_Kinematics"])
  high_level_online_names.append(["NumHighLevelObjects", "HistMacro_NumHighLevelObjects"])
  high_level_online_names.append(["PID", "HistMacro_PID"])
  high_level_online_names.append(["Trigger", "HistMacro_Trigger"])
  high_level_online_names.append(["Vertex", "HistMacro_Vertex"])

  for hist in high_level_online_names:
    l0.append("%s: https://halldweb.jlab.org/data_monitoring/Plot_Browser.html?minRunNum=%d&maxRunNum=%d&RunPeriod=%s&Version=rawdata_ver00&Plot=%s&rcdb_query=%s\n\n" % (hist[0], beginRun, endRun, CurrentPeriod, hist[1], rcdb_query_url))

  # set list of high_level titles and names in this list
  # high_level_names = []
  # high_level_names.append(["Beam", "Beam"])
  # high_level_names.append(["Vertex", "Vertex"])
  # high_level_names.append(["Trigger", "Trigger"])
  # high_level_names.append(["NumHighLevelObjects", "# HL Obj"])
  # high_level_names.append(["PID", "PID"])
  # high_level_names.append(["Kinematics", "Kinematics"])

  # for hist in high_level_names:
  #   l0.append("%s: https://halldweb.jlab.org/cgi-bin/data_monitoring/monitoring/plotBrowser.py?run1=%d&run2=%d&plot=HistMacro_%s&ver=rawdata_ver00\n\n" % (hist[1], beginRun, endRun, hist[0]))

  with open("/home/gluex/simple_email_list/lists/monitoring_update/message.txt", "w") as f:
    f.writelines(l0)


if __name__=="__main__":
  main()
