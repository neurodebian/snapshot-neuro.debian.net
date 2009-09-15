<%inherit file="/page.mako" />

%for entry in c.ls:
<a href="${entry['target']}/">${entry['name']}</a><br />
%endfor

prev: ${c.neighbors['prev']}<br />
next: ${c.neighbors['next']}<br />

<div class="readdir">
%	if not c.readdir is UNDEFINED:
%		for entry in c.readdir:
			${entry['filetype']}
%			if entry['filetype'] == 'd':
				<a href="${entry['name']}/">${entry['name']}/</a>
%			elif entry['filetype'] == '-':
				<a href="${entry['name']}">${entry['name']}</a>
				${entry['size']}
##				${entry['digest']}
%			elif entry['filetype'] == 'l':
				<a href="${entry['name']}">${entry['name']}</a> -&gt;
				<a href="${entry['target']}">${entry['target']}</a>
%			else:
				Unknown filetype ${entry}
%			endif
			<br/>
%		endfor
		<br />
%	endif
</div>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
