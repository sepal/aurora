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

## Installation

The following steps need to run all in the same python environment (virtualenv).

### Database

Since we produce quite much data, this system is hardly depending on the performance of the database. Therefore
everything read or written for the plagcheck tasks, is separated from the main database. (Not on a debugging system
 if performance is not required).

The plagcheck database stores the hashes, results of the checks, found suspicions and document metadata. You need this
data to check against already hashed documents. This means that if you're going to create a fresh installation of
Aurora and want the new documents checked against old ones, you need to keep the old plagcheck database for the
new installation.
If you don't want the database to grow infinitely, you could delete entries older than e.g. 5 years.

To prepare the separate database run the following:

    python manage.py migrate --database=plagcheck

There is a bug which produces new migrations even thou no new migrations are in place.

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

    celery -A AuroraProject worker -l info -E --loglevel=INFO --concurrency=1

Only one worker can run at the same time, because:
 - sherlock is not yet multi-thread ready
 - database queries need to be synchronized

### Task monitor

    celery -A PlagCheck flower

For the monitor to work you need to run the RabbitMQ message queue server
and set USE_DJANGO_BROKER to False. Otherwise
it should also work with Djangos internal database and set USE_DJANGO_BROKER to True.


### Management tasks

PlagCheck offers some scripts to handle different reoccurring tasks. Those programs are accessible via the Django
management command interface, which is simply:

    # python manage.py plagcheck_{COMMAND}
    # e.g.:
    python manage.py plagcheck_check_unverified

Each command has its own help text included. Just call the command with the help parameter to get to know what the
 command actually does:

    # python manage.py plagcheck_{COMMAND} -h
    # e.g.:
    python manage.py plagcheck_csv_elaboration_import -h

Since the help text is inside the code, it is not vise to list and describe them here. But you can use your consoles
auto-completion functionality to find commands starting with 'plagcheck_'.

### Was the installation successful?

In order to check your PlagCheck installation you can do the following:
  
First run the unit tests, to see if Sherlock is installed properly:

    python manage.py test PlagCheck

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