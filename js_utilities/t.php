<?php

$data = array();

$RunPeriods = scandir("/work/halld2/data_monitoring/");
file_put_contents("/u/group/halld/www/halldweb/html/data_monitoring/debug.txt", "test\n");

array_shift($RunPeriods);
array_shift($RunPeriods);
array_pop($RunPeriods);
foreach ($RunPeriods as &$runp) {
  $runpData = array();
  // echo $runp . "<br>";
  // echo "-----------<br>";
  $versions = scandir("/work/halld2/data_monitoring/" . $runp . "/");
  array_shift($versions);
  array_shift($versions);

  foreach ($versions as &$ver) {
    // echo $ver . "<br>";
    $runs = scandir("/work/halld2/data_monitoring/" . $runp . "/" . $ver . "/");
    array_shift($runs);
    array_shift($runs);
    // array_pop($runs);
    // array_pop($runs);
    // $jsonify_ver = array()
    $runList = array();
    foreach ($runs as &$run) {
      if (substr($run, 0, 3) == "Run") {
        $runList[] = $run;
      } else {
        continue;
      }
      // echo "       " . $run . "<br>";
    }
    $RunNumVer = array('Version'=>$ver, 'Runs'=>$runList);
    $runpData[] = $RunNumVer;
    // $runpData[] = json_encode($RunNumVer);
  }
  // echo "===================<br>";
  $path_parse = array('RunPeriod'=>$runp, 'Versions'=>$runpData);
  // echo json_encode($path_parse);
  // echo '<br>';
  // $data[] = json_encode($path_parse);
  $data[] = $path_parse;
}

echo json_encode($data,JSON_PRETTY_PRINT);
/* foreach ($data as $datum) {
  echo json_encode($datum);
  echo '<br>';
} */

return json_encode($data);
// clean dirs

?>
