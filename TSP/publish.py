"""" publisher module """
import json
import os
import logging
from django.conf import settings
from google.cloud import pubsub_v1
from concurrent import futures
from typing import Callable
from .utils import compute_euclidean_distance_matrix

from google.cloud import storage
from google.oauth2 import service_account

# THE FILE "tspcomputation.json" SHOULD NOT BE THE PART OF CODE REPOSITORY FOR PRIVACY CONCERNS. 
# ADDING AT THE MOMENT FOR THIS ASSIGNMENT
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS


project_id = settings.PUB_SUB_PROJECT
topic_id = settings.PUB_SUB_TOPIC
api_keys = settings.API_KEYS
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

publish_futures = []

log = logging.getLogger(__name__)

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        """
        Callback to get message id after publishing job.
        """
        try:
            # Wait 60 seconds for the publish call to succeed.
            message_id = publish_future.result(timeout=60)
            log.info(f'Data is published successfully with ID: {message_id} ')
        except futures.TimeoutError:
            log.error(f"Publishing {data} timed out.")
        
    return callback

def push_payload(no_of_vehicle, coordinates):
    """
    publish data to google pub/sub topic queue.
    """
    payload = {
        'distance_matrix': compute_euclidean_distance_matrix(coordinates).tolist(),
        'num_vehicles': no_of_vehicle,
        'depot': 0
    }
    publisher = pubsub_v1.PublisherClient()
    data = json.dumps(payload).encode("utf-8")

    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data, coordinates=json.dumps(coordinates).encode('utf-8'))
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, coordinates))
    publish_futures.append(publish_future)
