<html>
<head>
</head>
<body>
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
						$array[]="$dir/$file $title";
					}
				}
			}
		}
	}
}
$array=array();
listFiles(".","$keyword",$array);
foreach($array as $value)
{
	list($filedir,$title)=split("[ ]",$value,"2");
	echo "$title "."
\n";
} 
?>

</body>
</html>

