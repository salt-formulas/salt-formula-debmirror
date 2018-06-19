=====
Usage
=====

This file provides the debmirror sample pillars configurations for different
use cases.

A sample of one debmirror mirror configuration (Ubuntu):

.. code-block:: yaml

    parameters:
      debmirror:
        client:
          enabled: true
          mirrors:
            target01:
              force: False
              lock_target: True
              extra_flags: [ '--verbose', '--progress', '--nosource', '--no-check-gpg', '--rsync-extra=none' ]
              method: "rsync" # string
              arch: [ 'amd64' ]
              mirror_host: "mirror.mirantis.com" # rsync
              mirror_root: ':mirror/nightly/ubuntu/'
              target_dir: "/var/www/mirror/ubuntu/"
              log_file: "/var/www/mirror/target01_log.log"
              dist: [ xenial ] #, xenial-security, xenial-updates ]
              section: [ main ] #, multiverse, restricted, universe ]
              exclude_deb_section: [ 'games', gnome, Xfce, sound, electronics, graphics, hamradio , doc, localization, kde, video ]
              filter:
                00: "--exclude=/"
                01: "--exclude='/android*'"
                02: "--exclude='/firefox*'"
                03: "--exclude='/chromium-browser*'"
                04: "--exclude='/ceph*'"
                05: "--exclude='/*-wallpapers*'"
                06: "--exclude='/language-pack-(?!en)'"
                07: "--include='/main(.*)manpages'"
                08: "--include='/main(.*)python-(.*)doc'"
                09: "--include='/main(.*)python-(.*)network'"

**Documentation and bugs**

* http://salt-formulas.readthedocs.io/
   Learn how to install and update salt-formulas

* https://github.com/salt-formulas/salt-formula-debmirror/issues
   In the unfortunate event that bugs are discovered, report the issue to the
   appropriate issue tracker. Use the Github issue tracker for a specific salt
   formula

* https://launchpad.net/salt-formulas
   For feature requests, bug reports, or blueprints affecting the entire
   ecosystem, use the Launchpad salt-formulas project

* https://github.com/salt-formulas/salt-formula-debmirror
   Develop the salt-formulas projects in the master branch and then submit pull
   requests against a specific formula

* https://launchpad.net/~salt-formulas-users
   Join the salt-formulas-users team and subscribe to mailing list if required

* #salt-formulas @ irc.freenode.net
   Use this IRC channel in case of any questions or feedback which is always
   welcome
