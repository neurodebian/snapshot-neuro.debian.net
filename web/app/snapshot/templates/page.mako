<?xml version="1.0" encoding="iso-8859-1" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		% if c.title == "":
			<title>snapshot.debian.org</title>
		% else:
			<title>${c.title} - snapshot.debian.org</title>
		% endif
		<link rel="stylesheet" type="text/css" href="/static/style.css"/>
	</head>
	<body>
		<div id="top">
			<a id="logo" href="http://snapshot.debian.org/"><img src="/static/images/top.png" alt="snapshot.debian.org"/></a>
		</div>
		% if not c.breadcrumbs is UNDEFINED:
			<div id="pageheader">
			<ul id="breadcrumbs" style="font-size:small;">
				% for crumb in c.breadcrumbs:
					<li>
					% if crumb['url'] is None:
						${crumb['name']}
					% else:
						<a href="${crumb['url']}">${crumb['name']}</a>
					% endif
					% if not 'sep' in crumb:
						/
					% elif crumb['sep'] != "":
						${crumb['sep']}
					% endif
					</li>
				% endfor
			</ul>
			</div>
		% endif

% if not c.msg is UNDEFINED and c.msg != "":
<p>${c.msg}</p>
% endif

${self.body()}

		<div id="bottom">
			Made by Peter Palfrader &mdash;
			Web/Graphics design Bernhard Weitzhofer &mdash;
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
