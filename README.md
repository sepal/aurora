# Aurora

next generation of the portfolio

## Getting started

- Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)
- Clone the project `git clone git@github.com:martflu/aurora.git`
- cd to your project folder `cd aurora`
- start the vagrant box `vagrant up` (this will take quite a while and download a lot of data)
- ssh to it `vagrant ssh`
- you should now be in the project folder with active virtualenv:

  `(py3env)vagrant@vagrant-ubuntu-trusty-64:/vagrant$`

- you'll need a `local_settings.py` overwriting some settings from `AuroraProject/config.py` with your local needs.
  or copy the demo settings: `cp local_settings.example.py local_settings.py`

- and you'll need an extra config for the `Slides` app: `Slides/settings.py` with two parameters set. Quickstarters
  can use the example: `cp Slides/settings.example.py Slides/settings.py`

- create the database schema `python manage.py migrate`
- collect all static files in one place `python manage.py collectstatic`
- populate the database with some test data `python manage.py populate_demo_data`
- start the dev server `python manage.py runserver 0.0.0.0:8000`
- go to `http://localhost:8000` in your browser

    Dev users (password is same as username):
    students: s[0-49]
    dummy user: d[0-3]
    tutors: t[0-4]
    admin: amanaman
    staff: hagrid

    (from `AuroraUser/management/commands/populate_demo_data.py`)

- have fun hacking!

p.s. we use [PyCharm](https://www.jetbrains.com/pycharm/) for development. They provide free educational licences for owners of university email addresses.

### running aurora on your host machine

If you use pyCharm, pyCharm automatically installs the python requirements from `requirements.txt`. But actually
`requirements.txt` contains production python packages including postgres modules. There is a `requirements_dev.txt`
for development purposes, which you would have to set manually.
See the settings at `File | Settings | Tools | Python Integrated Tools`

- system requirements: python3, gcc or xcode and python3 headers.
- python requirements: pip, virtualenv, invoke
- Create a virtualenv:
  - Fastest way:  `invoke virtualenv && source .venv/bin/activate`
  - Either via pyCharm `File | Settings | Project (aurora) | Project interpreter` `Create VirtualEnv` (Be sure to select python3)
  - Or via command line: `virtualenv --python python3 .venv`
  - PyCharm: Select the created virtual environment for the django run configuration. Makes it possible to run the server from within pyCharm with the
play button.
- Install project dependencies: `invoke deps`
- Setup databases: `invoke clean -p`
- Run celery: `invoke celery`
- Run server: `python manage.py runserver`

