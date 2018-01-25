{%- if pillar.debmirror is defined %}
include:
{%- if pillar.debmirror.client is defined %}
- debmirror.client
{%- endif %}
{%- endif %}
