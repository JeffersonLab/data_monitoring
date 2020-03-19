<?php
    //echo "hi";
    $servername = "hallddb.jlab.org";
    $username = "rcdb";
    $password = "";
    $dbname = "rcdb";

    // Create connection
    $conn = mysqli_connect($servername, $username, $password, $dbname);
    // Check connection
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    
   // echo "hi";
   //echo $_GET['qs'] . " ---> " . $_GET['qe'];
   // echo "<br>";
    //$startDate = date("Y-m-d", strtotime($_GET['qs']));//date('Y-d-m', strtotime(str_replace('-', '/', $_GET['qs'])));
    //$endDate = date("Y-m-d", strtotime($_GET['qe']));//date('Y-d-m', strtotime(str_replace('-', '/', $_GET['qe'])));

    //echo $startDate . " ---> " . $endDate;
    //echo "<br>";
    //$sql = "SELECT " . $_GET['c'] . " FROM " . $_GET['t'] . " WHERE STR_TO_DATE(date_generated, '%Y-%m-%d') >= STR_TO_DATE('" . $startDate . "','%Y-%m-%d')" . " AND " . "STR_TO_DATE(date_generated, '%Y-%m-%d')  <= STR_TO_DATE('" . $endDate . "','%Y-%m-%d')";
    $sql = "SELECT " . "time_value, run_number" . " FROM " . "rcdb.conditions" . " WHERE " . "condition_type_id=57";
    //echo "<br>";
    echo $sql;
    //echo "<br>";
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }
    mysqli_select_db($conn, $dbname);
    $result = $conn->query($sql);
    echo "<br>";
    echo "result is:";
    echo "<br>";
    echo $result;
    $data = array();
    if($result)
    {
        echo "it returned something";
    }
    else
    {
        echo "it returned nothing";
    }
    echo $result->num_rows;

    if ($result->num_rows > 0) {
    // output data of each row
        
   
        while($row = $result->fetch_assoc()) {
            //$data[]=$row;
            echo "time: " . $row["time_value"]. " - Run: " . $row["run_number"] . "<br>";
            
        }
    } 
    else
    {
        echo "NO RESULT";
    }
    $conn->close();
    //return json_encode($data);

//} else {

//    $data=array();
//    return json_encode($data);
    // Fallback behaviour goes here
//}
?>
