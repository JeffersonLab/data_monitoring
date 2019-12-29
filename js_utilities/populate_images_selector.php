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
$sql = 'SELECT * FROM PlotTypes WHERE ID IN (SELECT PlotType_ID FROM Plots WHERE Run_ID IN (SELECT ID FROM Runs WHERE Version_ID=' . $_GET["ID"] . '))';
$result = $conn->query($sql);
$data = array();
while ($row = $result->fetch_assoc()) {
    $data[] = array(
        'ID' => $row['ID'],
        'FileName' => $row['FileName'],
        'DisplayName' => $row['DisplayName'],
        'PlotCategory_ID' => $row['PlotCategory_ID']
    );
}

$conn->close();

echo json_encode($data);

?>
