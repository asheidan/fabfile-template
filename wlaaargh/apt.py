from fabric.api import task
from fabric.operations import sudo


@task
def install(packages):
    """ Install apt-packages listed in iterable packages """
    sudo("apt-get install %s" % " ".join(packages))


@task
def install_from_file(requirementsfile):
    """ Install apt-packages listed in requirementsfile """
    sudo("xargs apt-get install < '%s'" % requirementsfile)
