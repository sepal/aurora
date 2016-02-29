# plagcheck

Plagiarism detection system

## Installation

Be sure to have the requirements from requirements_dev.txt file installed.

The worker needs to include the sherlock module, which is a external C module inside the a package. In order to use it
run its installation script in the workers python environment.

    cd Plagcheck/hashing/sherlock
    python setup.py install

For the monitor to work you need to run the RabbitMQ message queue server and set USE_DJANGO_BROKER to False. Otherwise
it should also work with djangos internal database and set USE_DJANGO_BROKER to True.

## Usage

### Worker process

    celery -A Plagcheck worker --concurrency=1 --loglevel=DEBUG

Only one worker can run at the same time, because:
 - sherlock is not yet multi-thread ready
 - database queries need to be synchronized

### Task monitor

    celery -A Plagcheck flower --loglevel=DEBUG

It will then be available at http://localhost:5555

Now each elaboration save operation should trigger a plagiarism check on the worker. On the monitor website you can see
when the worker finishes. The results are displayed on the monitor and within auroras admin page.
 
### In case you need to purge a RabbitMQ queue:

    rabbitmqctl purge_queue celery

If this doesn't work for you, you can use amqp-tools from your package repository:

    amqp-delete-queue -q celery


### Importing elaborations from a csv file

    python manage.py plagcheck_csv_elaboration_import ELABORATION_CSV_FILE [START_LINE #]

Import all elaborations from ELABORATION_CSV_FILE starting at START_LINE. START_LINE is useful
when aborting the import and continue with the import at the specified line. START_LINE defaults to 0.

### Cleaning all elaborations, references, results and suspects except the filtered

This is useful to test a big dataset. Import the csv dataset once, then create filters,
call this clean script and import the csv dataset again. This way filters will be applied to all
newly imported elaborations, instead of filtering just new elaborations when the filter has been added.

    python manage.py plagcheck_clear_but_filtered