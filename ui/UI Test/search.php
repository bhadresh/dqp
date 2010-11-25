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
		<form action="search.php" method="post" >
			
			<table cellspacing="0" cellpadding="0" align="left" >
				<tr>
					<td>
						<div align="left">
							<input name="keyword" type="text"  style="width:600px; height:32px;">
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
		
<?php
set_time_limit("600");
$keyword=trim($_POST["keyword"]);
if($keyword=="")
{
	echo"Please enter your keyword";
	exit; 
}
function listFiles($dir,$keyword,&$array)
{
	$handle=opendir($dir);
	while(false!==($file=readdir($handle)))
	{
		if($file!="."&&$file!="..")
		{
			if(is_dir("$dir/$file"))
			{
				listFiles("$dir/$file",$keyword,$array);
			}
			else
			{
				$data=fread(fopen("$dir/$file","r"),filesize("$dir/$file"));
				if(eregi("<body([^>]+)>(.+)</body>",$data,$b))
				{
					$body=strip_tags($b["2"]);
				}
				else
				{
					$body=strip_tags($data);
				} if($file!="search.php")
				{
					if(eregi("$keyword",$body))
					{
						if(eregi("<title>(.+)</title>",$data,$m))
						{
							$title=$m["1"];
						}
						else
						{
							$title="no title";
						}
						$array[]="$file $title";
					}
				}
			}
		}
	}
}
?>
<div>

<table id="tableStyle">
<?php

$array=array();
listFiles("pages","$keyword",$array);

if( $array )
{
	$i = 0;
	foreach($array as $value)
	{
		if( $i < 100 )
		{
			list($filedir,$title)=split("[ ]",$value,"2");
			echo "<tr><td id=\"linksDisplayed\"><a href=" . $filedir .">  $title <br /><br /></td> </tr>";
		}
		$i += 1;
	} 
}
else
{
	echo "<tr><td id=\"linksDisplayed\">Sorry no pages were found for : <b> $keyword </b> <br /><br /></td> </tr>";
}


?>
</table>
</div>
</body>
</html>

