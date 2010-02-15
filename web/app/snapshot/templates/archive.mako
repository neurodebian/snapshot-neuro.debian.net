<%inherit file="/page.mako" />

<h1>Archive ${c.archive}</h1>

<ul>
%for year in c.yearmonths:
<li>${year['year']}:
% for month in year['months']:
<a href="./?year=${year['year']}&month=${month}">${"%02d"%month}</a>
% endfor
</li>
%endfor
</ul>

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
