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
$row = $result->fetch_assoc();
file_put_contents('../debug.txt', $row['Name']);

$conn->close();

$data = shell_exec('python browser_family_to_json.py');
echo $data;
return $data;

?>
