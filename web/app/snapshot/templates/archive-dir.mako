<%inherit file="/page.mako" />

%for entry in c.ls:
<a href="${entry['target']}/">${entry['name']}</a><br />
%endfor

first: ${c.nav['first']}<br />
prev: ${c.nav['prev']}<br />
now: ${c.run['run']}<br />
next: ${c.nav['next']}<br />
last: ${c.nav['last']}<br />

<table class="readdir">
	%if not c.readdir is UNDEFINED:
			<tr>
				<th>&nbsp;</th>
				<th>Name</th>
				<th style='text-align: right'>Size</th>
				<th>first seen</th>
				<th>last seen</th>
			</tr>
		%for entry in c.readdir:
			<tr>
				<td>${entry['filetype']}</td>
				% if entry['filetype'] == 'd':
					<td colspan="2"><a href="${entry['name']}/">${entry['name']}/</a></td>
				% elif entry['filetype'] == '-':
					<td><a href="${entry['name']}">${entry['name']}</a></td>
					<td style='text-align: right'>${entry['size']}</td>
				% elif entry['filetype'] == 'l':
					<td colspan="2">
						<a href="${entry['name']}">${entry['name']}</a> -&gt;
						<a href="${entry['target']}">${entry['target']}</a>
					</td>
				% else:
					<td colspan="2">
						Unknown filetype ${entry}
					</td>
				% endif
				<td>
					% if not entry['first_run'] is None:
						${entry['first_run']}
					% endif
				</td>
				<td>
					% if not entry['last_run'] is None:
						${entry['last_run']}
					% endif
				</td>
			</tr>
		% endfor
		<br />
	% endif
</table>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
