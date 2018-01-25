debmirror:
  client:
    enabled: true
    mirrors:
      target01:
        extra_flags: '--verbose --progress --nosource --no-check-gpg --rsync-extra=none'
        method: "rsync" # string
        arch: [ 'amd64' ]
        mirror_host: "archive.ubuntu.com" # rsync
        mirror_root: ':ubuntu/' # rsync
        target_dir: "/tmp/mirror/ubuntu/"
        log_file: "/tmp/target01_log.log"
        dist: [ xenial ] #, xenial-security, xenial-updates ]
        section: [ main ] #, multiverse, restricted, universe ]
        exclude_deb_section: [ 'games', gnome, Xfce, sound, electronics, graphics, hamradio , doc, localization, kde, video ]
        filter:
          00: "--exclude='/*'"  # exclude all for test
        lock_target: True
        force: True
