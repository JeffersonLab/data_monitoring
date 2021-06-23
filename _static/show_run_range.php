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
$sql = 'SELECT MIN(RunNumber), MAX(RunNumber) FROM Runs WHERE Version_ID=' . $_GET["ID"];
$result = $conn->query($sql);
$data = array();
while ($row = $result->fetch_assoc()) {
    $data[] = array(
        'MIN' => $row['MIN(RunNumber)'],
        'MAX' => $row['MAX(RunNumber)']
    );
}

$conn->close();

echo json_encode($data);

?>
