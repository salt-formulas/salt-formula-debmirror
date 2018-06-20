#!/usr/bin/env python
"""
Management of debmirror
=======================

Create debian mirrors, using debmirror
--------------------------------------

.. code-block:: yaml
    debmirror_test1_present:
      debmirror.mirror_present:
        - name: test1

"""
import logging
import os
from functools import wraps
from salt.exceptions import CommandExecutionError, SaltInvocationError
log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load this module if debmirror is installed with deps.
    '''
    return 'debmirror'


def _test_call(method):
    (resource, functionality) = method.func_name.split('_')
    if functionality == 'present':
        functionality = 'updated'
    else:
        functionality = 'removed'

    @wraps(method)
    def check_for_testing(name, *args, **kwargs):
        if __opts__.get('test', None):
            return _no_change(name, resource, test=functionality)
        return method(name, *args, **kwargs)

    return check_for_testing


def _created(name, resource, resource_definition={}):
    changes_dict = {'name': name,
                    'changes': resource_definition,
                    'result': True,
                    'comment': '{0} {1} created'.format(resource, name)}
    return changes_dict


def _failed(name, resource, resource_definition={}):
    changes_dict = {'name': name,
                    'changes': resource_definition,
                    'result': False,
                    'comment': '{0} {1} failed to create'.format(resource,
                                                                 name)}
    return changes_dict


def _no_change(name, resource, test=False):
    changes_dict = {'name': name,
                    'changes': {},
                    'result': True}
    if test:
        changes_dict['comment'] = \
            '{0} {1} will be {2}'.format(resource, name, test)
    else:
        changes_dict['comment'] = \
            '{0} {1} is in correct state'.format(resource, name)
    return changes_dict


def _check_state(name, tgt):
    lock_file = _get_target_path(name, tgt)['lock_file']
    if os.path.isfile(lock_file) and not tgt.get('force', False):
        return _no_change(name, '{} exist=>repo locked.'.format(lock_file))
    return False


def _get_target_path(name, tgt):
    if not tgt.get('target_dir', False):
        raise SaltInvocationError('Argument "target_dir" is mandatory! ')
    return {'target_dir': tgt.get('target_dir'),
            'lock_file': tgt.get('lock_file',
                                 os.path.join(tgt.get('target_dir'),
                                              '.lockmirror')),
            'log_file': tgt.get('log_file', '/var/log/debmirror_'.join(name))}


def _get_env(tgt):
    env = {}
    for k in ['http_proxy', 'https_proxy', 'ftp_proxy', 'rsync_proxy']:
        if tgt.get(k, False):
            env[k] = tgt[k]
            env[k.upper()] = env[k]
    if tgt.get('no_proxy', False):
        env['no_proxy'] = ','.join(str(x) for x in tgt['no_proxy'])
        env['no_proxy'.upper()] = env['no_proxy']
    return env


def _get_cmdline(name, tgt):
    cmdline = " debmirror "
    if tgt.get('extra_flags'):
        cmdline += ' '.join(tgt['extra_flags'])
    if tgt.get('dist'):
        cmdline += ' --dist=' + ",".join(tgt['dist'])
    if tgt.get('section'):
        cmdline += ' --section=' + ",".join(tgt['section'])
    if tgt.get('method'):
        cmdline += ' --method=' + tgt.get('method')
    if tgt.get('mirror_host'):
        cmdline += ' --host="{}"'.format(tgt.get('mirror_host'))
    if tgt.get('mirror_root'):
        cmdline += ' --root="{}"'.format(tgt.get('mirror_root'))
    if tgt.get('arch', 'amd64'):
        cmdline += ' --arch=' + ','.join(tgt.get('arch'))
    if tgt.get('exclude_deb_section'):
        for section in tgt['exclude_deb_section']:
            cmdline += " --exclude-deb-section='" + section + "'"
    if tgt.get('filter'):
        for key, value in enumerate(sorted(tgt['filter'])):
            cmdline += " " + tgt['filter'][value]
    if tgt.get('target_dir', False):
        cmdline += ' ' + _get_target_path(name, tgt)['target_dir']
    return cmdline


def _update_mirror(name, tgt):
    # Remove old lock file, is was.
    lock_file = _get_target_path(name, tgt)['lock_file']
    if os.path.isfile(lock_file):
        log.debug("Removing lockfile:{} for mirror{}".format(lock_file, name))
        __states__['file.absent'](lock_file)
    cmdline = _get_cmdline(name, tgt)
    # fetch ENV params for proxy
    env_vars = _get_env(tgt)
    # init file logger
    l_dir = os.path.dirname(tgt['log_file'])
    if not os.path.isdir(l_dir):
        __salt__['file.makedirs'](l_dir + '/')
    fh = logging.FileHandler(
        "{0}".format(_get_target_path(name, tgt)['log_file']))
    fh.setLevel(logging.DEBUG)
    fh_format = logging.Formatter(
        '%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
    fh.setFormatter(fh_format)
    log2file = logging.getLogger("debmirror")
    log2file.addHandler(fh)
    result = __salt__['cmd.run_all'](cmdline, redirect_stderr=True,
                                     env=env_vars)
    log2file.debug(result['stdout'])
    # destroy file logger
    for i in list(log2file.handlers):
        log2file.removeHandler(i)
        i.flush()
        i.close()
    if result['retcode'] != 0:
        # raise CommandExecutionError(result['stderr'])
        return _failed(name,
                       "debmirror failed.Reason {0}".format(result['stderr']))
    if tgt.get('lock_target', None):
        __states__['file.touch'](lock_file)
    return _created(name, "Mirror {0} created.".format(name))


@_test_call
def mirror_present(name, **kwargs):
    '''

    :param name: mirror key name
    '''
    try:
        tgt = __salt__['config.get']('debmirror')['client']['mirrors'][name]
    except KeyError:
        comment = 'Mirror "{0}" not exist in configurathion,skipping..'.format(
            name)
        return _no_change(name, comment)

    current_state = _check_state(name, tgt)
    if not current_state:
        return _update_mirror(name, tgt)
    return current_state
