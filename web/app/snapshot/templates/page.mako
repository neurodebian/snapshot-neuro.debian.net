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

<P> &nbsp; <P> &nbsp; <P>
<div style="font-size: xx-small; text-align: center">
<hr style="width: 75%; height: 1px; border-width: 0; color: gray; background-color: gray">
Made by Peter Palfrader &mdash;
Graphics design and layout too (Can't you tell?) &mdash;
git: <a href="http://asteria.noreply.org/~weasel/snapshot.git">http://asteria.noreply.org/~weasel/snapshot.git</a> &mdash;
Report bugs and issues to weasel (XXX: eventually bugs.d.o)<br />
<%
	import datetime
	now = datetime.datetime.now()
%>
Built at ${now}
</div>
</body>
</html>
## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
