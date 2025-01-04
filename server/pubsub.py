from google.cloud import pubsub_v1
import os

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID")

publisher = pubsub_v1.PublisherClient()

def publish_message(message: str):
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    publisher.publish(topic_path, message.encode("utf-8"))
