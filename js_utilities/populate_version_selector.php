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
$sql = 'SELECT * FROM Versions WHERE RunPeriod_ID=' . $_GET["ID"] . ' ORDER BY VersionNumber';
$result = $conn->query($sql);
$data = array();
while ($row = $result->fetch_assoc()) {
    $data[] = array(
        'ID' => $row['ID'],
        'Type' => $row['Type'],
        'VersionNumber' => $row['VersionNumber'],
        'RunPeriod_ID' => $row['RunPeriod_ID']
    );
}
file_put_contents('../debug2.txt', json_encode($data));

$conn->close();

echo json_encode($data);

?>
