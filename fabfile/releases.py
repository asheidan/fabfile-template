from fabric.api import env
from fabric.api import cd, task
from fabric.contrib.files import exists
from fabric.operations import require, run

@task
def create_directory(release=env.release):
    """ Create the folders needed for a new release
    """
    require('release', 'hosts')
    if not exists('%(projectroot)s' % env):
        run('mkdir %(projectroot)s' % env)

    if not exists('%(commonroot)s' % env):
        run('mkdir %(commonroot)s' % env)

    if not exists('%(versionroot)s' % env):
        run('mkdir %(versionroot)s' % env)

    if not exists('%(releaseroot)s' % env):
        run('mkdir %(releaseroot)s' % env)


@task
def link_directory(release=env.release):
    """ Link a release for easy configuration
    """
    require('hosts')
    with cd('%(projectroot)s' % env):
        run("ln -snf 'releases/%s' current" % release)


@task
def list():
    """ List the deployed releases on the server
    """
    require('hosts')
    with cd('%(versionroot)s' % env):
        run('ls')
