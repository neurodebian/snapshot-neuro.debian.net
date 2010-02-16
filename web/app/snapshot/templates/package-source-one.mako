<%inherit file="/page.mako" />

<h1>Source package ${c.src} ${c.version}</h1>
<h3>Source files</h3>
<dl>
	% for hash in c.sourcefiles:
		<dt style="font-size: x-small"><code>${hash}</code>:</dt>
		% if hash in c.fileinfo:
			<dd>
				<dl>
				% for fi in c.fileinfo[hash]:
					<dt><a href="${fi['link']}"><code style="font-size: x-large"><strong>${fi['name']}</strong></code></a></dt>
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
<h2><a name="binpkgs">Binary packages</a></h2>
	<ul>
	% for binpkg in c.binpkgs:
		<li><a href="#${binpkg['escaped_name']}_${binpkg['escaped_version']}">${binpkg['name']} ${binpkg['version']}</a></li>
	%endfor
	</ul>
	% for binpkg in c.binpkgs:
		<h3><a name="${binpkg['escaped_name']}_${binpkg['escaped_version']}">${binpkg['name']} ${binpkg['version']}</a></h3>
		<div style="font-size: x-small"><a href="#top">top</a> - <a href="#binpkgs">up to binary packages</a></div>
		<dl>
			% for hash in binpkg['files']:
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
	% endfor
## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
