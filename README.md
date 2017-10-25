# Aurora

## Getting started

- Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)
- Install [vagrant-vbguest](https://github.com/dotless-de/vagrant-vbguest) `vagrant plugin install vagrant-vbguest`
- Clone the project `git clone git@github.com:martflu/aurora.git`
- cd to your project folder `cd aurora`
- start the vagrant box `vagrant up` (this will take quite a while and download a lot of data)
- ssh to it `vagrant ssh`
- you should now be in the project folder with active virtualenv:

  `(py3env)vagrant@vagrant-ubuntu-trusty-64:/vagrant$`

- create the database schema `python manage.py migrate`
- collect all static files in one place `python manage.py collectstatic`
- populate the database with some test data `python manage.py populate_demo_data`
- populate the database with some test slides `python manage.py populate_demo_slides`

- install PlagCheck 
    `cd Plagcheck/hashing/sherlock`
    `python setup.py install`
    
- return to base directory `cd ../../../`
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
