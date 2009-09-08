<html><head>
<title>snapshot.debian.org</title>
<link rel="stylesheet" type="text/css" href="/static/snapshot.css"/>
</head>
<body>
<div class="pageheader">snapshot.debian.org</div>

<h1>Archives</h1>

Browse ftp archive snapshots from one of the following archives:
<ul>
	% for row in c.rows:
	<li>${row}</li>
	%endfor
</ul>

<h1>Packages</h1>

<!--
vim:syn=html
vim:set ts=4:
vim:set shiftwidth=4:
-->
</html>
