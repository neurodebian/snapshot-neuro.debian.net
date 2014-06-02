<h1>snapshot.debian.org</h1>
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
The Debian Project would like to thank the
<a href="http://www.sanger.ac.uk/">Wellcome Trust Sanger Institute</a> and
<a href="http://www.leaseweb.com>LeaseWeb Netherlands B.V.</a> for providing
hardware and hosting.

We would also like to thank the
<a href="http://www.ece.ubc.ca/">Electrical and Computer Engineering</a>
department at the University of British Columbia, Canada and
<a href="http://www.nordicbet.com/">Nordic Gaming</a> for providing
hardware/hosting and hardware, respectively, in the past.
</p>

<h2>Usage</h2>
<p>
In order to browse snapshots of the archives kept on snapshot.debian.org, simply
follow the links on the top left.  They will lead you to a list of months for
which data was imported, and the list entries in turn will point you to all
timestamps of a given month's snapshots.
</p>

<p>For example,
<a href="/archive/debian/"><code>/archive/debian/</code></a>
shows that we have imports for the main Debian archive,
<a href="http://ftp.debian.org/debian/"><code>http://ftp.debian.org/debian/</code></a>,
from 2005 until the present.
Picking October of 2009,
<a href="/archive/debian/?year=2009;month=10"><code>/archive/debian/?year=2009;month=10</code></a>,
provides us with a list of many different states of the debian archive, roughly spaced 6 hours apart
(the update frequency of ftp.debian.org at that time).
Following any of these links, say
<a href="/archive/debian/20091004T111800Z/"><code>/archive/debian/20091004T111800Z/</code></a>,
shows how <code>ftp.debian.org/debian</code> looked on the 4th of October 2009 at around 11:18 UTC.
</p>

<p style="margin-top:2em;">
If you want to add a specific date's archive to your apt <code>sources.list</code> simply
add an entry like these:
</p>
<pre>
deb     <a href="/archive/debian/20091004T111800Z/">http://snapshot.debian.org/archive/debian/20091004T111800Z/</a> lenny main
deb-src <a href="/archive/debian/20091004T111800Z/">http://snapshot.debian.org/archive/debian/20091004T111800Z/</a> lenny main
deb     <a href="/archive/debian-security/20091004T121501Z/">http://snapshot.debian.org/archive/debian-security/20091004T121501Z/</a> lenny/updates main
deb-src <a href="/archive/debian-security/20091004T121501Z/">http://snapshot.debian.org/archive/debian-security/20091004T121501Z/</a> lenny/updates main
</pre>
<p>
To learn which snapshots exist, i.e. which date strings are valid, simply
browse the list as mentioned above.  Valid date formats are
<code><i>yyyymmdd</i>T<i>hhmmss</i>Z</code> or simply <code><i>yyyymmdd</i></code>.  If there
is no import at the exact time you specified you will get the latest
available timestamp which is before the time you specified.
</p>
<p>
It may be necessary to ignore the Valid-Until header within Release files, in order
to prevent apt from disregarding snapshot entries ("Release file expired").  Use
<code>aptitude -o Acquire::Check-Valid-Until=false update</code> or
<code>apt-get -o Acquire::Check-Valid-Until=false update</code> for this purpose.
</p>

<p style="margin-top:2em;">
If you want anything related to a specific package simply enter the
<em>source package name</em> in the form, or find it in the package index.
</p>
