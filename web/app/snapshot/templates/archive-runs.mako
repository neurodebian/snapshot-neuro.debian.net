<%inherit file="/page.mako" />

%for run in c.runs:
<a href="${run['run_mr']}/">${run['run']}</a><br />
%endfor

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
