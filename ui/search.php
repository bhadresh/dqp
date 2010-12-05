<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
		<title>Web Search</title>
		<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
		<style type="text/css">

            #linksDisplayed {font-family:'Lucida Casual', 'Verdana';}
            #tableStyle {padding-left:145px;}
			#navlist li
			{
				display: inline;
				list-style-type: none;
				padding-right: 20px;
			}

            body {font-family:Verdana;}            
            .time {padding-left: 140px; font-size:11px;}
            #results {margin-left:10px; margin-top:10px;}

		</style>
</head>
<body>
	<form action="search.php" method="get">		
		<table cellspacing="0" cellpadding="0">
			<tr>
                <td>
                	<a href="search.htm"><img src="backsmall.jpg" alt="" border="0" /></a>
                </td>
				<td>
					<div align="left">
						<input id="q" name="q" type="text" value="<?=(isset($_GET['q']) ? $_GET['q'] : '')?>" style="width:600px; height:26px;">
					</div>
				</td>
				<td>
					<div align="right">
						<input type="submit" value="Search" style="height:34px;" />
					</div>
				</td>
			</tr>
		</table>
	</form>
<?php
    if (isset($_GET['q']) && !empty($_GET['q'])) {
        $st = microtime(true);
        $json_result = shell_exec("python " . dirname(dirname(__file__)) . "/dp/distributor.py -p " . (isset($_GET['p']) ? $_GET['p'] : 1) . " -m " . (isset($_GET['m']) ? $_GET['m'] : 'QL') . " " . escapeshellarg($_GET['q']));
        $et = microtime(true);
        if (!empty($json_result)) {
            $result = json_decode(str_replace("'", '"', $json_result), true);
            echo '<div class="time">About ' . number_format($result['count']) . ' results (' . number_format($et - $st, 4) . ' seconds)</div>';
			echo '<table id="results" cellpadding="2" cellspacing="2">';
			foreach ($result['records'] as $rec) {
				$data = file_get_contents(dirname(__FILE__) . "/../data/pages/" . $rec['docid'] . ".html");
                if(eregi("<title>(.+)</title>", $data, $m)) {
					$title = strip_tags(preg_replace("#\s+#", " ", $m[1]));
				}
				else {
					$title = $rec['url'];
				}
				echo '<tr><td>';
				echo '<a href="' . $rec['url'] . '">' . $title . '</a><br/>';
				echo 'Page Rank: ' . $rec['pagerank'] . '<br/>';
				echo 'Score: ' . $rec['score'] . '<br/>';
				echo $rec['url'] . ' - <a href="../data/pages/' . $rec['docid'] . '.html">Cached</a>';
				echo '</td></tr>';
			}
			echo "</table>";
        }
        else {
            echo "Sorry no pages were found for: " . $_GET['q'];
        }
		$pagecount = $result['count'] / 10;
		if( $pagecount < 1 )
		{
			echo '<div id="navcontainer"><ul id="navlist">';
			for ($index = 1; $index <= $pagecount; $index++) 
			{ 
				echo '<li' . ($index == $_GET['p'] ? ' id="active"' : '') . '><a href="' . $_SERVER['PHP_SELF'] . '?q=' . urlencode($_GET['q']) . (isset($_GET['m'] ? '&m=' . $_GET['m'] : '') . '&p=' . $index . '">' . $index . '</a></li>';
			}

			echo '</ul></div>';
		}
    }
?>

</div>


</body>
</html>

