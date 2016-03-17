from invoke import run, task

@task
def create_plagcheck_db():
    run('python manage.py syncdb --database=plagcheck')

@task
def celery():
    run('python manage.py celery worker -E --loglevel=INFO --concurrency=1')

@task
def venv():
    run('virtualenv --python=python3.4 .venv')

@task
def deps():
    run('pip install -r requirements.txt requirements_dev.txt')

@task
def clean():
    run('rm -f database.db')
    run('rm -f plagcheck-database.db')

@task
def install():
    run('cd PlagCheck/hashing/sherlock && python setup.py install')
    run('pip install --upgrade pip')
    run('python manage.py syncdb --noinput')