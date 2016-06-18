# PlagCheck

Plagiarism detection system

## Installation

The following steps need to run all in the same python virtualenv environment. 

### Requirements

Be sure to have the requirements from requirements_dev.txt file installed.

Either run the vagrant provisioning again, or issue the following:

    pip install -r requirements.txt
    
or this one if you are in a development environment:

    pip install -r requirements_dev.txt

### Sherlock

The worker needs to include the sherlock module, which is a external C 
module inside the a package. In order to use it
run its installation script in the workers python environment.

    cd Plagcheck/hashing/sherlock
    python setup.py install

For the monitor to work you need to run the RabbitMQ message queue server 
and set USE_DJANGO_BROKER to False. Otherwise
it should also work with djangos internal database and set USE_DJANGO_BROKER to True.

### RabbitMQ message queue

Install the RabbitMQ message queue from your package repository.

For Ubuntu installations (vagrant virtual machine):

    sudo apt-get update
    sudo apt-get install rabbitmq-server
     
For MAC:

    brew update
    brew install rabbitmq

## Usage

Run all of these commands under your repository root, where all the
django apps are listed.

### Worker process

    python manage.py celery worker -E --loglevel=INFO --concurrency=1

Only one worker can run at the same time, because:
 - sherlock is not yet multi-thread ready
 - database queries need to be synchronized

### Task monitor

    celery -A PlagCheck flower

It will then be available at http://localhost:5555

Now each elaboration save operation should trigger a plagiarism check on 
the worker. On the monitor website you can see when the worker finishes.
The results are displayed on the monitor and within auroras admin page.

### Was the installation successful?

In order to check your PlagCheck installation you can do the following:
  
First run the unit tests, to see if Sherlock is installed properly:

    python manage.py test PlagCheck
     
Then you could wipe your current database and start from scratch:

    rm -f database.db&& python manage.py syncdb --noinput && python manage.py populate_demo_data
 
### In case you need to purge a RabbitMQ queue:

    rabbitmqctl purge_queue celery

If this doesn't work for you, you can use amqp-tools from your package repository:

    celery purge

### Importing elaborations from a csv file

    python manage.py plagcheck_csv_elaboration_import ELABORATION_CSV_FILE [START_LINE #]

Import all elaborations from ELABORATION_CSV_FILE starting at START_LINE.
START_LINE is useful when aborting the import and continue with the 
import at the specified line. START_LINE defaults to 0.

### Cleaning all elaborations, references, results and suspicions except the filtered

This is useful to test a big dataset. Import the csv dataset once, then create filters,
call this clean script and import the csv dataset again. This way filters will be applied to all
newly imported elaborations, instead of filtering just new elaborations when the filter has been added.

    python manage.py plagcheck_clear_but_filtered