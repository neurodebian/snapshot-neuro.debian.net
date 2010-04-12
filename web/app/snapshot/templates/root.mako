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
<h2>2010-04-12</h2>
<p>
Publicly <a href="http://www.debian.org/News/2010/20100412">announce the snapshot.debian.org service</a>.  Yay.
</p>

<h2>2010-03-15</h2>
<p>
The host stabile.debian.org is once again creating snapshots as snapshot-master,
all the data from the secondary setup on sibelius have been merged, so all is
back to normal.
</p>

<h2>2010-03-09</h2>
<p>
In the meantime we found a new controller and snapshot-master now is back
online.  One disk in one of the four RAID-6 arrays has also failed and we
are looking into replacing that soon.
</p><p>
The secondary setup on sibelius has faithfully continued to do snapshots
(except for backports.org for which we somehow failed to get pushed) and
we are in the process of merging those new snapshots into the database on
master.
</p><p>
The disk related problems raised some concerns about data integrity.
The actual data of snapshot is kept in the <i>farm</i>, a content
addressed file system.  That is to say that all files are named by the
SHA-1 hashsum of their content.  The metadata which links hashes to
packages and files in snapshotted archive trees is stored in a
PostgreSQL database.  To verify the health of the farm we have
implemented a rudimentary fsck which verifies two things:
</p>
<ul><li>First, that all the filenames match their actual content.
This check turned up several mismatches.  In four instances the
file on disk actual had the correct content as referenced by Release
and Packages files, but for some reason we calculated the wrong hash
during import time.  Yay.  This was relatively easy to repair as it
only required renaming the files on disk and updating all references
in the database.<br />
Then there were some 20 or 40 files with the same checksum (the hash of
the empty file), as a result of XFS failing to write the files' contents
when the disks went away two weeks ago.  Given that those import runs'
metadata never got committed in PostgreSQL either we could simply remove
those files.<br />
Another four files of the two latest mirrorruns of the debian archive that did
make it to our database actually turned out to be corrupt.  In all likelyhood
also as a result of XFS not liking it when suddenly its block device disappears
partially.  The files in questions were Packages.{gz,bz2} of the sid installer
for amd64 and s390.  The corrupted files have been removed.  We are
considering trying to reconstruct those files from the rest of the
ftp tree (it should after all just be an apt-ftparchive run), but
it is not a very high priority.
</li>
<li>The other check verified that for each hash referenced in the
PostgreSQL database we actually have the corresponding item in the
farm.  No errors were found by this check (except the four files
reportedly removed above).
</li></ul>
<p>
We are also currently importing historical snapshots of the debian-ports
ftp tree as requested in <a href="http://bugs.debian.org/571118">Bug
#571118</a>.
</p>
<p>
If all goes well we should be back to a normal state in a couple of
days.  Then we have to deal with removing things that got removed
from the source archives due to licensing problems.  Once that last
hurdle is taken we can finally announce it and make it an official
service.
</p>

<h2>2010-02-24</h2>
<p>
So we finally finally got a second machine up and serving a copy of snapshot.
Of course this means that now a disk controller breaks in the snapshot-master
machine and thus half of our disks are rendered inaccessible.  Even raid6
doesn't like that very much.
</p><p>
Therefore snapshot will not get any new data currently and the service is
provided by only one of the servers of what was previously a DNS round robin
rotation.
</p><p>
We had planned to eventually set up a secondary snapshot master that would do
the import runs into an alternate database for just such occassions.  This
occurance prompted us to somewhat expediate that project.
</p><p>
So while currently snapshot will not get any updates we should be able to
inject most mirrorruns into snapshot-master when it gets back.  We'll have lost
a few runs of volatile and the main debian archive, but we should not see a gap
longer than roughly a day.
</p>

<h2>2010-02-20</h2>
<p>
Finished setting up mirroring scripts.  While snapshot-master (stabile) still
is the entity importing new snapshots into the system all the data is now
replicated to a secondary site (sibelius).  The web front-end runs on both of
them.
</p>

</div>
</td>
</tr>
</table>
