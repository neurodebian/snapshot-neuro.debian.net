<%inherit file="/page.mako" />

%for year in c.yearmonths:
<li>${year['year']}:
% for month in year['months']:
<a href="./?year=${year['year']}&month=${month}">${month}</a>
% endfor
</li>
%endfor

## vim:syn=html
## vim:set ts=4:
## vim:set shiftwidth=4:
