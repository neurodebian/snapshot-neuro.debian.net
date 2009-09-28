<%inherit file="/page.mako" />

%for entry in c.ls:
<a href="${entry['target']}/">${entry['name']}</a><br />
%endfor

<div style="font-size: x-small">
	% if c.nav['first'] != c.run['run']:
		<acronym title="${c.nav['first']}"><a href="${c.nav['first_link']}">first</a></acronym>
		&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;
		<acronym title="${c.nav['prev']}"><a href="${c.nav['prev_link']}">prev</a></acronym>
	% else:
		No previous version of this directory available.
	% endif
	&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;
	${c.run['run']}
	&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;
	% if c.nav['last'] != c.run['run']:
		<acronym title="${c.nav['next']}"><a href="${c.nav['next_link']}">next</a></acronym>
		&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;
		<acronym title="${c.nav['last']}"><a href="${c.nav['last_link']}">last</a></acronym>
	% else:
		No later version of this directory available.
	%endif
</div>

<table class="readdir">
	%if not c.readdir is UNDEFINED:
			<tr>
				<th>&nbsp;</th>
				<th>Name</th>
				<th style='text-align: right'>Size</th>
##				<th>first seen</th>
##				<th>last seen</th>
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
##				<td>
##					% if not entry['first_run'] is None:
##						${entry['first_run']}
##					% endif
##				</td>
##				<td>
##					% if not entry['last_run'] is None:
##						${entry['last_run']}
##					% endif
##				</td>
##				## debugging only
##				% if entry['filetype'] == '-':
##					<td>${entry['digest']}</td>
##				% endif
			</tr>
		% endfor
		<br />
	% endif
</table>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
