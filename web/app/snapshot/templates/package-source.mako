<%inherit file="/page.mako" />

<h1>Source package ${c.src}</h1>
<p>
Available versions:
</p>
<ul>
	%for entry in c.sourceversions:
	<li><a href="${entry['quoted']}/">${entry['raw']}</a></li>
	%endfor
</ul>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
