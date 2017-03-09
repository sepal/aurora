from invoke import task
import os
import sys

#
# This is a [invoke](http://www.pyinvoke.org/) tasks file which is used to automate specific tasks needed
# for debugging and deployment.
#



@task
def install(ctx, fresh=False):
    """ Install the virtual environment.

    :param fresh: Remove the virtual environment before.
    """
    venv(ctx, fresh)


@task
def prepare(ctx, fresh=False):
    """ Install requirements and prepare database.

    :param fresh: Remove the database before.
    """
    deps(ctx)
    db(ctx, fresh=fresh)

    # populate database only on a fresh database
    if fresh:
        populate(ctx)


@task
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
    ctx.run('pip install --upgrade -r requirements_dev.txt')

    try:
        import sherlock
    except ImportError:
        ctx.run('cd PlagCheck/hashing/sherlock && python setup.py install')


@task
def populate(ctx):
    """ Run populate_demo_data """
    ctx.run('python manage.py populate_demo_data', pty=True)


@task
def db(ctx, fresh=False, demo=False, plagcheck=False):
    """ Wipe databases and recreate them.

    :param plagcheck: Wipe also plagcheck database (default=False)
    :param demo: Populate demo data (default=True)
    :param migrate: Do also migrations (default=False)
    """
    if fresh:
        ctx.run('rm -f database.db')

    ctx.run('python manage.py migrate')

    if plagcheck:
        ctx.run('rm -f database-plagcheck.db')
        ctx.run('python manage.py migrate --database=plagcheck --noinput')
        ctx.run('celery purge -f')

    if demo:
        populate(ctx)


@task
def server(ctx):
    """ Run the debugging webserver"""
    ctx.run('python manage.py runserver', pty=True)


@task
def celery(ctx, worker=1):
    """ Run the background worker"""
    ctx.run('python manage.py celery worker -E --loglevel=INFO --concurrency={0}'.format(worker), pty=True)


@task
def flower(ctx):
    """ Run the monitor for the message queue"""
    ctx.run('celery flower', pty=True)


@task
def static(ctx):
    """ Install static files"""
    ctx.run('python manage.py collectstatic --clear --noinput')
    ctx.run('python manage.py collectstatic --noinput')