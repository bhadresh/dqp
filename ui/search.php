<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
		<title>Web Search</title>
		<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
		<style type="text/css">
            #linksDisplayed {font-family:'Lucida Casual', 'Verdana';}
            #tableStyle {padding-left:145px;}
		</style>
</head>
<body bgcolor="#FFFFFF" text="#000000">
		<br />
		<div align="middle">
			<a href="search.htm"> <img src="backsmall.jpg" align="left" border="none"/> </a>
		</div>
		<p>
		<form action="search.php" method="get" >
			
			<table cellspacing="0" cellpadding="0" align="left" >
				<tr>
					<td>
						<div align="left">
							<input id="q" name="q" type="text" value="<?=(isset($_GET['q']) ? $_GET['q'] : '')?>" style="width:600px; height:32px;">
						</div>
					</td>
					<td>
						<div align="right">
							<input type="image" src="searchsmall.png" style="height: 32px; width: 66px" name="Submit" value="Search" width="35px">
						</div>
					</td>
				</tr>
			</table>
		</form>
		</p>
		<br />
		<br />
		<br />
		<br />
<div>

<?php
    if (isset($_GET['q']) && !empty($_GET['q'])) {
        $st = microtime(true);
        $json_result = shell_exec("python " . dirname(dirname(__file__)) . "/dp/distributor.py -p " . (isset($_GET['p']) ? $_GET['p'] : 1) . " -m " . (isset($_GET['m']) ? $_GET['m'] : 'QL') . " " . escapeshellarg($_GET['q']));
        $et = microtime(true);
        if (!empty($json_result)) {
            echo "<p>Retrieved in: " . ($et - $st) . " seconds </p>";
            $result = json_decode(str_replace("'", '"', $json_result), true);
			echo "<table id=\"tableStyle\">";
			foreach ($result['records'] as $rec) {
				$data = file_get_contents(dirname(__FILE__) . "/../data/pages/" . $rec['docid'] . ".html");
				echo $data;
                                if(eregi("<title>(.+)</title>",$data,$m))
				{
					$title=$m["1"];
				}
				else
				{
					$title="no title";
				}
				echo '<tr><td id="linksDisplayed">';
				echo '<a href="' . $rec['url'] . '">' . $title . '</a><br/>';
				echo 'Page Rank: ' . $rec['pagerank'] . '<br/>';
				echo 'Score: ' . $rec['score'] . '<br/>';
				echo '</td></tr>';
			}
			echo "</table>";
        }
        else {
            echo "Sorry no pages were found for: " . $_GET['q'];
        }
    }
?>



</div>
</body>
</html>

