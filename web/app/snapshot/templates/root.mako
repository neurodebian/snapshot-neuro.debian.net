<%inherit file="/page.mako" />


<table class="rootmaintable">
<tr>
<td>
<h1>Archives</h1>

<p>Browse ftp archive snapshots from one of the following archives:</p>

<ul>
	% for name in c.names:
	<li><a href="archive/${name}/">${name}</a></li>
	%endfor
</ul>

<h1>Packages</h1>

Search in the index:</br>
<ul class="inlineList">
%for letter in c.srcstarts:
	<li><a href="package/?cat=${letter}">${letter}</a></li>
%endfor
</ul>

<form action="package/">
<p>Or enter a source package name directly: <input name="src" /> <input type="submit" value="Submit" /></p>
</form>

</td>

<td>
<div class="rootmaintext">
<h1>Snapshot.debian.org</h1>
<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque vehicula
lobortis mauris vitae congue. In porttitor augue ut risus vulputate mattis. In
ac ante augue, a fermentum neque. Mauris volutpat volutpat urna sed euismod.
Cras nec consequat velit. Etiam id nibh id turpis bibendum rutrum. Quisque et
eros nisi, ac mattis augue. In hac habitasse platea dictumst. Morbi nec leo
turpis, non lacinia augue. Phasellus hendrerit mollis nunc, sit amet pulvinar
sem vestibulum ac. Curabitur fermentum nulla et tortor viverra non sollicitudin
lectus condimentum. Aliquam luctus fringilla dui, ut faucibus mi laoreet
vehicula. In interdum, dui in dictum mollis, mi purus laoreet enim, non congue
lacus metus ut felis. Nam nisi elit, dictum id accumsan sit amet, sodales vitae
metus.
</p>

<p>
Maecenas quam urna, laoreet eu condimentum eget, posuere vel libero. Ut vel arcu eu ante mollis ornare quis a turpis. Proin iaculis pulvinar massa, non hendrerit magna commodo ac. Sed vel felis augue, vel lobortis enim. Proin ultricies sem ac augue porta at vehicula dolor posuere. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse fermentum lectus at elit laoreet eget commodo arcu blandit. Aliquam pulvinar pretium elit, nec ultricies nisi consectetur sed. Ut lacinia nisi tempor tortor adipiscing consequat. Mauris a imperdiet odio. Sed dapibus viverra nulla eget tincidunt.
</p>

<h1>News</h1>
<h2>2010-01-21</h2>
<p>
Syncing stuff to sibelius.
</p>

<h2>2010-01-01</h2>
<p>
It is 2010 now.
</p>

</div>
</td>
</tr>
</table>
