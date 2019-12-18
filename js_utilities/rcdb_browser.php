<?php

$data_json = file_get_contents('../test2.json');

// $data = json_decode($data_json, true);

// echo json_encode($data, JSON_PRETTY_PRINT);
echo $data_json;

// return json_encode($data);
return $data_json;

?>
