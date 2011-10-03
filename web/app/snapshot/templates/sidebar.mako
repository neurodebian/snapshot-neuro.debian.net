<h1>Archives</h1>

<p>Browse ftp archive snapshots from one of the following archives:</p>

<ul>
	% for name in c.names:
	<li><a href="archive/${name['quoted']}/">${name['raw']}</a></li>
	%endfor
</ul>

<h1>Packages</h1>

<h2>source packages:</h2>

Search in the index of source packages:<br />
<ul class="inlineList">
%for letter in c.srcstarts:
	<li><a href="package/?cat=${letter['quoted']}">${letter['raw']}</a></li>
%endfor
</ul>

<form action="package/">
<p>Or enter a <strong>source</strong> package name directly: <input name="src" /> <input type="submit" value="Submit" /></p>
</form>

<h2>binary packages:</h2>

<ul class="inlineList">
%for letter in c.binstarts:
	<li><a href="binary/?cat=${letter['quoted']}">${letter['raw']}</a></li>
%endfor
</ul>

<form action="binary/">
<p>Search for a <strong>binary</strong> package name: <input name="bin" /> <input type="submit" value="Submit" /></p>
</form>

<h1>Miscellaneous</h1>
<ul>
	<li><a href="oldnews">older news</a></li>
	<li><a href="http://lists.debian.org/debian-snapshot/">mailinglist</a></li>
	<li><a href="http://git.debian.org/?p=mirror/snapshot.debian.org.git;a=blob_plain;f=API">machine-usable interface</a></li>
	<li><a href="removal/">removal logs</a></li>
</ul>
