<html><head>
<title>snapshot.debian.org</title>
<link rel="stylesheet" type="text/css" href="/static/snapshot.css"/>
</head>
<body>
<div class="pageheader">snapshot.debian.org</div>

%for year in c.yearmonths:
<li>${year['year']}: 
% for month in year['months']:
<a href=".${year['year']}-${month}">${month}</a>
% endfor
</li>
%endfor

<!--
vim:syn=html
vim:set ts=4:
vim:set shiftwidth=4:
-->
</body>
</html>
