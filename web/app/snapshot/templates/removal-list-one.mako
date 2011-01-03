<%inherit file="/page.mako" />

<h1>Removal log #${c.removal['removal_log_id']}</h1>

<p style="font-size: small">${c.removal['entry_added']}</p>
<pre>${c.removal['reason']}</pre>

<h1>Affected files</h1>

<dl>
	% for hash in c.files:
		<dt style="font-size: x-small"><code>${hash}</code>:</dt>
		% if hash in c.fileinfo:
			<dd>
				<dl>
				% for fi in c.fileinfo[hash]:
					<dt><a href="${fi['link']}"><code style="font-size: large"><strong>${fi['name']}</strong></code></a></dt>
					<dd>
						Seen in ${fi['archive_name']} on ${fi['run']} in
						% if 'dirlink' in fi:
							<a href="${fi['dirlink']}">${fi['path']}</a>.
						% else: 
							${fi['path']}.
						% endif
						<br />
						Size: ${fi['size']}
					</dd>
				% endfor
				</dl>
			</dd>
		% endif
	%endfor
</dl>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
