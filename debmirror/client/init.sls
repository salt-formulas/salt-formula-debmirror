{%- from "debmirror/map.jinja" import client with context %}
{%- if client.enabled %}

debmirror_client_packages:
  pkg.installed:
  - names: {{ client.pkgs }}

{%- for mirror_name, opts in client.get("mirrors",{}).iteritems() %}

{%- if opts.get('enabled', True ) %}
debmirror_{{ mirror_name }}_present:
  debmirror.mirror_present:
    - name: {{ mirror_name }}
    - require:
      - debmirror_client_packages
  {%- if grains['saltversioninfo'][0] >= 2017 and grains['saltversioninfo'][1] >= 7 %}
    - retry:
        attempts: {{ opts.get('fetch_retry' , 1) }}
        until: True
        interval: 5
        splay: 2
  {%- endif %}
{% endif %}

{%- endfor %}
{% endif %}

