<%inherit file="/page.mako" />

<h1>Archives</h1>

Browse ftp archive snapshots from one of the following archives:
<ul>
	% for name in c.names:
	<li><a href="archive/${name}/">${name}</a></li>
	%endfor
</ul>

<h1>Packages</h1>

<form action="package/">
Enter source package name: <input name="src" /> <input type="submit" value="Submit" />
</form>
