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
# $sql = 'SELECT * FROM PlotTypes WHERE ID IN (SELECT PlotType_ID FROM Plots WHERE Run_ID IN (SELECT ID FROM Runs WHERE Version_ID=' . $_GET["ID"] . '))';
$bit4 = '(bitmask >> 3 = 0 AND "rawdata" IN (SELECT Type FROM Versions WHERE ID=' . $_GET["ID"] . '))';
$bit2 = '(bitmask >> 1 & 1 = 0 AND "mon" IN (SELECT Type FROM Versions WHERE ID=' . $_GET["ID"] . '))';
$bit1_mc = '(bitmask & 1 = 0 AND "mc" IN (SELECT Type FROM Versions WHERE ID=' . $_GET["ID"] . '))';
$bit1_re = '(bitmask & 1 = 0 AND "recon" IN (SELECT Type FROM Versions WHERE ID=' . $_GET["ID"] . '))';
$bit1_an = '(bitmask & 1 = 0 AND "analysis" IN (SELECT Type FROM Versions WHERE ID=' . $_GET["ID"] . '))';
$sql = 'SELECT * FROM PlotTypes WHERE ID IN (SELECT PlotType_ID FROM Plots WHERE Run_ID IN (SELECT ID FROM Runs WHERE Version_ID=' . $_GET["ID"] . ')) AND NOT (' . $bit4 . ' OR ' . $bit2 . ' OR ' . $bit1_mc . ' OR ' . $bit1_re . ' OR ' . $bit1_an . ')';
$result = $conn->query($sql);
$data = array();
while ($row = $result->fetch_assoc()) {
    $data[] = array(
        'ID'              => $row['ID'],
        'FileName'        => $row['FileName'],
        'DisplayName'     => $row['DisplayName'],
        'PlotCategory_ID' => $row['PlotCategory_ID']
    );
}

$conn->close();

echo json_encode($data);

?>
