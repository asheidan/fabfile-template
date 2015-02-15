from fabric.api import cd, env, task
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project
from fabric.operations import require, run, sudo

import time
import os

env.hostnames = {
    'staging': [],
    'production': [],
}

env.wwwroot = "/var/www"
env.projectname = "fabfile_deploy"

env.projectroot = os.path.join(env.wwwroot, env.projectname)
env.release = time.strftime("%Y%m%d%H%M%S")

env.commonroot = os.path.join(env.projectroot, 'common')
env.currentroot = os.path.join(env.projectroot, 'current')
env.versionroot = os.path.join(env.projectroot, 'releases')
env.releaseroot = os.path.join(env.versionroot, env.release)


@task
def local():
    pass


@task
def staging():
    """ Sets hosts for staging-env
    """
    env.hosts = "user@sta.gi.ng"


@task
def production():
    """ Sets hosts for production-env
    """
    env.hosts = []

environments = [local, staging, production]

@task
def bootstrap():
    """ Installs necessary software on the server
    """
    pass


@task
def setup():
    """ Sets up the folder structure on the server
    """
    pass

@task
def create_release(release=env.release):
    """ Create the folders needed for a new release
    """
    require('release', 'hosts', provided_by=environments)
    if not exists('%(projectroot)s' % env):
        run('mkdir %(projectroot)s' % env)

    if not exists('%(commonroot)s' % env):
        run('mkdir %(commonroot)s' % env)

    if not exists('%(versionroot)s' % env):
        run('mkdir %(versionroot)s' % env)

    if not exists('%(releaseroot)s' % env):
        run('mkdir %(releaseroot)s' % env)


@task
def deploy():
    """ Deploys a new version to the server
    """
    require('hosts', provided_by=environments)
    create_release()
    rsync_project(local_dir="./",
                  remote_dir=env.releaseroot,
                  extra_opts='--link-dest="%(currentroot)s"' % env)
    link_release()


@task
def link_release(release=env.release):
    """ Link a release for easy configuration
    """
    require('hosts', provided_by=environments)
    with cd('%(projectroot)s' % env):
        run("ln -snf 'releases/%s' current" % release)


@task
def list_releases():
    """ List the deployed releases on the server
    """
    require('hosts', provided_by=environments)
    with cd('%(versionroot)s' % env):
        run('ls')
