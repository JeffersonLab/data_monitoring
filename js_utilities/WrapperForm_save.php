<?php

$dateNOW = date("m-d-Y");
$timeNOW = date("h:i:sa");
$datetimeNOW = date("Ymdhisa");

$rungen = 0;
$savegen = 0;

$rungeant = 0;
$savegeant = 0;

$runsmear = 0;
$savesmear = 0;

$runrecon = 0;
$saverecon = 0;

if ( $_GET["RunGeneration"] != "")
{
    $rungen = 1;
}
if ( $_GET["SaveGeneration"] != "")
{
    $savegen = 1;
}

if ( $_GET["RunGeant"] != "")
{
    $rungeant = 1;
}
if ( $_GET["SaveGeant"] != "")
{
    $savegeant = 1;
}

if ( $_GET["RunSmear"] != "")
{
    $runsmear = 1;
}
if ( $_GET["SaveSmear"] != "")
{
    $savesmear = 1;
}

if ( $_GET["RunRecon"] != "")
{
    $runrecon = 1;
}
if ( $_GET["SaveRecon"] != "")
{
    $saverecon = 1;
}

$msg = $_GET["username"] . ", I received your request for Monte Carlo on " . $dateNOW . " at " . $timeNOW . "\n";

$addrange="";
$runlow = $_GET["runnumber"];
$runhigh = $runlow;
if ( $_GET["maxRunNum"] != "" )
{
    $addrange=" to " . $_GET["maxRunNum"];
    $runhigh = $_GET["maxRunNum"];
}

$msg = $msg . "You have requested " . $_GET["numevents"] . " events to be produced from run number " . $_GET["runnumber"] . $addrange . "\n";
$msg = $msg . "The configuration file, reproduced below, will be checked by our team of skilled technicians to ensure you will receive only the finest artisinal Monte Carlo samples.\n";
$msg = $msg . "You will be contacted at " . $_GET["useremail"] . " in the event issues are encountered.\n";
$msg = $msg . "===============================================================================\n";

$msg = $msg . "\n\n\n\n";

$fullOutput = "/volatile/halld/home/tbritton/REQUESTED_MC/" . $_GET["outputloc"] . "_" . $datetimeNOW . "/";
$configstub = "";
$configstub = $configstub . "DATA_OUTPUT_BASE_DIR=" . $fullOutput . "\n";

$configstub = $configstub . "NCORES=1\n";

$configstub = $configstub . "GENERATOR=" . $_GET["generator"] . "\n";
$configstub = $configstub . "GENERATOR_CONFIG=" . $_GET["generator_config"] . "\n";
$configstub = $configstub . "GEANT_VERSION=" . $_GET["Geantver"] . "\n";

$bkg = $_GET["bkg"];

if ( $_GET["randomtag"] != "" )
{
    $bkg = $bkg . ":" . $_GET["randomtag"];
}

$configstub = $configstub . "BKG=" . $bkg . "\n";

$msg = $msg . $configstub;
$msg = $msg . "===============================================================================\n";
$msg = $msg . $_GET["addreq"];

$servername = "hallddb.jlab.org";
$username = "mcuser";
$password = "";
$dbname = "gluex_mc";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "INSERT INTO Project (Submitter, Email, Is_Dispatched, RunNumLow, RunNumHigh, NumEvents, GeantVersion, OutputLocation, Submit_Time, RunGeneration, SaveGeneration, RunGeant, SaveGeant, RunSmear, SaveSmear, RunReconstruction, SaveReconstruction, Generator, Generator_Config, Config_Stub, BKG, Comments)" . " VALUES (\"" . $_GET["username"] . "\", \"" . $_GET["useremail"] . "\", \"" . "NO" . "\", " . $runlow . ", " . $runhigh . ", " . $_GET["numevents"] . ", " . $_GET["Geantver"] . ", \"" . $fullOutput . "\", " . "NOW()" . ", " . $rungen . ", " . $savegen . ", " . $rungeant . ", " . $savegeant . ", " . $runsmear . ", " . $savesmear . ", " . $runrecon . ", " . $saverecon . ", \"" . $_GET["generator"] . "\", \"" . $_GET["generator_config"] . "\", \"" . $configstub . "\", \"" . $bkg . "\", \"" . $_GET["addreq"] . "\")";
//echo $sql;
//echo "<br>";
if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();

//echo $msg;
mail("tbritton@jlab.org," . $_GET["useremail"],"MC Request",$msg);
echo "<br>";
echo "Thanks for your submition, your request should have been received.  A copy of your request has been emailed to the given address for your records.";

?>
