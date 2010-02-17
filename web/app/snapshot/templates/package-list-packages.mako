<%inherit file="/page.mako" />

<h1>Source packages ${c.start}*</h1>

<p>
%for pkg in c.packages:
<a href="${pkg['quoted']}/">${pkg['raw']}</a><br />
%endfor
</p>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
