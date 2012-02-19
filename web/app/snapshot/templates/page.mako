<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		% if c.title == "":
			<title>${app_globals.domain}</title>
		% else:
			<title>${c.title} - ${app_globals.domain}</title>
		% endif
		<link rel="stylesheet" type="text/css" href="/static/style.css" />
		<link rel="icon" type="image/vnd.microsoft.icon" href="/static/favicon.ico" />
	</head>
	<body>
		<div id="top">
			<a id="logo" href="http://${app_globals.domain}"><img src="/static/images/top.png" alt="${app_globals.domain}" width="644" height="71"/></a>
		</div>
		% if not c.breadcrumbs is UNDEFINED and (len(c.breadcrumbs) != 0):
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
			Made by Peter Palfrader
			&mdash;
			Web/Graphics design Bernhard Weitzhofer
			&mdash;
			<code>git://git.debian.org/mirror/snapshot.debian.org.git</code>
			(<a href="http://git.debian.org/?p=mirror/snapshot.debian.org.git">gitweb on alioth</a>)
			&mdash;
			<a href="http://www.debian.org/Bugs/Reporting">Report bugs</a> and issues against the
			  <a href="http://bugs.debian.org/snapshot.debian.org">snapshot.debian.org package</a> on bugs.debian.org.
			<br />
			<%
				import datetime
				now = datetime.datetime.now()
			%>
			Built at ${now} on ${app_globals.thishost}
			<br />
			<a href="http://validator.w3.org/check?uri=referer">validate</a>
		</div>
	</body>
</html>
## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
