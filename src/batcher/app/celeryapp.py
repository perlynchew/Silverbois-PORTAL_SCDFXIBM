from __future__ import absolute_import
from celery import Celery
from celery import bootsteps
from kombu import Consumer, Exchange, Queue, Connection
from kombu.serialization import registry
import json

# accept plain text content type
CELERY_ACCEPT_CONTENT = ['text/plain']
registry.enable('text/plain')

my_queue = Queue('scdf', Exchange('scdf'), 'routing_key')

BROKER_URL='amqp://guest:guest@rabbitmq/scdf-vhost'
result_backend ='db+postgres://postgres:password@postgres'

app = Celery(broker=BROKER_URL,backend=result_backend,include=['task'])

# If True the task will report its status as “started” when the task is executed by a worker. 
# the following allows status of task to be tracked when it has started, not just succeeded
# diabled as it may cause bugs in postgres due to excessive inserting and updating of result table
app.conf.task_track_started = False

# building a custom message consumer to convert postgres-rabbitmq messages to a format that celery understands

class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[my_queue],
                         callbacks=[self.handle_message],
                         accept=['text/plain'])]

# converting messages received to celery tasks
    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        messagedict = json.loads(body)
        with Connection(BROKER_URL) as conn:
            queue = conn.SimpleQueue('celery')
            exit = False
            # add tasks with args here
            if messagedict.get("event") == "fire":
                args = [messagedict.get("event_id"), messagedict.get("location"), messagedict.get("description")]
            elif messagedict.get("event") == "EMS":
                args = [messagedict.get("event_id"), messagedict.get("location"), messagedict.get("description")]
            # if unknown task is received
            else:
                print('Error Occured: Unknown task')
                message.ack()
                exit = True
            if not exit:
                createTask = {
                    "id": str(messagedict.get("event_id")),
                    "args": args,
                    "task": f'task.{messagedict.get("event")}'
                             }
                queue.put(createTask)
                queue.close()
                message.ack()

app.steps['consumer'].add(MyConsumerStep)
