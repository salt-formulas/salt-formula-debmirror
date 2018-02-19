
==================================
debmirror Formula
==================================

Service debmirror description


Sample Pillars
==============

Example for one debmirror mirror, ubuntu.

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

More Information
================

* https://github.com/salt-formulas/salt-formula-debmirror
* Check debmirror/schemas/client.yaml for parameters description


Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate issue tracker. Use GitHub issue tracker for specific salt
formula:

    https://github.com/salt-formulas/salt-formula-debmirror/issues

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit pull request against specific formula.

You should also subscribe to mailing list (salt-formulas@freelists.org):

    https://www.freelists.org/list/salt-formulas

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net

Read more
=========

* links
