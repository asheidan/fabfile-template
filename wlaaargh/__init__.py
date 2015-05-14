from fabric.api import cd, env, task
# from fabric.context_managers import cd
# from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project
from fabric.operations import require  # sudo, put

from .utils import w
from . import git
from . import releases
from . import virtualenv

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
    require('hosts', 'deploybranch', 'piprequirementsfile')

    # Make sure directories exists
    releases.create_directory()

    # Transfer
    git.push(env.deploybranch)

    # Copy code to releasedirectory
    git.remote_export(env.deploybranch, env.releaseroot)

    # Setup new virtualenv for new release
    env.virtualenvroot = os.path.join(env.releaseroot(), "virtualenv")
    virtualenv.create(env.virtualenvroot)

    # Install packages in virtualenv
    with cd(env.releaseroot()):
        virtualenv.install("-r %s" % env.piprequirementsfile)

    # Set the deployed release as "current"
    releases.link_directory()
