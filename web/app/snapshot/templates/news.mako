<h1>News</h1>
<h2>2010-09-07</h2>
<p>
Renamed the backports.org archive to debian-backports as it has now
<a href="http://lists.debian.org/20100905211658.GH7615@lisa.snow-crash.org">moved
to debian.org infrastructure</a>.  A rewrite rule has been put in place
so old URLs should continue to work (at least for HTTP clients that know
how to follow HTTP redirects).
</p>

<h2>2010-08-16</h2>
<p>
Set up a caching proxy in front of the two snapshot webservers.  This will help
in cases where an entire organisation uses various apt sources.list entries on
a lot of their machines.
</p>
<p>
Usually such entities would use proxy caches like squid and then there is no
problem, assuming the cache works correctly.  Unfortunately apt-cacher, apparently
a common choice which is supposed to be smarter for debian archives, completely ignores the
Cache-Control headers that snapshot sends and hits this service for all
requests made to anything under <code>dist/</code>.  A single <code>apt-get
update</code> can cause up to a few dozen of such requests and when multiplied
by scores of machines - all running the update at the same time - this caused
the snapshot backend to run into limits.  Now such requests won't hit the backend
any more.
</p>

<h2>2010-04-12</h2>
<p>
Publicly <a href="http://www.debian.org/News/2010/20100412">announce the snapshot.debian.org service</a>.  Yay.
</p>

<hr style="height:1px;" />
<p>For older entries see <a href="oldnews">the older news page</a>.</p>
