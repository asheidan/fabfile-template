from fabric.api import env, task
from fabric.operations import require, run

from .utils import w
import os

env.pipcachedir = w(lambda: os.path.join(env.projectroot(), "pipcache"))

@task
def create(directory):
    return run("virtualenv '%s'" % directory)


@task
def pip(command):
    require("virtualenvroot")
    pip = os.path.join(env.virtualenvroot,
                       "bin", "pip")
    return run("'%s' %s" % (pip, command))


@task
def install(packages):
    require("pipcachedir")

    pip("install -q --download-cache '%s' %s" % (env.pipcachedir(), packages))
