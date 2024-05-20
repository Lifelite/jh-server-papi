import functools
import json
import os
import uuid

from dotenv import load_dotenv
from kafka import KafkaProducer, KafkaConsumer

load_dotenv()

KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")


class KafkaEventPublisher(KafkaProducer):

    def __init__(self):
        super().__init__(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)

    def produce(self, topic, data):
        if self.bootstrap_connected():
            key = str(uuid.uuid4())
            key = bytes(key, 'utf-8')
            data = bytes(json.dumps(data), "utf-8")
            future = self.send(topic, key=key, value=data)
            result = future.get(timeout=60)
            if result:
                print(f"Kafka producer successfully posted to {topic}, Result: {result}")
                return True
            else:
                print(f"Kafka producer failed to post to {topic} topic: {data},\n Result: {result}")
                return False
        else:
            print("Unable to connect to kafka bootstrap server")
            return False

    def produce_to_postres_topic(self, data):
        return self.produce('postgres', data)

    def jh_com_post_contact_me(self, body):
        print(body)
        parsed = json.loads(body)
        parsed["provider"] = "contact-me"
        parsed = json.dumps(parsed)
        return self.produce_to_postres_topic(parsed)


class KafkaEventSubscriber(KafkaConsumer):
    def __init__(self, *topics, **configs):
        super().__init__(*topics, **configs)
