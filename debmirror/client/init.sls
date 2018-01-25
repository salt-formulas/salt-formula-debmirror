{%- from "debmirror/map.jinja" import client with context %}
{%- if client.enabled %}

debmirror_client_packages:
  pkg.installed:
  - names: {{ client.pkgs }}

{%- for mirror_name, opts in client.get("mirrors",{}).iteritems() %}

debmirror_{{ mirror_name }}_present:
  debmirror.mirror_present:
    - name: {{ mirror_name }}
    - require:
      - debmirror_client_packages

{%- endfor %}
{% endif %}

