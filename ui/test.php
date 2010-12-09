<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
    <title>Search Test</title>
</head>
<body>
    <form action="<?=$_SERVER['PHP_SELF']?>" method="get">
        <input type="text" id="q" name="q" size="60" maxsize="255" value="<?=(isset($_GET['q']) ? $_GET['q'] : '')?>" />&nbsp;<input type="submit" value="Search" />
    </form>
<?php
    if (isset($_GET['q']) && !empty($_GET['q'])) {
        $st = microtime(true);
        $json_result = shell_exec("python " . dirname(dirname(__file__)) . "/dp/distributor.py -p " . (isset($_GET['p']) ? $_GET['p'] : 1) . " -m " . (isset($_GET['m']) ? $_GET['m'] : 'QL') . " -q " . escapeshellarg($_GET['q']));
        $et = microtime(true);
        if (!empty($json_result)) {
            echo "<p>Retrieved in: " . ($et - $st) . " seconds";
            $result = json_decode(str_replace("'", '"', $json_result), true);
            echo "<p>Search Result (Raw JSON):<br /><pre>";
            echo $json_result;
            echo "</pre>";
            
            echo "</p><p>Search Result (PHP Array):<br /><pre>";
            var_export($result);
            echo "</pre></p>";            
        }
        else {
            echo "Sorry no pages were found for: " . $_GET['q'];
        }
    }
?>    
</body>
</html>
