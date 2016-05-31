from invoke import run, task, exceptions

@task
def create_plagcheck_db():
    run('python manage.py syncdb --database=plagcheck --noinput')

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
    run('pip install --upgrade pip')
    run('pip install --upgrade -r requirements.txt -r requirements_dev.txt')

    try:
        import sherlock
    except ImportError:
        run('cd PlagCheck/hashing/sherlock && python setup.py install')

@task
def clean(plagcheck=False, migrate=False, demo=True):
    """
    Wipe databases and recreate them with following options.

    :param plagcheck: Wipe also plagcheck database (default=False)
    :param demo: Populate demo data (default=True)
    :param migrate: Do also migrations (default=False)
    """
    run('rm -f database.db')

    result = run('python manage.py syncdb --noinput')
    if result.return_code is not 0:
        raise exceptions.Failure(result)

    if plagcheck:
        run('rm -f database-plagcheck.db')
        create_plagcheck_db()

    if migrate:
        run('python manage.py makemigrations')
        run('python manage.py migrate')

    if demo:
        run('python manage.py populate_demo_data')