from invoke import run, task

@task
def create_plagcheck_db():
    run('python manage.py syncdb --database=plagcheck')

@task
def celery():
    run('python manage.py celery worker -E --loglevel=INFO --concurrency=1')

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
def clean():
    run('rm -f database.db')
    run('rm -f plagcheck-database.db')
    run('python manage.py syncdb --noinput')
    run('python manage.py populate_demo_data')
    #create_plagcheck_db()