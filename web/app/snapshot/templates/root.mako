<%inherit file="/page.mako" />


<table class="rootmaintable">
<tr>
<td>
<h1>Archives</h1>

<p>Browse ftp archive snapshots from one of the following archives:</p>

<ul>
	% for name in c.names:
	<li><a href="archive/${name['quoted']}/">${name['raw']}</a></li>
	%endfor
</ul>

<h1>Packages</h1>

Search in the index:<br />
<ul class="inlineList">
%for letter in c.srcstarts:
	<li><a href="package/?cat=${letter['quoted']}">${letter['raw']}</a></li>
%endfor
</ul>

<form action="package/">
<p>Or enter a source package name directly: <input name="src" /> <input type="submit" value="Submit" /></p>
</form>

</td>

<td>
<div class="rootmaintext">
<h1>snapshot.debian.org</h1>
<p>
The snapshot archive is a wayback machine that allows access to old
packages based on dates and version numbers.  It consists of all
past and current packages the Debian archive provides.
</p>

<p>
The ability to install packages and view sourcecode from any given date
in the past is very helpful for developers who try to fix regressions.
Users frequently need an older version of the software in order to make
a particular application run.
</p>

<p>
The Debian Project wants to thank <a href="http://www.sanger.ac.uk/">Wellcome
Trust Sanger Institute</a>, <a href="http://www.ece.ubc.ca/">UBC Electrical and
Computer Engineering</a> and <a href="http://www.nordicbet.com/">Nordic
Gaming</a> for providing hardware and hosting for this service.
</p>

<h1>News</h1>
<h2>2010-02-20</h2>
<p>
Finished set up of mirroring scripts.  While snapshot-master (stabile) still is
the entity importing new snapshots into the system all the data is now replicated
to a secondary site (sibelius).  The web front-end runs on both of them.
</p>

</div>
</td>
</tr>
</table>
