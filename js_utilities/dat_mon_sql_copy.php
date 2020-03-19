<?php
echo "hi";
$servername = "hallddb";
$username = "datmon";
$password = "";
$dbname = "data_monitoring";

//echo $_GET['qs'] . " ---> " . $_GET['qe'];

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);
// Check connection
if (!$conn) {
   die("Connection failed: " . mysqli_connect_error());
}
?>
