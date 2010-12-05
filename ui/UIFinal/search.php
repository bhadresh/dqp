<html>
<head>
		<title>Web Search</title>
		<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
		<style>
		#linksDisplayed 
		{
			font-family:'Lucida Casual', 'Verdana';
		}

		#tableStyle
		{
			padding-left:145px;
		}
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
							<input id="q" name="q" type="text"  style="width:600px; height:32px;">
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
        $json_result = shell_exec("python " . dirname(dirname(__file__)) . "/dp/distributor.py " . escapeshellarg($_GET['q']));
        $et = microtime(true);
        if (!empty($json_result)) {
            echo "<p>Retrieved in: " . ($et - $st) . " seconds </p>";
            $result = json_decode(str_replace("'", '"', $json_result), true);
            var_export($result);
			echo "<table id=\"tableStyle\">";
			foreach ($result['records'] as $r)
			{
				echo "<tr><td id=\"linksDisplayed\">";
				echo '"<a href=  "' .$r['url'] . '" > '. $r['docid'] .'</a> <br/>"';
				echo '"Page Rank: ' . $r['pagerank'] . '<br/>"';
				echo '"Score: ' . $r['score'] . '"';
				echo "<br /><br /></td> </tr>";
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

