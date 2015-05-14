from fabric.api import env, task
from fabric.contrib.files import exists
from fabric.operations import local

from .utils import w, run

import os

env.deploybranch = w(lambda: "master")
env.remoterepo = w(lambda: os.path.join(env.projectroot(),
                                        "repo.git"))


@task
def push(commit, local_repo=".git", remote_repo=None):
    """ Push specific commit to remote (bare) repo
    """

    remote_repo = remote_repo if remote_repo is not None else env.remoterepo()

    if not exists(env.remoterepo()):
        print("%s does not exists" % env.remoterepo())
        run("git init --bare '%s'" % env.remoterepo())

    # host_info = "%s@%s:%s" % (env.user, env.host_string, env.port)
    command = "git --git-dir='%s' push -f -q 'ssh://%s@%s%s' '%s'" % (
        local_repo, env.impersonate_user, env.host_string, env.remoterepo(), commit
    )
    return local(command, )  # env.passwords[host_info])


@task
def remote_export(commit, directory):
    """ Export specific commit to directory
    """
    return run(("git --git-dir='%s' archive --format=tar '%s' |"
                " tar -x -C '%s' -f -") % (env.remoterepo(), env.deploybranch(), env.releaseroot()))
