<?php

$command = escapeshellcmd('python ./browser_rcdb_interface.py ' . $_GET["query"] . " " . $_GET["RunP"]);

$output = shell_exec($command);

echo $output;

?>
