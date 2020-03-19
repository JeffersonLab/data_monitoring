<?php
$data = array();
$rootpath='/work/halld2/calibration/';
echo $rootpath;
echo "<br>";
echo $_GET["option"];
echo "<br>";
$things = scandir($rootpath);
echo "<br>";
$files = array_diff(scandir($rootpath), array('.','..'));
echo "<br>";
echo $files;
if($_GET["option"]=="RunPeriod")
{

    $di = new RecursiveDirectoryIterator($rootpath);

    echo $di;
}

echo json_encode($data);

return json_encode($data);



    function endswith($string, $test) {
        $strlen = strlen($string);
        $testlen = strlen($test);
        if ($testlen > $strlen) return false;
        return substr_compare($string, $test, $strlen - $testlen, $testlen) === 0;
    }


?>
