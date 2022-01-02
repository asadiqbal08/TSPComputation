import logging
import os
import sys
import json
from django.conf import settings
from google.cloud import pubsub_v1

module_path = os.path.abspath(os.getcwd() + '/subscriber/')
if module_path not in sys.path:
    sys.path.append(module_path)

from route_calculation import calculate_shortest_distance

logger = logging.getLogger(__name__)

project_id = settings.PUB_SUB_PROJECT
subscription_id = settings.PUB_SUB_SUBSCRIPTION

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    routes = {}
    try:
        routes = calculate_shortest_distance(eval(message.data))
    except Exception as err:
        logger.error(f"Failed: <calculate_shortest_distance> with error : {err}")
    
    print('------------------START---------------')
    #Display the routes.
    for key, route in enumerate(routes):
        print('Route for vehicle {0}: {1}'.format(key, list(route.values())[0]))
    print('------------------END------------------')
    message.ack()

# Limit the subscriber to only have ten outstanding messages at a time.
flow_control = pubsub_v1.types.FlowControl(max_messages=10)

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback, flow_control=flow_control
)

logger.info(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result()
    except Exception as e:
        logger.error(f"Error occured while pulling data by subscriber: {e}")
        print(
            f"Listening for messages on {subscription_path} threw an exception: {e}."
        )
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
