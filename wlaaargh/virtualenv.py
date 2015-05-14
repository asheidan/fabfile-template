from fabric.api import env, task
from fabric.operations import require

from .utils import w, run
import os

env.pipcachedir = w(lambda: os.path.join(env.projectroot(), "pipcache"))


@task
def create(directory):
    """ Create a new virtualenv in the given directory """
    return run("virtualenv -q '%s'" % directory)


@task
def pip(command):
    """ Use pip from a virtualenv """
    require("virtualenvroot")
    pip = os.path.join(env.virtualenvroot,
                       "bin", "pip")
    return run("'%s' %s" % (pip, command))


@task
def install(packages):
    """ Install packages into the virtualenv

        Uses a local cache to speed up installation.
    """
    require("pipcachedir")

    pip("install -q --download-cache '%s' %s" % (env.pipcachedir(), packages))
