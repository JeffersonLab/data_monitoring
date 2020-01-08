<?php
//echo 'python ./browser_rcdb_interface.py ' . $_GET["query"];
//echo "<br>";
$command = escapeshellcmd('python ./browser_rcdb_interface.py ' . $_GET["query"] . " " . $_GET["RunP"]);
//echo $command;
$output = shell_exec($command);
//echo $output;
echo $output;
return $output
?>
