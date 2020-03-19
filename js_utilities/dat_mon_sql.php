<?php
if (isset($_GET['qs'])) {
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

  //echo $_GET['qs'] . " ---> " . $_GET['qe'];
   // echo "<br>";
    $startDate = date("Y-m-d", strtotime($_GET['qs']));//date('Y-d-m', strtotime(str_replace('-', '/', $_GET['qs'])));
    $endDate = date("Y-m-d", strtotime($_GET['qe']));//date('Y-d-m', strtotime(str_replace('-', '/', $_GET['qe'])));

    //echo $startDate . " ---> " . $endDate;
    //echo "<br>";
    $sql = "SELECT " . $_GET['c'] . " FROM " . $_GET['t'] . " WHERE STR_TO_DATE(date_generated, '%Y-%m-%d') >= STR_TO_DATE('" . $startDate . "','%Y-%m-%d')" . " AND " . "STR_TO_DATE(date_generated, '%Y-%m-%d')  <= STR_TO_DATE('" . $endDate . "','%Y-%m-%d')";
    //echo "<br>";
    //echo $sql;
    //echo "<br>";
    $result = $conn->query($sql);
    $data = array();
    if ($result->num_rows > 0) {
    // output data of each row
        while($row = $result->fetch_assoc()) {
            $data[]=$row;
         //echo "id: " . $row["id"]. " - Run: " . $row["run"]. "<br>";
        }
    } 
    $conn->close();
    echo json_encode($data);
    return json_encode($data);

} else {

    $data=array();
    return json_encode($data);
    // Fallback behaviour goes here
}
?>
