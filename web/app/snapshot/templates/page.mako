<html><head>
<title>snapshot.debian.org</title>
<link rel="stylesheet" type="text/css" href="/static/snapshot.css"/>
</head>
<body>
<div class="pageheader">snapshot.debian.org</div>
% if not c.breadcrumbs is UNDEFINED:
	% for crumb in c.breadcrumbs:
		% if crumb['url'] is None:
			${crumb['name']}
		% else:
			<a href="${crumb['url']}">${crumb['name']}</a>
		% endif
		% if not 'sep' in crumb:
			/
		% else:
			${crumb['sep']}
		% endif

	% endfor
	<br />
% endif

% if not c.msg is UNDEFINED:
<p>${c.msg}</p>
% endif

${self.body()}
</body>
</html>
## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
