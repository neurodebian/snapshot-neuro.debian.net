<html><head>
<title>snapshot.debian.org</title>
<link rel="stylesheet" type="text/css" href="/static/snapshot.css"/>
</head>
<body>
<div class="pageheader">snapshot.debian.org</div>

%for run in c.runs:
<a href="${run['run']}/">${run['run_hr']}</a><br />
%endfor

<!--
vim:syn=html
vim:set ts=4:
vim:set shiftwidth=4:
-->
</body>
</html>
