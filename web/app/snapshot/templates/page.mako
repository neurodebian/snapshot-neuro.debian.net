<html><head>
<title>snapshot.debian.org</title>
<link rel="stylesheet" type="text/css" href="/static/snapshot.css"/>
</head>
<body>
<div class="pageheader">snapshot.debian.org</div>
% if not c.breadcrumbs is UNDEFINED:
%  for crumb in c.breadcrumbs:
${crumb} /
%  endfor
<br />
% endif
${self.body()}
</body>
</html>
## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
