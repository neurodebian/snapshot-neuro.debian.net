<%inherit file="/page.mako" />

<h1>Source package ${c.src} ${c.version}</h1>
<h3>Source files</h3>
<dl>
	% for hash in c.sourcefiles:
		<dt style="font-size: x-small"><code>${hash}</code>:</td>
		% if hash in c.fileinfo:
			<dd>
				<dl>
				% for fi in c.fileinfo[hash]:
					<td><a href="${fi['link']}"><code style="font-size: x-large"><strong>${fi['name']}</strong></code></a></td>
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

	</li>
	%endfor
</dl>
<h2>Binary packages</h2>
	% for binpkg in c.binpkgs:
		<h3>${binpkg['name']} ${binpkg['version']}</h3>
		<dl>
			% for hash in binpkg['files']:
				<dt style="font-size: x-small"><code>${hash}</code>:</td>
				% if hash in c.fileinfo:
					<dd>
						<dl>
						% for fi in c.fileinfo[hash]:
							<td><a href="${fi['link']}"><code style="font-size: x-large"><strong>${fi['name']}</strong></code></a></td>
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

			</li>
			%endfor
		</dl>
	% endfor
## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
