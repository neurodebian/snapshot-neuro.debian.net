<%inherit file="/page.mako" />

<h1>Archives</h1>

Browse ftp archive snapshots from one of the following archives:
<ul>
	% for name in c.names:
	<li><a href="archive/${name}/">${name}</a></li>
	%endfor
</ul>

<h1>Packages</h1>

Search in the index:</br>
<div class="box">
%for letter in c.srcstarts:
	<a href="package/?cat=${letter}">${letter}</a>
	% if letter != c.srcstarts[-1]:
		-
	% endif
%endfor
</div>

<form action="package/">
Or enter a source package name directly: <input name="src" /> <input type="submit" value="Submit" />
</form>

