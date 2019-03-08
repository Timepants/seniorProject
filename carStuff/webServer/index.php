<?php
$dir    = '/home/pi/Curiopo/src/';
$modelDir   = $dir.'carModels/';
$files1 = scandir($modelDir);

// print_r($files1);

$command = 'python3 '.$dir.'controllerTest.py';
// $command = 'python3 '.$dir.'unused/phpTest.py';

// $command = 'ls';

echo $command;

echo '<pre>';
// Outputs all the result of shellcommand "ls", and returns
// the last output line into $last_line. Stores the return value
// of the shell command in $retval.
$last_line = system($command, $retval);
// Printing additional info
echo '
</pre>
<hr />Last line of the output: ' . $last_line . '
<hr />Return value: ' . $retval;
?>