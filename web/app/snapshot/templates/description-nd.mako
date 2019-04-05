<h1>snapshot-neuro.debian.net</h1>
<p>
The snapshot archive is a wayback machine that allows access to old
packages based on dates and version numbers.  It consists of all
past and current packages the NeuroDebian archive provides.  You will
likely need also snapshots of the packages from the official <a
href="http://snapshot.debian.org">Debian archive snapshots</a>.
</p>

<p>
The ability to install packages and view source code from any given date can be
very helpful to developers and users. It provides a valuable resource for
tracking down when regressions were introduced, or for providing a specific
environment that a particular application or data analysis was ran in
some time before. The snapshot
archive is accessible like any normal apt repository, allowing it to be easily
used by any Debian-based system supported by NeuroDebian (ATM Debian
and Ubuntu releases).
</p>

<p>
The NeuroDebian Project wants to thank Peter Palfrader for developing
the snapshotting engine, Bernhard Weitzhofer for the original webdesign
for the web front-end,
and <a href="http://pbs.dartmouth.edu/">Department of
Psychological and Brain Sciences, Dartmouth College</a> for originally providing
hardware and network bandwidth.
</p>

<p>
Currently NeuroDebian repository snapshotting service is supported as a part of
the <a href="http://repronim.org">ReproNim</a> project to facilitate (re)creation
of computational environments for data analysis in neuroimaging.
</p>

<h2>Usage</h2>
<p>
This archive contains solely snapshots of
the <a href="http://neuro.debian.net">NeuroDebian</a> repository,
which you could browse by following the link on the top left.  It
will lead you to a list of months for which packages was imported, and the
list entries in turn will point you to all timestamps of a given
month's snapshots.  Snapshots of the main Debian archive (including
backports, volatile, etc.) are available from the
official <a href="http://snapshot.debian.org">snapshot.debian.org</a>
and should be used in conjunction with this snapshots archive.
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
apt <code>sources.list</code>, add an entry like this to cover
snapshots of NeuroDebian and main debian archives:
</p>
<pre>
# NeuroDebian
deb     <a href="/archive/neurodebian/20101014T200503Z/">http://snapshot-neuro.debian.net:5002/archive/neurodebian/20101014T200503Z/</a> lenny main
deb-src <a href="/archive/neurodebian/20101014T200503Z/">http://snapshot-neuro.debian.net:5002/archive/neurodebian/20101014T200503Z/</a> lenny main
# Main Debian repository
deb     <a href="http://snapshot.debian.org/archive/debian/20101014T200503Z/">http://snapshot.debian.org/archive/debian/20101014T200503Z/</a> lenny main
deb-src <a href="http://snapshot.debian.org/archive/debian/20101014T200503Z/">http://snapshot.debian.org/archive/debian/20101014T200503Z/</a> lenny main
# Security updates
deb     <a href="http://snapshot.debian.org/archive/debian-security/20091004T121501Z/">http://snapshot.debian.org/archive/debian-security/20091004T121501Z/</a> lenny/updates main
deb-src <a href="http://snapshot.debian.org/archive/debian-security/20091004T121501Z/">http://snapshot.debian.org/archive/debian-security/20091004T121501Z/</a> lenny/updates main
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
