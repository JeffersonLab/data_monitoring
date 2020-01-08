  Array.prototype.max = function() {
    return Math.max.apply(null, this);
  };

  Array.prototype.min = function() {
    return Math.min.apply(null, this);
  };

  // https://halldweb.jlab.org/data_monitoring/Plot_Browser.html?minRunNum=40000&maxRunNum=51000&RunPeriod=RunPeriod-2018-01&Version=rawdata_ver00&Plot=CDC_occupancy&rcdb_query=@is_2018production
  var query_result = [];
  var SelectedRunListOBJ = [];
  var toDisplay = [];
  var first_showing = true;
  var run_num_limit = 100;

  var par_from_url = { minRunNum: "", maxRunNum: "", RunPeriod: "", Version: "", Plot: "", rcdb_query: "" };
  var use_url_par = false;
  var run_range_set_by_user = false;

  $(document).ready(function() {
    SetOptionsFromURL();
    PopulateColumnsSelector();
    document.getElementById('maxNumOfPlots').value = run_num_limit;
    PopulateRunPeriodSelector();
  });

function SetOptionsFromURL() {
  currentURL_split = document.URL.split("?");
  if (currentURL_split.length == 2) {
    use_url_par = true;
    URL_AND_split = currentURL_split[1].split("&");
    for (var i = 0; i < URL_AND_split.length; i++) {
      var opt = URL_AND_split[i].split("=");
      par_from_url[opt[0]] = opt[1];
    }
    if (par_from_url['minRunNum'] != "" && par_from_url['maxRunNum'] != "") {
      run_range_set_by_user = true;
    }
    document.getElementById("minRunNum").value = par_from_url['minRunNum'];
    document.getElementById("maxRunNum").value = par_from_url['maxRunNum'];
    if (par_from_url['rcdb_query'] != "") {
      document.getElementById('rcdb_query').value = par_from_url['rcdb_query'].replace(/%3E/g, ">").replace(/%20/g, " ");
    }
  }
}

function ClearOptionsFromURL() {
  par_from_url['minRunNum']  = "";
  par_from_url['maxRunNum']  = "";
  par_from_url['RunPeriod']  = "";
  par_from_url['Version']    = "";
  par_from_url['Plot']       = "";
  par_from_url['rcdb_query'] = "";
  use_url_par                = false;
}

function ShowWaitIcon() {
  document.getElementById("wait_icon").style.visibility = "visible";
}

function HideWaitIcon() {
  document.getElementById("wait_icon").style.visibility = "hidden";
}

function SetMaxNumPlots() {
  var tmp_num = document.getElementById('maxNumOfPlots').value;
  if (tmp_num >= 1) {
    run_num_limit = tmp_num;
  } else {
    run_num_limit = 1;
    document.getElementById('maxNumOfPlots').value = run_num_limit;
  }
}

function PopulateColumnsSelector() {
  var default_num = 3;
  if ((navigator.userAgent.indexOf('iPhone') > 0 && navigator.userAgent.indexOf('iPad') == -1) || navigator.userAgent.indexOf('iPod') > 0 || navigator.userAgent.indexOf('Android') > 0) {
    default_num = 1;
    run_num_limit = 15;
  }
  for (var i = 1; i <= 10; i++) {
    var newoption   = document.createElement("option");
    newoption.text  = i;
    newoption.value = i;
    if (i == default_num) newoption.selected = true;
    document.getElementById("Columns").add(newoption);
  }
}

function DoQuery() {
  query_result = [];
  if (document.getElementById('rcdb_query').value == "") return;
  ShowWaitIcon();
  if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp = new XMLHttpRequest();
  } else {
    // code for IE6, IE5
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }

  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      query_result = this.responseText.split("_");
      HideWaitIcon();
    }
  }
  xmlhttp.open("GET", "./js_utilities/rcdb_sql.php?query=" + document.getElementById("rcdb_query").value + "&RunP=" + document.getElementById("RunPeriod").options[document.getElementById("RunPeriod").selectedIndex].value, false);
  xmlhttp.send();
}

function sortSelect(selElem) {
  var tmpAry = new Array();
  for (var i = 0; i < selElem.options.length; i++) {
    tmpAry[i] = new Array();
    tmpAry[i][0] = selElem.options[i].text;
    tmpAry[i][1] = selElem.options[i].value;
    tmpAry[i][2] = selElem.options[i].id;
    tmpAry[i][3] = selElem.options[i].dbid;
    tmpAry[i][4] = selElem.options[i].selected;
  }
  tmpAry.sort();
  while (selElem.options.length > 0) {
    selElem.options[0] = null;
  }
  for (var i = 0; i < tmpAry.length; i++) {
    var op = new Option(tmpAry[i][0], tmpAry[i][1]);
    op.id       = tmpAry[i][2];
    op.dbid     = tmpAry[i][3];
    op.selected = tmpAry[i][4];
    selElem.options[i] = op;
  }
}

function ShowPlots() {
  var tableRef = document.getElementById('imgTable').getElementsByTagName('tbody')[0];
  var RunPSelector = document.getElementById("RunPeriod");
  var SelectedRunP = RunPSelector.options[RunPSelector.selectedIndex].value;

  var VerSelector = document.getElementById("Version");
  var SelectedVer = VerSelector.options[VerSelector.selectedIndex].value;

  var IMGSelector = document.getElementById("Plot");
  var SelectedIMG = IMGSelector.options[IMGSelector.selectedIndex].value;

  var columnstoDisplay = document.getElementById("Columns").value;

  if (first_showing) {
    first_showing = false;
    HideWaitIcon();
  }

  QueryXref();

  $("#imgTableBody").empty();

  var numAdded = 0;

  for (var i = 0; i < toDisplay.length; i++) {
    var runNum_asINT = parseInt(toDisplay[i].split("Run")[1]);
    if (runNum_asINT < document.getElementById("minRunNum").value || runNum_asINT > document.getElementById("maxRunNum").value) {
      continue;
    }

    var DOM_img = document.createElement("IMG");

    var DOM_txt = document.createElement("b");
    DOM_txt.setAttribute('style', 'text-align:center;')
    DOM_txt.innerHTML = "<center><font size='5'>" + "Run  " + toDisplay[i].split("Run")[1] + "</font></center>";

    // Insert a row in the table at the last row
    if (numAdded % columnstoDisplay == 0) {
      var newRowhead = tableRef.insertRow(tableRef.rows.length);
      var newRow = tableRef.insertRow(tableRef.rows.length);
    }
    var newCellh = newRowhead.insertCell(numAdded % columnstoDisplay);
    var newCell  = newRow.insertCell(numAdded % columnstoDisplay);

    var JSRootLinkt = '<center><font size="5"><b><a href=\"/cgi-bin/data_monitoring/monitoring/runBrowser.py?run_number=' + runNum_asINT + '&ver=' + SelectedVer + '&period=' + SelectedRunP + '\" target=\"_blank\">' + "Run  " + toDisplay[i].split("Run")[1] + '</a></b>  <a href=\"https://halldweb.jlab.org/rcdb/runs/info/' + runNum_asINT + '\"' + 'target=\"_blank\">' + 'info' + '</a></font></center>'

    DOM_txt.innerHTML = JSRootLinkt;
    var imgpth = "/work/halld2/data_monitoring/" + SelectedRunP + "/" + SelectedVer + "/" + toDisplay[i] + "/" + SelectedIMG;
    DOM_img.setAttribute("src", "https://halldweb.jlab.org" + imgpth);
    var currentwidth = 1196;
    var currentheight = 772;

    var width_to_use = $(document).width() * .95 / columnstoDisplay;
    var scale_factor = width_to_use / currentwidth;
    DOM_img.setAttribute("width", currentwidth * scale_factor);
    DOM_img.setAttribute("height", currentheight * scale_factor);
    var fullpth = "https://halldweb.jlab.org" + imgpth;

    DOM_img.onclick = function click() { window.open(this.getAttribute("src"), '_blank'); }

    // Append a text node to the cell
    newCellh.appendChild(DOM_txt);
    newCell.appendChild(DOM_img);
    numAdded++;
  }

  if (use_url_par) ClearOptionsFromURL();
}

function SetRunListOBJ() {
  if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp = new XMLHttpRequest();
  } else {
    // code for IE6, IE5
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var result = JSON.parse(this.responseText);
      SelectedRunListOBJ = [];
      int_run_list = [];
      for (var i = 0; i < result.length; i++) {
        SelectedRunListOBJ.push('Run' + ('000000' + result[i]['RunNumber']).slice(-6));
        int_run_list.push(parseInt(result[i]['RunNumber']));
      }
      if (!run_range_set_by_user) {
        document.getElementById("minRunNum").value = int_run_list.min();
        document.getElementById("maxRunNum").value = int_run_list.max();
      }
    }
  }
  var php_string = "js_utilities/set_run_list_obj.php?verID=" + document.getElementById("Version").options[document.getElementById("Version").selectedIndex].dbid + "&typeID=" + document.getElementById("Plot").options[document.getElementById("Plot").selectedIndex].dbid + "&runNumLimit=" + run_num_limit;
  if (run_range_set_by_user) {
    php_string += "&minRunNum=" + document.getElementById("minRunNum").value;
    php_string += "&maxRunNum=" + document.getElementById("maxRunNum").value;
  }
  xmlhttp.open("GET", php_string, false);
  xmlhttp.send();
}

function PopulateRunPeriodSelector() {
  if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp = new XMLHttpRequest();
  } else {
    // code for IE6, IE5
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var result = JSON.parse(this.responseText);
      for (var i = 0; i < result.length; i++) {
        var newoption   = document.createElement("option");
        newoption.text  = result[i]['Name'];
        newoption.value = result[i]['Name'];
        newoption.id    = result[i]['Name'];
        newoption.dbid  = result[i]['ID'];
        if (newoption.id == par_from_url['RunPeriod']) {
          newoption.selected = true;
        }
        if (i == result.length - 1 && par_from_url['RunPeriod'] == "") {
          newoption.selected = true;
        }
        document.getElementById("RunPeriod").add(newoption);
      }
      PopulateVersionSelector();
    }
  }
  xmlhttp.open("GET", "js_utilities/populate_runperiod_selector.php", true);
  xmlhttp.send();
}

function PopulateVersionSelector() {
  removeOptions(document.getElementById("Version"));

  if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp = new XMLHttpRequest();
  } else {
    // code for IE6, IE5
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var result = JSON.parse(this.responseText);
      for (var i = 0; i < result.length; i++) {
        var newoption   = document.createElement("option");
        var text = "";
        if (result[i]['Type'] == "rawdata") {
          text += "Rootspy ";
        } else if (result[i]['Type'] == "recon") {
          text += "Reconstruction Launch ";
        } else if (result[i]['Type'] == "mon" && result[i]['VersionNumber'] != 1) {
          text += "Monitoring Launch ";
        } else if (result[i]['Type'] == "mon" && result[i]['VersionNumber'] == 1) {
          text += "Incoming Data ";
        } else if (result[i]['Type'] == "mc") {
          text += "Monte Carlo ";
        } else {
          continue;
        }
        text += 'ver' + ('00' + result[i]['VersionNumber']).slice(-2);
        newoption.text  = text;
        newoption.value = result[i]['Type'] + '_ver' + ('00' + result[i]['VersionNumber']).slice(-2);
        newoption.id    = newoption.value;
        newoption.dbid  = result[i]['ID'];
        if (newoption.id == par_from_url['Version']) {
          newoption.selected = true;
        }
        if (i == 0 && par_from_url['Version'] == "") {
          newoption.selected = true;
        }
        document.getElementById("Version").add(newoption);
      }
      PopulateImagesSelector();
    }
  }
  xmlhttp.open("GET", "js_utilities/populate_version_selector.php?ID=" + document.getElementById("RunPeriod").options[document.getElementById("RunPeriod").selectedIndex].dbid, true);
  xmlhttp.send();
}

function PopulateImagesSelector() {
  removeOptions(document.getElementById("Plot"));

  if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp = new XMLHttpRequest();
  } else {
    // code for IE6, IE5
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var result = JSON.parse(this.responseText);
      for (var i = 0; i < result.length; i++) {
        var newoption   = document.createElement("option");
        newoption.text  = result[i]['DisplayName'];
        newoption.value = result[i]['FileName'];
        newoption.id    = newoption.value.slice(0, -4);
        newoption.dbid  = result[i]['ID'];
        if (newoption.id == par_from_url['Plot']) {
          newoption.selected = true;
        }
        document.getElementById("Plot").add(newoption);
      }
      sortSelect(document.getElementById("Plot"));
      if (par_from_url['Plot'] == "") {
        document.getElementById("Plot").selectedIndex = 0;
      }
      if (par_from_url['rcdb_query'] != "") DoQuery();  // Sets query_result.
      SetRunListOBJ();
      ShowPlots();
    }
  }
  xmlhttp.open("GET", "js_utilities/populate_images_selector.php?ID=" + document.getElementById("Version").options[document.getElementById("Version").selectedIndex].dbid, true);
  xmlhttp.send();
}

function removeOptions(selectbox) {
  for (var i = selectbox.options.length - 1; i >= 0; i--) {
    selectbox.remove(i);
  }
}

function QueryXref() {
  var to_return = SelectedRunListOBJ;
  var to_return2 = to_return;

  if (query_result.length != 0) {
    to_return2 = to_return.filter(function(id) {
      var tofind = id.split("Run")[1];
      while (tofind.charAt(0) === '0') {
        tofind = tofind.substr(1);
      }
      return query_result.indexOf(tofind) > -1;
    });
  }
  toDisplay = to_return2;  // .reverse();
}
