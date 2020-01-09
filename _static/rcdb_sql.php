<?php

echo shell_exec('./' . $_GET['script'] . '.py "' . http_build_query($_GET) . '"');

?>
