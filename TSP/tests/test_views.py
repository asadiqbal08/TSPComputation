"""Google pub/sub unittest"""
import os
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from dotenv import load_dotenv
from google.cloud import pubsub_v1
from urllib.parse import urlencode
from django.contrib.messages import get_messages

from ..constants import locations_msg, vehicle_msg

load_dotenv()

PROJECT = os.getenv('PUB_SUB_PROJECT')
TOPIC = os.getenv('PUB_SUB_TOPIC')

assert PROJECT is not None
assert TOPIC is not None


class TestPublishingJob(TestCase):
    """
    Tests for publishing user input long-lat locations to google pub/sub topic queue.
    """

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.publisher_client = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher_client.topic_path(PROJECT, TOPIC)

    def test_form_coordinates_not_valid(self):
        """test_form_coordinates_not_valid"""
        # Publish the message
        coordinates = '[[20, 10 ], [100, 240], [120, 210]]'
        data = urlencode({"coordinates": coordinates, "no_of_vehicle": "1"})
        response = self.client.post(reverse('publish'), data, content_type="application/x-www-form-urlencoded")
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(len(messages), 1)
        self.assertEqual(locations_msg, messages[0]['coordinates'][0])

    def test_form_vehicle_input_not_valid(self):
        """test_form_vehicle_input_not_valid"""
        # Publish the message
        coordinates = '[20, 10 ], [100, 240], [120, 210]'
        data = urlencode({"coordinates": coordinates, "no_of_vehicle": "xyz"})
        response = self.client.post(reverse('publish'), data, content_type="application/x-www-form-urlencoded")
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(len(messages), 1)
        self.assertEqual(vehicle_msg, messages[0]['no_of_vehicle'][0])

    def test_success_message(self):
        """test_success_message"""
        # Publish the message
        coordinates = '[20, 10 ], [100, 240], [120, 210]'
        data = urlencode({"coordinates": coordinates, "no_of_vehicle": "1"})
        response = self.client.post(reverse('publish'), data, content_type="application/x-www-form-urlencoded")
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(len(messages), 1)
        self.assertIn('Request is published successfully.', messages)

    def test_data_pubish_logs(self):
        """test_data_pubish_logs"""
        # Publish the message
        coordinates = '[20, 10 ], [100, 240], [120, 210]'
        data = urlencode({"coordinates": coordinates, "no_of_vehicle": "1"})
        
        with self.assertLogs(logger='TSP.views', level='INFO') as cm:
            self.client.post(reverse('publish'), data, content_type="application/x-www-form-urlencoded")
            self.assertIn(
                "INFO:TSP.views:Pushing payload to google pub/sub topic queue.",
                cm.output
            )
    
    #### NOTE FOR REVIEWER ###
    #### NOTE FOR REVIEWER ###
    #### FURTHER TESTS CAN BE ADDED IN ORDER TO TEST GOOGLE PUBLISHER LOGS FOR THE INPUT DATA
