<?php

$command = './browser_rcdb_interface.py ' . urlencode($_GET["query"]) . " " . $_GET["RunP"];

if (array_key_exists('minRunNum', $_GET) && array_key_exists('maxRunNum', $_GET)) {
    $command .= " " . $_GET["minRunNum"] . " " . $_GET["maxRunNum"];
}

echo shell_exec(escapeshellcmd($command));

?>
