# PlagCheck

Plagiarism detection system

## How it works

When someone submits a document, a background task runs and divides the document in small pieces and generates
hashes out of it. After storing the hashes and metadata of the suspected document in the database, it starts
comparing its hashes with the hashes of all other documents in the database. Whenever the hashes match with another
documents hashes to a specific amount, then a suspicion report is generated and stored in the database.

Sherlock is the hashing algorithm itself. It is taken from http://www.cs.usyd.edu.au/~scilect/sherlock/ and
adapted to compile as a Python wrapped C library.

We use celery as our background task processor. Flower is a monitor, to watch the status of ongoing celery
 hashing tasks.

To let the Aurora frontend communicate to the background task processor a RabbitMQ message queue is used.

Since we produce quite much data, this system is hardly depending on the performance of the database. Therefor
everything read or written for the plagcheck tasks, is separated from the main database. (Not on a debugging system
 if performance is not required)

## Installation

The following steps need to run all in the same python environment (virtualenv).

### Sherlock

The worker needs to include the sherlock module, which is a external C 
module inside the package, which needs to be compiled first. In order to use it
run its installation script in the workers python environment.

    cd Plagcheck/hashing/sherlock
    python setup.py install

### RabbitMQ message queue

Install the RabbitMQ message queue from your package repository.

For Ubuntu installations (vagrant virtual machine):

    sudo apt-get update
    sudo apt-get install rabbitmq-server
     
For MAC:

    brew update
    brew install rabbitmq

## Usage

If everything is setup, you just need to start the task processor beside the Aurora webserver

    python manage.py celery worker -E --loglevel=INFO --concurrency=1

Only one worker can run at the same time, because:
 - sherlock is not yet multi-thread ready
 - database queries need to be synchronized

### Task monitor

    celery -A PlagCheck flower

For the monitor to work you need to run the RabbitMQ message queue server
and set USE_DJANGO_BROKER to False. Otherwise
it should also work with djangos internal database and set USE_DJANGO_BROKER to True.

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