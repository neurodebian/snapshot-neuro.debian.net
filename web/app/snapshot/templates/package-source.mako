<%inherit file="/page.mako" />

<h2>Source package ${c.src}</h2>
Available versions:
<ul>
	%for entry in c.sourceversions:
	<li><a href="${entry}/">${entry}</a></li>
	%endfor
</ul>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
