import json

import pytest
from confluent_kafka import Consumer, Producer
from loguru import logger


class Config:
    kafka_uri: str = "kafka:9092"
    consumer_topics: list[str] = ["appended.text.naive"]
    producer_topic: str = "unappended.text.naive"
    group_id: str = "append-text"


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def consumer(config: Config):
    consumer = Consumer(
        {
            "bootstrap.servers": config.kafka_uri,
            "group.id": config.group_id,
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe(config.consumer_topics)
    return consumer


class TestService:
    def test_regular_message(self, config: Config, consumer: Consumer):
        msg = {"baggage": {}, "original_content": "hello"}
        producer = Producer({"bootstrap.servers": config.kafka_uri})
        producer.produce(config.producer_topic, value=json.dumps(msg))
        producer.flush(5)

        if app_msg := consumer.poll(timeout=60):
            if msg_val := json.loads(app_msg.value()):
                logger.info(f"Received message: {msg_val}")
                assert msg_val.get("appended_text") == "hello goodbye"
                return

        pytest.fail("Did not receive response from service.")
