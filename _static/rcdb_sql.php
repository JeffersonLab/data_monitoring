<?php

$command_str = 'python ./browser_rcdb_interface.py ' . $_GET["query"] . " " . $_GET["RunP"];

if (array_key_exists('minRunNum', $_GET) && array_key_exists('maxRunNum', $_GET)) {
  $command_str = 'python ./browser_rcdb_interface.py ' . $_GET["query"] . " " . $_GET["RunP"] . " " . $_GET["minRunNum"] . " " . $_GET["maxRunNum"];
}

$command = escapeshellcmd($command_str);

echo shell_exec($command);

?>
