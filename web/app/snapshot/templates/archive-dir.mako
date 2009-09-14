<%inherit file="/page.mako" />

%for entry in c.ls:
<a href="${entry['target']}/">${entry['name']}</a><br />
%endfor

%	if not c.readdir is UNDEFINED:
		d <a href="../">..</a><br />
%		for entry in c.readdir:
			${entry['filetype']}
%			if entry['filetype'] == 'd':
				<a href="${entry['name']}/">${entry['name']}</a>
%			else:
				${entry['name']}
				${entry['size']}
				${entry['digest']}
%			endif
			<br/>
%		endfor
		<br />
%	endif

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
