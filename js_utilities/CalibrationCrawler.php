<?php
$data = array();

$rootpath='/work/halld2/calibration/';
//echo $rootpath;
//echo "<br>";
//echo $_GET["option"];
//echo "<br>";
//echo "<br>";
//echo $files;
if($_GET["RunP"] )
{
$rootpath=$rootpath . $_GET["RunP"] . "/";
}

if($_GET["Ver"])
{
$rootpath=$rootpath . $_GET["Ver"] . "/";
}

if($_GET["Pass"])
{
$dirs = array_filter(glob($rootpath . '/*'), 'is_dir');
$rootpath=$dirs[sizeof($dirs)-1] . "/" . $_GET["Pass"];
}

#echo $rootpath;
#echo "<br>";

if( $_GET["option"] != "images" && $_GET["option"] != "SubDir" && $_GET["option"] != "Runs" )
{
//echo $rootpath;

$dirs = array_filter(glob($rootpath . '/*'), 'is_dir');

foreach($dirs as $dir)
{
    $parts=explode("/",$dir);
    //print_r($parts);
    $data[]=$parts[sizeof($parts)-1];
}
}
else if ( $_GET["option"] == "SubDir")
{
    
    $dirs = array_filter(glob($rootpath . '/*'), 'is_dir');

    $dirs = array_filter(glob($dirs[sizeof($dirs)-1] . '/*'), 'is_dir');

    foreach($dirs as $dir)
    {
    $parts=explode("/",$dir);
    //print_r($parts);
    $data[]=$parts[sizeof($parts)-1];
    }

}
else if ( $_GET["option"] == "images")
{
    
    foreach (glob($rootpath . "/*.png") as $img)
    {

    $parts=explode("/",$img);
    //print_r($parts);
    $data[]=$parts[sizeof($parts)-1];
    }
}
else if ( $_GET["option"] == "Runs")
{
    //echo $rootpath;
    //echo "<br>";
    $dirs = array_filter(glob($rootpath . '/*'), 'is_dir');

    foreach($dirs as $dir)
    {
    $parts=explode("/",$dir);
    //print_r($parts);
    $data[]=$parts[sizeof($parts)-1];
    }

}

echo json_encode($data);

return json_encode($data);



    function endswith($string, $test) {
        $strlen = strlen($string);
        $testlen = strlen($test);
        if ($testlen > $strlen) return false;
        return substr_compare($string, $test, $strlen - $testlen, $testlen) === 0;
    }





//$di = new RecursiveDirectoryIterator('/work/halld2/calibration/RunPeriod-2018-01/');
//foreach (new RecursiveIteratorIterator($di) as $filename => $file) {
//    if( endswith($filename, 'png'))
//    {
//        /*/work/halld2/calibration/RunPeriod-2017-01/ver17/Run030843/verify/verify_PIDSystemTiming.png*/
//        //echo $filename;
//        $path = explode("/",$filename);
//       if ($path[4] != "RunPeriod-2018-01")
//        {
//            continue;
//        }
//        if ($path[5] != "ver17" && $path[5] != "ver20" && $path[5] != "ver18" && $path[5] != "ver19")
//        {
//            continue;
//        }
//        
//        //echo $path[4] . "<br>";
//        $path_parse=array('RunPeriod'=>$path[4],'Version'=>$path[5],'RunNumber'=>$path[6], 'SubDir'=>$path[7], 'FileName'=>$path[8]);
//        //echo json_encode($path_parse);
//        //echo '<br>';
//        $data[]=json_encode($path_parse);
//    }
//}
//
//    /*foreach ($data as $datum)
//    {
//       //echo json_encode($datum);
//       echo '<br>'; 
//    }*/
//
//    $path = "/group/halld/www/halldweb/data/webdata/CalibBrowser.json";
//
//    //echo "Path : $path";
//    //echo "<br>";
//    //echo "<br>";
//    require "$path";
//    $fp = fopen('/group/halld/www/halldweb/data/webdata/CalibBrowser.json', 'w') or die("can't open file");
//    //echo "Write";
//    //echo json_encode($data);
//    fwrite($fp, json_encode($data));
//    fclose($fp);
//    //echo "Closed";
//    echo json_encode($data);
//    //echo "done";
//    return json_encode($data);
//
//    function endswith($string, $test) {
//        $strlen = strlen($string);
//        $testlen = strlen($test);
//        if ($testlen > $strlen) return false;
//        return substr_compare($string, $test, $strlen - $testlen, $testlen) === 0;
//    }
//
//
?>
