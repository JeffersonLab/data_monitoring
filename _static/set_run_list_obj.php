<?php

$servername = 'hallddb.jlab.org';
$username   = 'monbrowser';
$password   = '';
$dbname     = 'BrowserFamily';

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);
// Check connection
if (!$conn) {
    die('Connection failed: ' . mysqli_connect_error());
}
mysqli_select_db($conn, $dbname);

$sql = 'SELECT * FROM Runs WHERE Version_ID=' . $_GET["verID"] . ' AND ID IN (SELECT Run_ID FROM Plots WHERE PlotType_ID=' . $_GET["typeID"] . ')';
if (array_key_exists('minRunNum', $_GET) && array_key_exists('maxRunNum', $_GET)) {
  $sql .= ' AND (RunNumber BETWEEN ' . $_GET['minRunNum'] . ' AND ' . $_GET['maxRunNum'] . ')';
}
if (array_key_exists('query', $_GET)) {
  $sql .= " AND RunNumber IN (" . str_replace("_", ", ", $_GET['query']) . ")";
}
$sql .= ' ORDER BY RunNumber DESC LIMIT ' . $_GET["runNumLimit"];

file_put_contents("/u/group/halld/www/halldweb/html/data_monitoring/debug.txt", print_r($sql, true), FILE_APPEND);

$result = $conn->query($sql);
$data = array();
while ($row = $result->fetch_assoc()) {
    $data[] = array(
        'ID' => $row['ID'],
        'RunNumber' => $row['RunNumber'],
        'Version_ID' => $row['Version_ID']
    );
}

$conn->close();

echo json_encode($data);

?>
