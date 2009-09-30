<%inherit file="/page.mako" />

<h1>Source packages ${c.start}*</h1>

%for pkg in c.packages:
<a href="${pkg}/">${pkg}</a><br />
%endfor

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
