<%inherit file="/page.mako" />

<h1>Binary package ${c.binary}</h1>
<p>
Available versions:
</p>
<ul>
	%for entry in c.binaryversions:
	<li><a href="${entry['link']}#${entry['escaped_name']}_${entry['escaped_version']}">${entry['binary_version']} (source: ${entry['source']} ${entry['version']})</a></li>
	%endfor
</ul>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
