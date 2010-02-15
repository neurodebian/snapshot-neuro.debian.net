<%inherit file="/page.mako" />

<h1>Archive ${c.archive}</h1>
<h2>${c.year}-${c.month}</h2>

<p>
%for run in c.runs:
<a href="${run['run_mr']}/">${run['run']}</a><br />
%endfor
</p>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
