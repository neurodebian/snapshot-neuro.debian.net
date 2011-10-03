<%inherit file="/page.mako" />

<%
   g.snapshotdebian = "snapshot.debian.org"
%>

<div class="documentwrapper">
<div class="bodywrapper">
<div class="body">
<h1>snapshot-neuro.debian.net</h1>
<p>
The snapshot archive is a wayback machine that allows access to old
packages based on dates and version numbers.  It consists of all
past and current packages the Debian archive provides.
</p>

<p>
The ability to install packages and view source code from any given date can be
very helpful to developers and users. It provides a valuable resource for
tracking down when regressions were introduced, or for providing a specific
environment that a particular application may require to run. The snapshot
archive is accessible like any normal apt repository, allowing it to be easily
used by all.
</p>

<p>
The NeuroDebian Project wants to thank Peter Palfrader for developing
snapshotting engine, Bernhard Weitzhofer for the original webdesign
for the web front-end,
and <a href="http://www.dartmouth.edu/~psych/">Department of
Psychological and Brain Sciences, Dartmouth College</a> for providing
hardware and network bandwidth.
</p>

<h2>Usage</h2>
<p>
<a href="/">${g.domain}</a> contains solely snapshots of
the <a href="http://neuro.debian.net">NeuroDebian</a> repository,
which you could browser by following the link on the top left.  It
will lead you to a list of months for which data was imported, and the
list entries in turn will point you to all timestamps of a given
month's snapshots.  Snapshots of the main Debian archive (including
backports, volatile, etc.) are available from the
official <a href="http://${g.snapshotdebian}">${g.snapshotdebian}</a>
and should be used in conjunction with <a href="/">${g.domain}</a>.
</p>

<p>For example,
<a href="/archive/neurodebian/"><code>/archive/neurodebian/</code></a>
shows that we have imports for the NeuroDebian archive,
<a href="http://neuro.debian.net/debian/"><code>http://neuro.debian.net/debian/</code></a>,
from October 2010 until the present.
Picking October of 2010,
<a href="/archive/neurodebian/?year=2010;month=10"><code>/archive/neurodebian/?year=2010;month=10</code></a>,
provides us with a list of many different states of the NeuroDebian archive, spaced 12 hours apart
(the snapshotting frequency of neuro.debian.net at that time).
Following any of these links, say
<a href="/archive/neurodebian/20101014T200503Z/"><code>/archive/neurodebian/20101014T200503Z/</code></a>,
shows
how <a href="http://neuro.debian.net/debian"><code>neuro.debian.net/debian</code></a>
looked on the 14th of October 2010 at around 20:05 UTC.
</p>

<p style="margin-top:2em;">
If you want to add a specific date's archive to your
apt <code>sources.list</code> simply add an entry like these to cover
snapshots of NeuroDebian and main debian archives.
</p>
<pre>
# NeuroDebian
deb     <a href="/archive/neurodebian/20101014T200503Z/">http://${g.domain}/archive/neurodebian/20101014T200503Z/</a> lenny main
deb-src <a href="/archive/neurodebian/20101014T200503Z/">http://${g.domain}/archive/neurodebian/20101014T200503Z/</a> lenny main
# Main Debian repository
deb     <a href="http://${g.snapshotdebian}/archive/debian/20101014T200503Z/">http://${g.snapshotdebian}/archive/debian/20101014T200503Z/</a> lenny main
deb-src <a href="http://${g.snapshotdebian}/archive/debian/20101014T200503Z/">http://${g.snapshotdebian}/archive/debian/20101014T200503Z/</a> lenny main
# Security updates
deb     <a href="http://${g.snapshotdebian}/archive/debian-security/20091004T121501Z/">http://${g.snapshotdebian}/archive/debian-security/20091004T121501Z/</a> lenny/updates main
deb-src <a href="http://${g.snapshotdebian}/archive/debian-security/20091004T121501Z/">http://${g.snapshotdebian}/archive/debian-security/20091004T121501Z/</a> lenny/updates main
</pre>
<p>
To learn which snapshots exist, i.e. which date strings are valid, simply
browse the list as mentioned above.  Valid date formats are
<code><i>yyyymmdd</i>T<i>hhmmss</i>Z</code> or simply <code><i>yyyymmdd</i></code>.  If there
is no import at the exact time you specified you will get the latest
available timestamp which is before the time you specified.
</p>

<p style="margin-top:2em;">
If you want anything related to a specific package simply enter the
<em>source package name</em> in the form, or find it in the package index.
</p>

<h1>News</h1>
<h2>2011-10-03</h2>
<p>
Re-instantiated snapshotting service which was inactive since <a href="/archive/neurodebian/20110805T200503Z/">2011-08-05</a>.
</p>

<h2>2010-10-18</h2>
<p>
Initial, not-yet-official, availability of <a href="/">${g.domain}</a>.
</p>

</div>
</div>
</div>

<div class="sphinxsidebar">
<div class="sphinxsidebarwrapper">

           <p class="logo"><a href="">
              <img class="logo" src="http://neuro.debian.net/_static/fmri_w200.png" alt="Logo"/> 
            </a></p> 

<h3>Archives</h3>

<p>Browse ftp archive snapshots from one of the following archives:</p>

<ul>
	% for name in c.names:
	<li><a href="archive/${name['quoted']}/">${name['raw']}</a></li>
	%endfor
</ul>

<h3>Packages</h3>

<h4>source packages:</h4>

Search in the index of source packages:<br />
<ul class="inlineList">
%for letter in c.srcstarts:
	<li><a href="package/?cat=${letter['quoted']}">${letter['raw']}</a></li>
%endfor
</ul>

<form action="package/">
<p>Or enter a <strong>source</strong> package name directly: <input name="src" /> <input type="submit" value="Submit" /></p>
</form>

<h4>binary packages:</h4>

<ul class="inlineList">
%for letter in c.binstarts:
	<li><a href="binary/?cat=${letter['quoted']}">${letter['raw']}</a></li>
%endfor
</ul>

<form action="binary/">
<p>Search for a <strong>binary</strong> package name: <input name="bin" /> <input type="submit" value="Submit" /></p>
</form>

<h3>Miscellaneous</h3>
<ul>
	<!-- <li><a href="oldnews">older news</a></li> -->
	<li><a href="http://snapshot.debian.org/">snapshot.debian.org</a>
	<li><a href="http://git.debian.org/?p=mirror/snapshot.debian.org.git;a=blob_plain;f=API">machine-usable interface</a></li>
	<!-- <li><a href="http://${config['app_conf']['snapshot.masterdomain']}/removal">removal logs</a></li> -->
</ul>

</div>
</div>



