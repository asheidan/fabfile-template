from fabric.api import env
from fabric.operations import run as original_run
from fabric.operations import sudo


def impersonate(*command, **kwargs):
    if "user" not in kwargs:
        kwargs["user"] = env.impersonate_user

    sudo(*command, **kwargs)


def run(*command, **kwargs):
    if "impersonate_user" in env:
        impersonate(*command, **kwargs)
    else:
        original_run(*command, **kwargs)


class w:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __str__(self):
        return self()

    def replace(self, *args, **kwargs):
        return self().replace(*args, **kwargs)
