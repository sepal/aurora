# plagcheck

Plagiarism detection daemon

## Installation

Be sure to have the requirements from requirements_dev.txt file installed.

The worker needs to include the sherlock module, which is a external C module inside the a package. In order to use it
run its installation script in the workers python environment.

    cd Plagcheck/hashing/sherlock
    python setup.py install

For the monitor to work you need to run the RabbitMQ message queue server and set USE_DJANGO_BROKER to False. Otherwise
it should also work with djangos internal database and set USE_DJANGO_BROKER to True.

## Usage

Start the worker

    celery -A Plagcheck worker --concurrency=1 --loglevel=DEBUG

Only one worker can run at the same time, because:
 - sherlock is not yet multi-thread ready
 - database queries need to be synchronized

Run the flower monitor:

    celery -A Plagcheck flower --loglevel=DEBUG

It will then be available at http://localhost:5555

Now each elaboration save operation should trigger a plagiarism check on the worker. On the monitor website you can see
when the worker finishes. The results are displayed on the monitor and within auroras admin page.
 
In case you need to purge a RabbitMQ queue:

    rabbitmqctl purge_queue celery
