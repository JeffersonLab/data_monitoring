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

// Initial query to determine the min and max run numbers (only if not provided)
if (!array_key_exists('minRunNum', $_GET) && !array_key_exists('maxRunNum', $_GET)) {
    $rangeSql = 'SELECT MIN(RunNumber) as minRun, MAX(RunNumber) as maxRun FROM Runs WHERE Version_ID=' . $_GET["verID"] . ' AND ID IN (SELECT Run_ID FROM Plots WHERE PlotType_ID=' . $_GET["typeID"] . ')';
    $rangeResult = mysqli_query($conn, $rangeSql);
    $rangeRow = mysqli_fetch_assoc($rangeResult);

    $_GET['minRunNum'] = $rangeRow['minRun'];
    $_GET['maxRunNum'] = $rangeRow['maxRun'];
}

// Now apply the main query with the determined range or user-specified range
$sql = 'SELECT * FROM Runs WHERE Version_ID=' . $_GET["verID"] . ' AND ID IN (SELECT Run_ID FROM Plots WHERE PlotType_ID=' . $_GET["typeID"] . ')';
$sql .= ' AND (RunNumber BETWEEN ' . $_GET['minRunNum'] . ' AND ' . $_GET['maxRunNum'] . ')';

// Apply additional query filtering if needed
if (array_key_exists('query', $_GET)) {
    $sql .= " AND RunNumber IN (" . str_replace("_", ", ", $_GET['query']) . ")";
}

// Determine the order direction (ASC or DESC) based on user input or default
$orderDirection = isset($_GET['order']) && $_GET['order'] === 'ASC' ? 'ASC' : 'DESC';

// Apply the sorting and limit
$sql .= ' ORDER BY RunNumber ' . $orderDirection . ' LIMIT ' . $_GET["runNumLimit"];


$result = $conn->query($sql);
$data = array();
while ($row = $result->fetch_assoc()) {
    $data[] = array(
        'ID'         => $row['ID'],
        'RunNumber'  => $row['RunNumber'],
        'Version_ID' => $row['Version_ID']
    );
}

$conn->close();

echo json_encode($data);

?>
