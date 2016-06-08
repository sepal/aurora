from invoke import run, task, exceptions

@task
def celery():
    run('python manage.py celery worker -E --loglevel=INFO --concurrency=1')

@task
def flower():
    run('celery -A PlagCheck flower')

@task
def venv():
    run('virtualenv --python=python3 .venv')

@task
def deps():
    run('pip install --upgrade pip wheel distribute')
    run('pip install --upgrade -r requirements.txt -r requirements_dev.txt')

    try:
        import sherlock
    except ImportError:
        run('cd PlagCheck/hashing/sherlock && python setup.py install')

@task
def clean(plagcheck=False, migrate=True, demo=True):
    """
    Wipe databases and recreate them with following options.

    :param plagcheck: Wipe also plagcheck database (default=False)
    :param demo: Populate demo data (default=True)
    :param migrate: Do also migrations (default=False)
    """
    run('rm -f database.db')

    if plagcheck:
        run('rm -f database-plagcheck.db')
        run('python manage.py migrate --database=plagcheck --noinput')

    run('python manage.py migrate')

    if demo:
        run('python manage.py populate_demo_data')

    run('python manage.py collectstatic --clear --noinput')
    run('python manage.py collectstatic --noinput')