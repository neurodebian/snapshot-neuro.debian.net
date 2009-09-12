<%inherit file="/page.mako" />

%for run in c.runs:
<a href="${run['run']}/">${run['run_hr']}</a><br />
%endfor

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
