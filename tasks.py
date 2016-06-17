from invoke import task

@task
def celery(ctx, worker=1):
    ctx.run('python manage.py celery worker -E --loglevel=INFO --concurrency={0}'.format(worker))

@task
def flower(ctx):
    ctx.run('celery flower')

@task
def venv(ctx):
    ctx.run('virtualenv --python=python3 .venv')

@task
def deps(ctx):
    ctx.run('pip install --upgrade pip wheel distribute')
    ctx.run('pip install --upgrade -r requirements.txt -r requirements_dev.txt')

    try:
        import sherlock
    except ImportError:
        ctx.run('cd PlagCheck/hashing/sherlock && python setup.py install')

@task
def clean(ctx, plagcheck=False, migrate=True, demo=True):
    """
    Wipe databases and recreate them with following options.

    :param plagcheck: Wipe also plagcheck database (default=False)
    :param demo: Populate demo data (default=True)
    :param migrate: Do also migrations (default=False)
    """
    ctx.run('rm -f database.db')
    ctx.run('python manage.py migrate')

    if plagcheck:
        ctx.run('rm -f database-plagcheck.db')
        ctx.run('python manage.py migrate --database=plagcheck --noinput')
        ctx.run('celery purge -f')

    if demo:
        ctx.run('python manage.py populate_demo_data')

    ctx.run('python manage.py collectstatic --clear --noinput')
    ctx.run('python manage.py collectstatic --noinput')