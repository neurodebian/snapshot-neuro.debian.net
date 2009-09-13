<%inherit file="/page.mako" />

%for entry in c.ls:
<a href="${entry['target']}/">${entry['name']}</a><br />
%endfor

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
