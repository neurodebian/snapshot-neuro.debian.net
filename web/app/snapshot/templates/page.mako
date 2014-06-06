<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		% if not hasattr(c, 'title'):
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
		% if hasattr(c, 'breadcrumbs') and len(c.breadcrumbs) > 0:
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

% if hasattr(c, 'msg') and c.msg != "":
<p>${c.msg}</p>
% endif

${self.body()}

		<div id="bottom">
			Application Developed by Peter Palfrader &mdash; Web/Graphics designed by Bernhard Weitzhofer
			<br/>
			Source code available for download via <a href="git://git.debian.org/mirror/snapshot.debian.org.git">git</a> and browseable online via <a href="http://git.debian.org/?p=mirror/snapshot.debian.org.git">gitweb</a>.
			<br/>
			Please <a href="http://www.debian.org/Bugs/Reporting">report bugs</a> against the <a href="http://bugs.debian.org/snapshot.debian.org">snapshot.debian.org package</a>.
			<br/>
			<%
				import datetime
				now = datetime.datetime.now()
			%>
			Built at ${now} on ${app_globals.thishost}.
			<br/>
			<a href="http://validator.w3.org/check?uri=referer">validate</a>
			<br/>
			<br/>
			<br/>
            <a href="http://www.leaseweb.com" title="LeaseWeb offers hosted infrastructure solutions, including Cloud, CDN, Dedicated Servers, Managed Hosting, Colocation, and Hybrid Solutions" target="_blank"><img src="/static/images/leaseweb.gif" alt="LeaseWeb" width="140" height="25"/></a>
		</div>
	</body>
</html>
## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
