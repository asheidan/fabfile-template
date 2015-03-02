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


from . import releases

@task
def local():
    env.hosts = ["localhost"]


@task
def staging():
    """ Sets hosts for staging-env
    """
    env.hosts = ["user@sta.gi.ng"]


@task
def production():
    """ Sets hosts for production-env
    """
    env.hosts = ["user@pro.ducti.on"]

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
def deploy():
    """ Deploys a new version to the server
    """
    require('hosts', provided_by=environments)
    create_release()
    rsync_project(local_dir="./",
                  remote_dir=env.releaseroot,
                  extra_opts='--link-dest="%(currentroot)s"' % env)
    link_release()


