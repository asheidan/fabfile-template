from fabric.api import cd, env, task
# from fabric.context_managers import cd
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project
from fabric.operations import require, run, sudo, put

from utils import w

import time
import os

env.hostnames = {
    'staging': [],
    'production': [],
}


def _env(key):
    value = env.get(key)
    if hasattr(value, "__call__"):
        return value()
    else:
        return value

env.wwwroot = "/var/www"
env.projectname = "fabfile_deploy"
env.localroot = "./"

env.projectroot = w(lambda: os.path.join(env.wwwroot, env.projectname))
env.release = time.strftime("%Y%m%d%H%M%S")

env.commonroot = w(lambda: os.path.join(env.projectroot(), 'common'))
env.currentroot = w(lambda: os.path.join(env.projectroot(), 'current'))
env.versionroot = w(lambda: os.path.join(env.projectroot(), 'releases'))
env.releaseroot = w(lambda: os.path.join(env.versionroot(), env.release))


from . import releases
from .deploy import transfer


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
    require('hosts')
    releases.create_directory()
    rsync_project(local_dir=env.localroot,
                  remote_dir=env.releaseroot,
                  exclude=["*.py[co]", "*~", "__pycache__", ".DS_Store"],
                  extra_opts='--link-dest="%(currentroot)s"' % env)

    releases.link_directory()


