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
$sql = 'SELECT * FROM RunPeriods';
$result = $conn->query($sql);
$data = array();
while ($row = $result->fetch_assoc()) {
    $myarray[] = array(
        'ID' => $row['ID'],
        'Name' => $row['Name'],
        'Location_ID' => $row['Location_ID']
    );
}

$conn->close();

return json_encode($data));

?>
