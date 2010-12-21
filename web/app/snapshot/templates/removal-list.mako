<%inherit file="/page.mako" />

<h1>Removal log</h1>

<dl>
%for e in c.removals:
	<dt style="font-size: small">${e['entry_added']}</dt>
	<dd>
		<pre>${e['reason']}</pre>
		<p style="font-size: x-small">[<a href="${e['removal_log_id']}">affected files]</a></p>
	</dd>
%endfor
</dl>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
