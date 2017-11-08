from invoke import task
import os
import tempfile
import sys
import stat

#
# This is a [invoke](http://www.pyinvoke.org/) tasks file which is used to automate specific tasks needed
# for debugging and deployment.
#
# invoke needs to be installed inside the virtualenv
#
# pip requirements:
#
# invoke
# virtualenv

venv_path = '.venv'

@task
def install(ctx, fresh=False):
    """ Install the virtual environment.

    :param fresh: Remove the virtual environment before.
    """

    sys_check(ctx)

    deps(ctx)
    db(ctx, fresh, True, True)

@task
@DeprecationWarning
def venv(ctx, fresh=False):
    """ Create the virtual python environment

    :param fresh: Remove the virtual environment before.
    """

    import shutil

    if os.path.exists('.venv'):
        if fresh:
            shutil.rmtree('.venv')
        else:
            print('virtualenv already created, run again with --fresh to reinstall it.')
            return

    ctx.run('virtualenv --python=python3 .venv')

@task
def deps(ctx):
    """ Install project dependencies"""
    ctx.run('pip install --upgrade pip wheel distribute')
    ctx.run('pip install --upgrade -r requirements.txt')

    try:
        import sherlock
    except ImportError:
        ctx.run('cd PlagCheck/hashing/sherlock && python setup.py install')

@task
def populate(ctx):
    """ Run populate_demo_data """
    ctx.run('python manage.py populate_demo_data', pty=True)

@task
def db(ctx, fresh=False, demo=False, plagcheck=True):
    """ Wipe databases and recreate them.

    :param plagcheck: Wipe also plagcheck database (default=False)
    :param demo: Populate demo data (default=True)
    :param migrate: Do also migrations (default=False)
    """
    settings = getSettings(ctx)

    print_info('Wiping databases')
    if fresh:
        if 'postgres' in settings.DATABASES['default']['ENGINE']:
            psql_cmd(ctx, 'DROP DATABASE IF EXISTS aurora;')
            psql_cmd(ctx, 'CREATE DATABASE aurora OWNER aurora;')
        else:
            if os.path.isfile(settings.DATABASES['default']['NAME']):
                os.remove(settings.DATABASES['default']['NAME'])

        if plagcheck and 'plagcheck' in settings.DATABASES['default']['ENGINE']:
            psql_cmd(ctx, 'DROP DATABASE IF EXISTS plagcheck;')
            psql_cmd(ctx, 'CREATE DATABASE plagcheck OWNER aurora;')
        else:
            if os.path.isfile(settings.DATABASES['plagcheck']['NAME']):
                os.remove(settings.DATABASES['plagcheck']['NAME'])

    print_info('Running migrate')
    ctx.run('python manage.py migrate')
    if plagcheck:
        print_info('Running migrate for plagcheck')
        ctx.run('python manage.py migrate --database=plagcheck --noinput')
        ctx.run('celery purge -f')

    if fresh and not demo:
        if query_yes_no('Do you want to install demo data?'):
            demo = True

    if demo:
        populate(ctx)

@task
def server(ctx):
    """ Run the debugging webserver"""
    ctx.run('python manage.py runserver', pty=True)

@task
def daphne(ctx):
    """Run daphne interface server"""
    ctx.run('daphne AuroraProject.asgi:channel_layer -p 8001')

@task
def asgiworker(ctx):
    """Run asgi worker for daphne"""
    ctx.run('python manage.py runworker')

@task
def uwsgi(ctx):
    """Run uWSGI server"""
    ctx.run('uwsgi /etc/uwsgi.ini')

@task
def nginx(ctx):
    """Run nginx"""
    ctx.run('sudo nginx')

@task
def celery(ctx, worker=1):
    """ Run the background worker"""
    ctx.run('celery -A AuroraProject worker -l info -E --loglevel=INFO --concurrency={0}'.format(worker), pty=True)

@task
def flower(ctx):
    """ Run the monitor for the message queue"""
    ctx.run('celery flower', pty=True)

@task
def static(ctx):
    """ Install static files"""
    ctx.run('python manage.py collectstatic --clear --noinput')
    ctx.run('python manage.py collectstatic --noinput')

@task
def server(ctx):
    """ Run the debugging webserver"""
    ctx.run('python manage.py runserver', pty=True)

@task
def flower(ctx):
    """ Run the monitor for the message queue"""
    ctx.run('celery flower', pty=True)


# Utility functions and constants

RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"


def sys_check(ctx):
    if sys.version_info >= (3,5):
        print_error('Django 1.7 is not supported on python version 3.5 and greater')
        print_error('Please install python3.4 to run compatible')
        raise EnvironmentError('Incompatible python version')


def print_colored(msg, color):
    print(color, end='', flush=True)
    print(msg)
    print(RESET, end='', flush=True)


def print_info(msg):
    print_colored(msg, GREEN)


def print_error(msg):
    print_colored(msg, RED)


def psql_cmd(ctx, cmd):

    """
    # for multiline psql commands; not used atm
    tmp_file = tempfile.NamedTemporaryFile(mode='w+')
    tmp_file.write(cmd)

    st = os.stat(tmp_file.name)
    os.chmod(tmp_file.name, st.st_mode | 0o444)
    """

    ctx.sudo('psql -c "{}"'.format(cmd), user='postgres')

    """tmp_file.close()"""


def getSettings(ctx):
    with ctx.prefix('source {}/bin/activate &&'.format(venv_path)):

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AuroraProject.settings")
        from django.conf import settings

        return settings


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    From: https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")