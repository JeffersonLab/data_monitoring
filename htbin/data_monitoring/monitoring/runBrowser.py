#! /usr/bin/env python
# coding:utf-8

import MySQLdb
import cgi
import cgitb
cgitb.enable()

import datetime
import re

import os
os.environ["RCDB_HOME"] = "/group/halld/www/halldweb/html/rcdb_home"
import sys
sys.path.append("/group/halld/www/halldweb/html/rcdb_home/python")
import rcdb
import glob

db = rcdb.RCDBProvider("mysql://rcdb@hallddb/rcdb")

dbhost = "hallddb.jlab.org"
dbuser = 'datmon'
dbpass = ''
dbname = 'data_monitoring'

conn = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
curs = conn.cursor()

# get data from the database
# if an interval is passed,
# return a list of records from the database
def get_data(options):

    revision_str = str(options[1])
    revision = int(re.search(r'\d+', revision_str).group())

    query = "SELECT distinct r.run_num, r.start_time, r.num_events FROM run_info r, version_info v, bcal_hits b WHERE b.runid=r.run_num and v.version_id=b.version_id and run_num>0 and revision=%s and run_period=%s ORDER BY r.run_num"
    print revision
    print str(options[2])
    curs.execute(query, (revision, str(options[2])))
    rows = curs.fetchall()
    return rows


# get list of versions from the DB
def get_versions(options):

    query = "SELECT revision, data_type, production_time, run_period from version_info where run_period=%s ORDER BY version_id DESC"
    curs.execute(query, [str(options[2])])
    rows = curs.fetchall()

    return rows


# get list of periods from the DB
def get_periods(options):

    query = "SELECT DISTINCT run_period from version_info ORDER BY run_period DESC"
    curs.execute(query)
    rows = curs.fetchall()
    rowstoreturn = []

    for i in range(0, len(rows)-1):
        rowstoreturn.append(rows[i])

    return rowstoreturn


# get period for given run_number from the DB
def get_periods_run_number(options):

    query = "SELECT DISTINCT run_period from version_info v, run_info r, bcal_hits b WHERE b.runid=r.run_num and v.version_id=b.version_id and r.run_num=%s ORDER BY run_period DESC"
    curs.execute(query, [str(options[0])])
    rows = curs.fetchall()

    return rows


# get dates to list on runBrowser page
def get_dates(options):

    revision_str = str(options[1])
    revision = int(re.search(r'\d+', revision_str).group())
    #revision_str = revision_str.replace("ver","")
    #revision = int(float(revision_str))
    query = "SELECT DISTINCT DATE(r.start_time) FROM run_info r, version_info v WHERE run_num>0 and start_time>'2014-11-01' and revision=%s and run_period=%s ORDER BY DATE(start_time)"
    curs.execute(query, (revision, str(options[2])))
    rows = curs.fetchall()

    return rows


# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"


# print the HTML head section with java script for handling histogram display
def printHTMLHead(title):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    print """
     <style>
	  div.link-list {
          width:20.0em;
	  height: 98%;
	  position:absolute;
          padding-left:1%;
          padding-right:1%;
          margin-left:0;
          margin-right:0;
	}
	#main {
	  height: 101%;
          margin-left:21.0em;
          padding-left:1em;
          padding-right:2em;
	  overflow-y: scroll;
	}
	#nav {
          left:0;
	  overflow-y: scroll;
	}

        /* Menu styles */
        .link-list ul
        {
        margin:0px;
        padding:0px;
        }
        .link-list li
        {
        margin:0px 0px 0px 5px;
        padding:0px;
        list-style-type:none;
        text-align:left;
        font-weight:normal;
        }

        /* Symbol styles */
        .link-list .symbol-item,
        .link-list .symbol-open,
        .link-list .symbol-close
        {
        float:left;
        width:16px;
        height:1em;
        background-position:left center;
        background-repeat:no-repeat;
        }
        .link-list .symbol-open  { background-image:url(https://halldweb.jlab.org/data_monitoring/js/runBrowser/icons/minus.png); }
        .link-list .symbol-close { background-image:url(https://halldweb.jlab.org/data_monitoring/js/runBrowser/icons/plus.png);}

        /* Menu line styles */
        .link-list li.open  { font-weight:bold; }
        .link-list li.close { font-weight:normal; }
      
        .header .sign:after{
        content:"+";
        display:inline-block;      
        }
        .header.expand .sign:after{
         content:"-";
        }

        </style>
"""

    print "<script src=\"https://halldweb.jlab.org/data_monitoring/js/runBrowser/TreeMenu.js\" type=\"text/javascript\"></script>"
    print "<script src=\"https://halldweb.jlab.org/data_monitoring/js/jquery.js\" type=\"text/javascript\"></script>"

    print """
      <script type="text/javascript">
	       
	var freeze = false;
	
        function showPlot()
	{
          if(document.getElementById("plotToShow").value != "none")
          {
	  var imgsrc = document.getElementById("folderPath").innerHTML;//"https://halldweb.jlab.org/work/halld2/data_monitoring/"		
	  imgsrc += document.getElementById("plotToShow").value;
	  imgsrc += ".png";

          document.getElementById('imageshow').src=imgsrc;
          document.getElementById('imageshow').style.display='block';
          }
        }

        function freezeIt()
        {
          if(freeze) {freeze = false;}
          else 
          {
          freeze = true;
          }
        }


        function updatePlot(name)
        {
         if(!freeze)
             document.getElementById("plotToShow").value=name;
        }
    </script>

      <script>
         function toggleRows(id)
         {
           var e = document.getElementById(id);
            if(e.style.display == 'none')
              e.style.display = 'block';
            else
              e.style.display = 'none';
           
         }
      </script>

      <script>
      function changeText(id,text)
      {
       document.getElementById(id).innerHTML = text;
      }
      </script>
      
      <script>
        function changePeriod()
	{
           $("#ver").load("/data_monitoring/textdata/" + $(this.period).val() + ".txt");
        }
      </script>
       <script>
       function checkPeriod()
       {
        if($(this.period).val()=="RunPeriod-2018-01")
          return 1;
        else
          return 0;
       }
      </script>
      <script>
        function changeRunList(options)
        {
	
            var Options=options;
            
            var RUNLIST = document.getElementById("runList");
            var listItem = RUNLIST.getElementsByTagName("li");

            /*for(var i=0; i<listItem.length ;i++)
            {
                 //listItem[i].innerHTML="hello"+i;
            }*/
	
	/*var txtFile = new XMLHttpRequest();
	txtFile.open("GET", "/u/group/halld/www/halldweb/htbin/data_monitoring/monitoring/file.txt", true);
	console.log(txtFile.readyState);
	txtFile.onreadystatechange = function() {
      if (txtFile.readyState === 4) {  // Makes sure the document is ready to parse
        if (txtFile.status === 200) {  // Makes sure it's found the file
          text = txtFile.responseText;
          console.log(text);
        }
      }
    }*/
	
      }
      </script>

      <script>
        function help_function()
         {
           alert('1. Toggle your Run Period/Version \\n2. Click Show Runs \\n3. Select a run \\n4. Click show plots');
         }
      </script>
      <script>
        function changePath()
        {
            var runpth="./";
            var linkpth="https://halldweb.jlab.org/cgi-bin/data_monitoring/monitoring/runBrowser.py?";
            var Period = document.getElementById("period");
            var Periodstr = Period.options[Period.selectedIndex].text;

            var Version = document.getElementById("ver");
            var Versionstr = Version.options[Version.selectedIndex].value;


           if(Periodstr !=  "None" )
             {
              linkpth="https://halldweb.jlab.org/cgi-bin/data_monitoring/monitoring/runBrowser.py?";
              linkpth+="period=";
              linkpth+=Periodstr;
              linkpth+="&ver=";
              linkpth+=Versionstr;
              linkpth+="&run_number=";

              runpth = "/work/halld2/data_monitoring/";
              runpth += Periodstr;
              runpth += "/";
              runpth += Versionstr
              runpth += "/Run";
              var length = ($(this.run_number).val()).length;
              for(var i=0;i<6-length;i++)
              {
                runpth += "0";
                linkpth+= "0";
              }
            linkpth+=$(this.run_number).val();
            runpth += $(this.run_number).val();
            runpth += "/";
             }
           document.getElementById("folderPath").innerHTML=runpth;
           document.getElementById("linkPath").innerHTML=linkpth;
        }
      </script>

      <script>
        function changeRun(run, runNumber)
	{
           document.getElementById('run_number').value = "0"
           document.getElementById('run_number').value += run
           myVar = "Run "+runNumber+":"
           changeText("RunLine",myVar)
        }
      </script>
"""


def print_version_selector(options):
    print """<form action="/cgi-bin/data_monitoring/monitoring/runBrowser.py" method="POST">"""

    periods = get_periods(options)
    print "<select id=\"period\" name=\"period\" onChange=\"changePeriod();changePath();\">"
    for period in periods:
        if period[0] == "RunPeriod-2015-01":
            continue
        print "<option value=\"%s\" " % (period[0])
        if options != None and period[0] == options[2]:
            print "selected"
        print "> %s</option>" % (period[0])
    print "</select>"

    recon_versions = []

    versions = get_versions(options)
    print "<select id=\"ver\" name=\"ver\" onChange=\"changeRunList(options);changePath();showPlot();\">"
    for version in versions:
        revision = ("ver%02d" % version[0])
        data_type = version[1]
        production_time = version[2]
        full_version_name = "%s_%s" % (data_type, revision)
        if version[0] not in recon_versions or data_type != "recon":
            print "<option value=\"%s\" " % full_version_name
        if options != None and full_version_name == options[1]:
            if data_type != "recon":
                print "selected"
            elif version[0] not in recon_versions:
                print "selected"
        version_name = ""
        if version[0] == 0 and data_type == "rawdata":
            version_name = "RootSpy"
        elif data_type == "mon":
            if version[0] == 1:
                version_name = "Incoming Data"
            else:
                version_name = "Monitoring Launch "
                version_name += production_time
        elif data_type == "recon":
            if version[0] in recon_versions:
                print "> %s %s</option>" % (revision, version_name)
                continue
            version_name = "Recon Launch "
            version_name += production_time
            recon_versions.append(version[0])
        elif data_type == "mc":
            version_name = "MC Production "
            version_name += production_time
        print "> %s %s</option>" % (revision, version_name)

    print "</select>"

    print "<input type=\"submit\" value=\"Show Runs\" />"
    print "<input type=\"submit\" value=\"Show Plots\" />"
    print "Link displays plots or <button type=\"button\"> ROOT </button> opens file"
    print "<br>"
    print "<button onclick=\"help_function()\"> Help </button>"
    print "<br><br>"


# def newprint_run_selector(options)
def print_run_selector(records, options, row):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rcdb_inelig = ['detcom_02', 'RunPeriod-2014-10',
                   'RunPeriod-2015-03', 'RunPeriod-2015-06', 'RunPeriod-2015-12']
    print "<ul id=\"runList\">"
    dates = get_dates(options)

    runmin = 40000
    runmax = 49999

    if options[2] == "RunPeriod-2016-10":
        runmin = 20000
        runmax = 29999
    elif options[2] == "RunPeriod-2016-02":
        runmin = 10000
        runmax = 19999
    elif options[2] == "RunPeriod-2017-01":
        runmin = 30000
        runmax = 39999

    if options[2] in rcdb_inelig or options[2] == "RunPeriod-2018-01":
        rcdb_runs = db.get_runs(runmin, runmax)
    else:
        rcdb_runs = db.select_runs(
            "@status_approved and @is_production", runmin, runmax)

    rcdb_run_numbers = [run.number for run in rcdb_runs]

    if "mc_ver01" in options:
        newText = "MC"
        print ("<label><input type=\"radio\" id=\"run_number\" name=\"run_number\" value=\"%s\" onclick=\"changeRun(%s,%s);\"> %s</label>" %
               (10000, 10000, "MC_run", 10000))
        return

    #print dates
    for date in dates:
        if date[0] == None:
            continue

        # format date (must be a better way)
        fulldate = str(date[0])
        month = fulldate[5:7]
        day = fulldate[8:10]
        namedate = "%s %s" % (months[int(month)-1], day)

        # get run range
        minRun = 9e9
        maxRun = 0
        for row in records:
            if row[1] == None or row[1] == '0':
                continue

            if "recon" in options[1] and row[0] not in rcdb_run_numbers:
                continue

            rundate_obj = None
            try:
                rundate_obj = datetime.datetime.strptime(
                    row[1], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
            if rundate_obj == None:
                continue

            try:
                rundate = rundate_obj.strftime("%Y-%m-%d")
            except ValueError:
                pass

            if rundate == fulldate:
                if row[0] < minRun:
                    minRun = row[0]
                if row[0] > maxRun:
                    maxRun = row[0]

        if minRun != 9e9 and maxRun != 0:
            print "<li>"
            print "<b>%s</b> (Run %s-%s)" % (namedate, minRun, maxRun)
            print "<ul>"

            # print runs for given date
            for row in records:
                if row[1] == None or row[1] == '0':
                    continue
                if "recon" in options[1] and row[0] not in rcdb_run_numbers:
                    continue

                rundate_obj = None
                try:
                    rundate_obj = datetime.datetime.strptime(
                        row[1], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
                if rundate_obj == None:
                    continue
                #print rundate_obj

                try:
                    rundate = rundate_obj.strftime("%Y-%m-%d")
                except ValueError:
                    pass
                #print rundate

                numevents = row[2]

                if rundate == fulldate:
                    if options[2] not in rcdb_inelig:
                        if db.get_condition(row[0], "event_count"):
                            numevents = db.get_condition(
                                row[0], "event_count").value
                    print "<li>"
                    print ("<label><input type=\"radio\" id=\"run_number\" name=\"run_number\" value=\"%s\" onclick=\"changeRun(%s,%s);changePath();showPlot()\"> %s (%s eve)</label>" %
                           (row[0], row[0], row[0], row[0], numevents))
                    print ("<a href=\"/cgi-bin/data_monitoring/monitoring/browseJSRoot.py?run_number=%s&ver=%s&period=%s\" target=\"_blank\"><button type=\"button\"> ROOT </button></a>" %
                           (row[0], options[1], options[2]))
                    print (
                        "<a href=\"https://halldweb.jlab.org/rcdb/runs/info/%s\" target=\"_blank\"><button type=\"button\"> RCDB </button></a>" % (row[0]))
                    print "</li>"

            print "</ul>"
            print "</li>"

    print "</ul>"

    print "<script type=\"text/javascript\">make_tree_menu('runList');</script>"


# print row of table to display histograms
def print_row(options, charts):
    for chart in charts:
        print "<td class=\"plotrows\" style='text-align:center' bgcolor='#A9E2F3' onclick=\"freezeIt(); updatePlot(\'%s\');showPlot();\" onmouseover=\"updatePlot(\'%s\');showPlot(); this.style.backgroundColor='#F78181';\" onmouseout=\"this.style.backgroundColor='#A9E2F3';\">%s</td>" % (
            chart[0], chart[0], chart[1])


# return the option passed to the script
def get_options():
    form = cgi.FieldStorage()
    options = []

    if 'run_number' in form:
        options.append(int(form['run_number'].value))
    else:
        options.append(None)

    if 'ver' in form:
        options.append(str(form['ver'].value))
    else:
        options.append(None)

    if 'period' in form:
        options.append(str(form["period"].value))
    else:
        options.append(None)

    if options[0] == None and options[1] == None and options[2] == None:
        options[1] = 'mon_ver01'
        options[2] = 'RunPeriod-2019-11'
    return options


def get_path(options):
    runpth = "./"
    if options[0] != None:
        runpth = "/work/halld2/data_monitoring/"
        runpth += options[2]
        runpth += "/"
        runpth += options[1]
        runpth += "/Run"
        length = len(str(options[0]))
        for i in range(6-length):
            runpth += "0"
        runpth += str(options[0])
        runpth += "/"
    return runpth


def get_link_path(options):
    runpth = "./"
    if options[0] != None:
        runpth = "https://halldweb.jlab.org/cgi-bin/data_monitoring/monitoring/runBrowser.py?period="
        runpth += options[2]
        runpth += "&ver="
        runpth += options[1]
        runpth += "&run_number="
        length = len(str(options[0]))
        for i in range(6-length):
            runpth += "0"
        runpth += str(options[0])
    return runpth


# main function
# This is where the program starts
def main():
    # get options that may have been passed to this script
    options = get_options()

    # print the HTTP header
    printHTTPheader()

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("Offline Data Monitoring: Run Browser")

    print "</head>"

    # print the page body
    print "<body style=\"overflow-y: hidden\" >"

    print "<input type=\"hidden\" id=\"plotToShow\" value=\"none\">"
    # set period and version if only run_number is given
    if options[0] is not None:
        # set period first
        if options[2] is None:
            period = get_periods_run_number(options)
            options[2] = period[0][0]
        # set version
        if options[1] is None:
            versions = get_versions(options)
            revision = ("%s_ver%d" % (versions[0][1], versions[0][0]))
            options[1] = revision

    # print version selector
    print """<div id="nav" class="link-list">"""
    print_version_selector(options)

    # print run selector form
    records = get_data(options)
    # if records == None:
    #    records.append([10267, "", 10])
    print_run_selector(records, options, records)
    print "</form>"
    print "</div class=\"link-list\">"

    # print main page with plots if run number selected
    print """<div id="main">"""

    # get revision number
    revision_str = str(options[1])
    revision = int(re.search(r'\d+', revision_str).group())

    isRecon = "recon" in revision_str
# 3
    # define and initialize charts
    occupancy_charts = [["OCCUPANCY", "OCCUPANCY"]]
    occupancy_charts.pop(0)
    cdc_charts = [["CDC", "CDC"]]
    cdc_charts.pop(0)
    bcal_charts = [["BCAL", "BCAL"]]
    bcal_charts.pop(0)
    fcal_charts = [["FCAL", "FCAL"]]
    fcal_charts.pop(0)
    tof_charts = [["TOF", "TOF"]]
    tof_charts.pop(0)
    fdc_charts = [["FDC", "FDC"]]
    fdc_charts.pop(0)
    st_charts = [["ST", "ST"]]
    st_charts.pop(0)
    tagm_charts = [["TAGM", "TAGM"]]
    tagm_charts.pop(0)
    tagh_charts = [["TAGH", "TAGH"]]
    tagh_charts.pop(0)
    hldetectortiming_charts = [["HLTIMING", "HLTIMING"]]
    hldetectortiming_charts.pop(0)
    ps_charts = [["PS", "PS"]]
    ps_charts.pop(0)
    l1_charts = [["L1", "L1"]]
    l1_charts.pop(0)
    rf_charts = [["RF", "RF"]]
    rf_charts.pop(0)
    ana_charts1 = [["ANA1", "ANA1"]]
    ana_charts1.pop(0)
    ana_charts2 = [["ANA2", "ANA2"]]
    ana_charts2.pop(0)
    ana_charts3 = [["ANA3", "ANA3"]]
    ana_charts3.pop(0)
    tpol_charts = [["TPOL", "TPOL"]]
    tpol_charts.pop(0)
    elec_charts = [["ELECTRONICS", "ELECTRONICS"]]
    elec_charts.pop(0)
    uncat_charts = [["UNCAT", "UNCAT"]]
    uncat_charts.pop(0)

    # folder_path="./"
    folder_path = get_path(options)
    print "<b id='folderPath'>"
    print folder_path
    print "</b>"
    print "<br>"
    link_path = get_link_path(options)
    print "Link:"
    print "<b id='linkPath'>"
    print link_path
    print "</b>"
    print "<br>"
    print "<br>"
    # for each file in the folder find the corresponding textfile entry and sort into the subdetector table
    if os.path.isdir(folder_path):
        os.chdir(folder_path)
        for file in glob.glob("*.png"):
            if os.stat(folder_path+file).st_size < 3000:
                continue

            is_found = False
            #print file
            #print "<br>"
            filename = ""
            dispname = ""
            category = ""
            with open('/u/group/halld/www/halldweb/htbin/data_monitoring/monitoring/figure_titles', 'r') as f:
                for line in f:
                    words = line.split(',', 4)
                    filename = words[0]  # line.split(',', 3)[0]
                    dispname = words[1]  # line.split(',', 3)[1]
                    category = words[2]  # line.split(
                    version = words[3]

                    if filename == file:
                        is_found = True
                        break

            if is_found == False:
                print "<script>"
                print "console.log(\"%s\")" % (file)
                print "</script>"
                continue
            else:
                if category == "ANA":
                    ana_charts3.append([filename[:-4], dispname])
                elif category == "OCCUPANCY":
                    occupancy_charts.append([filename[:-4], dispname])
                elif category == "RECONSTRUCTION":
                    ana_charts1.append([filename[:-4], dispname])
                elif category == "CDC":
                    cdc_charts.append([filename[:-4], dispname])
                elif category == "BCAL":
                    bcal_charts.append([filename[:-4], dispname])
                elif category == "FCAL":
                    fcal_charts.append([filename[:-4], dispname])
                elif category == "TOF":
                    tof_charts.append([filename[:-4], dispname])
                elif category == "FDC":
                    fdc_charts.append([filename[:-4], dispname])
                elif category == "SC":
                    st_charts.append([filename[:-4], dispname])
                elif category == "TAGM":
                    tagm_charts.append([filename[:-4], dispname])
                elif category == "TAGH":
                    tagh_charts.append([filename[:-4], dispname])
                elif category == "L1":
                    l1_charts.append([filename[:-4], dispname])
                elif category == "HLDT":
                    hldetectortiming_charts.append([filename[:-4], dispname])
                elif category == "PS":
                    ps_charts.append([filename[:-4], dispname])
                elif category == "RF":
                    rf_charts.append([filename[:-4], dispname])
                elif category == "TPOL":
                    tpol_charts.append([filename[:-4], dispname])
                elif category == "ELECTRONICS":
                    elec_charts.append([filename[:-4], dispname])
                else:
                    uncat_charts.append([filename[:-4], dispname])

    else:
        print "This run number does not exist for the given run period/version number!!!!"
        print "<br>"
        print "<br>"
        print "<br>"
        print "<br>"

    occupancy_charts.sort()
    cdc_charts.sort()
    bcal_charts.sort()
    fcal_charts.sort()
    tof_charts.sort()
    fdc_charts.sort()
    st_charts.sort()
    tagm_charts.sort()
    tagh_charts.sort()
    hldetectortiming_charts.sort()
    ps_charts.sort()
    l1_charts.sort()
    rf_charts.sort()
    ana_charts1.sort()
    ana_charts2.sort()
    ana_charts3.sort()
    tpol_charts.sort()
    elec_charts.sort()
    uncat_charts.sort()


####################################################################################

    # display all possible charts in table for selection
    print """Click on a system header, then mouse over <font style="background-color: #A9E2F3">light blue</font> entries in table to view histograms, and <b>click</b>  on an entry to freeze/unfreeze a specific histogram. <br>"""
    print """<table style="width:200px; font-size:0.8em">"""

    if len(elec_charts) > 0:
        print "<th onclick=toggleRows(\"eleccharts\") >Electronics: "
        print "</th>"
        print "<tr id=\"eleccharts\" style=\"display:none;\">"
        print_row(options, elec_charts)
        print "</tr>"

    if len(occupancy_charts) > 0:
        print "<th onclick=toggleRows(\"occcharts\") >Occupancy: "
        print "</th>"
        print "<tr id=\"occcharts\" style=\"display:none;\">"
        print_row(options, occupancy_charts)
        print "</tr>"

    if len(rf_charts) > 0:
        print "<th onclick=toggleRows(\"rfcharts\") >RF: "
        print "</th>"
        print "<tr id=\"rfcharts\" style=\"display:none;\">"
        print_row(options, rf_charts)
        print "</tr>"

    if len(tpol_charts) > 0:
        print "<th onclick=toggleRows(\"tpolcharts\") >TPOL: "
        print "</th>"
        print "<tr id=\"tpolcharts\" style=\"display:none;\">"
        print_row(options, tpol_charts)
        print "</tr>"

    if len(tagm_charts) > 0:
        print "<th onclick=toggleRows(\"tagmcharts\") >TAGM: "
        print "</th>"
        print "<tr id=\"tagmcharts\" style=\"display:none;\">"
        print_row(options, tagm_charts)
        print "</tr>"

    if len(tagh_charts) > 0:
        print "<th onclick=toggleRows(\"taghcharts\") >TAGH: "
        print "</th>"
        print "<tr id=\"taghcharts\" style=\"display:none;\">"
        print_row(options, tagh_charts)
        print "</tr>"

    if len(ps_charts) > 0:
        print "<th onclick=toggleRows(\"pscharts\") >PS: "
        print "</th>"
        print "<tr id=\"pscharts\" style=\"display:none;\">"
        print_row(options, ps_charts)
        print "</tr>"

    if len(st_charts) > 0:
        print "<th onclick=toggleRows(\"stcharts\") >SC/ST: "
        print "</td>"
        print "<tr id=\"stcharts\" style=\"display:none;\">"
        print_row(options, st_charts)
        print "</tr>"

    if len(cdc_charts) > 0:
        print "<th onclick=toggleRows(\"cdccharts\") >CDC: "
        print "</th>"
        print "<tr id=\"cdccharts\" style=\"display:none;\">"
        print_row(options, cdc_charts)
        print "</tr>"

    if len(bcal_charts) > 0:
        print "<th onclick=toggleRows(\"bcalcharts\") >BCAL: "
        print "</th>"
        print "<tr id=\"bcalcharts\" style=\"display:none;\">"
        print_row(options, bcal_charts)
        print "</tr>"

    if len(fdc_charts) > 0:
        print "<th onclick=toggleRows(\"fdccharts\") >FDC: "
        print "</th>"
        print "<tr id=\"fdccharts\" style=\"display:none;\">"
        print_row(options, fdc_charts)
        print "</tr>"

    if len(fcal_charts) > 0:
        print "<th onclick=toggleRows(\"fcalcharts\") >FCAL: "
        print "</th>"
        print "<tr id=\"fcalcharts\" style=\"display:none;\">"
        print_row(options, fcal_charts)
        print "</tr>"

    if len(tof_charts) > 0:
        print "<th onclick=toggleRows(\"tofcharts\") >TOF: "
        print "</td>"
        print "<tr id=\"tofcharts\" style=\"display:none;\">"
        print_row(options, tof_charts)
        print "</tr>"

    if len(l1_charts) > 0:
        print "<th onclick=toggleRows(\"l1charts\") >L1: "
        print "</th>"
        print "<tr id=\"l1charts\" style=\"display:none;\">"
        print_row(options, l1_charts)
        print "</tr>"

    if len(hldetectortiming_charts) > 0:
        print "<th onclick=toggleRows(\"hldtcharts\") >HLDT: "
        print "</th>"
        print "<tr id=\"hldtcharts\" style=\"display:none;\">"
        print_row(options, hldetectortiming_charts)
        print "</tr>"

    if len(ana_charts1) > 0:
        print "<th onclick=toggleRows(\"ana1charts\") >Recon.: "
        print "</th>"
        print "<tr id=\"ana1charts\" style=\"display:none;\">"
        print_row(options, ana_charts1)
        print "</tr>"

    if len(ana_charts3) > 0:
        print "<th onclick=toggleRows(\"ana3charts\") >ANA: "
        print "</th>"
        print "<tr id=\"ana3charts\" style=\"display:none;\">"
        print_row(options, ana_charts3)
        print "</tr>"

    if len(uncat_charts) > 0:
        print "<th onclick=toggleRows(\"uncatcharts\") >Uncategorized: "
        print "</th>"
        print "<tr id=\"uncatcharts\" style=\"display:none;\">"
        print_row(options, uncat_charts)
        print "</tr>"

    print "</table>"
    print "<br>"
    print "<b id='RunLine'> <b>Run %s:</b> </b>" % (options[0])

    # display histogram
    print """<img src="" id="imageshow" style="display:none">"""
    print "</div>"

    print "</body>"
    print "</html>"

    conn.close()


if __name__ == "__main__":
    main()
