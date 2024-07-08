"""
This is where the Kafka logic is implemented and where the Enricher is called.
You shouldn't need to change much, if anything, here.
"""

import json
from json import JSONDecodeError

from confluent_kafka import (
    Consumer,
    KafkaError,
    Message,
    Producer,
    TopicPartition,
    admin,
)
from confluent_kafka.admin import KafkaException
from pydantic import ValidationError as PydanticValidationError

from service import config, logger
from service.config import AppConfig
from service.enrich import Enricher
from service.model import Request

kadmin = admin.AdminClient({"bootstrap.servers": config.bootstrap_servers})
topics = config.consumer_topics + "," + config.producer_topic
kadmin.create_topics([admin.NewTopic(topic) for topic in topics.split(",")])


class App:
    _config: AppConfig = config

    def __init__(self):
        logger.debug(f"Config = {self._config}")
        self.running = False
        self.enricher = Enricher()
        # A complete list of configuration options can be found here:
        # https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#kafka-client-configuration
        kafka_config = {
            "bootstrap.servers": self._config.bootstrap_servers,
            "group.id": self._config.group_id,
            "error_cb": self._error_callback,
            "auto.offset.reset": "earliest",
            # "logger": logger  # creating double logs
        }
        self.consumer = Consumer(kafka_config, on_commit=self._commit_callback)
        del kafka_config["group.id"]
        del kafka_config["auto.offset.reset"]
        self.producer = Producer(kafka_config, on_delivery=self._delivery_callback)
        self.max_batch_size = config.max_batch_size
        self.max_batch_ms = config.max_batch_ms

    def _error_callback(self, err: Exception):
        logger.error(f"Callback exception: {err}")
        self.shutdown()

    def _delivery_callback(self, err: KafkaError, msg: Message):
        logger.debug("Delivered Kafka message")

    def _commit_callback(self, err: KafkaError, part: list[TopicPartition]):
        if err is not None:
            logger.error("Failed to commit offset")
        logger.debug(f"Committing partitions: {part}")

    def start(self):
        self.running = True
        try:
            logger.debug(f"Consumer topics: {self._config.consumer_topics}")
            self.consumer.subscribe(self._config.consumer_topics.split(","))

            while self.running:
                _msgs = []
                if msgs := self.consumer.consume(
                    num_messages=self._config.max_batch_size, timeout=self._config.consumer_timeout
                ):
                    logger.info(f"Processing {len(msgs)} messages")

                    self.consumer.commit(asynchronous=True)

                    for msg in msgs:
                        if msg.error():
                            # A complete list of KafkaErrors can be found here:
                            # https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#kafkaerror
                            logger.error(f"Kafka error encountered: {msg.error()}")
                            if msg.error().code() == KafkaError._PARTITION_EOF:
                                logger.error(
                                    f"{msg.topic()} [{msg.partition()}] reached end of offset {msg.offset()}"
                                )
                            elif msg.error():
                                # Stop the service, depend on Docker to restart it
                                raise KafkaException(msg.error())

                            # Don't process this message
                            # TODO: handle this better. Maybe return an empty response?
                            continue
                        else:
                            _msgs.append(msg)

                    self.handle_batch(_msgs)
        finally:
            logger.critical("Fatal error encountered. Shutting down.")
            self.shutdown()

    def handle_batch(self, batch: list[Message]):
        requests = [self.handle_message(m) for m in batch]
        non_empty_requests: list[Request] = [r for r in requests if r is not None]

        try:
            for response in self.enricher(non_empty_requests):
                logger.debug(f"Topic = {self._config.producer_topic}")
                logger.debug(f"Producer response: {response.model_dump_json()}")
                self.producer.produce(self._config.producer_topic, value=response.model_dump_json())
        except PydanticValidationError:
            logger.error(f"Failed to validate messages: {non_empty_requests}")
            return
        except FileNotFoundError as e:
            logger.error("File not found", e)
        except Exception as e:
            logger.error("Failed to process request", e)

    def handle_message(self, msg: Message) -> Request | None:
        try:
            if payload := json.loads(msg.value()):
                return payload
            else:
                logger.error("Failed to parse message")
        except JSONDecodeError:
            logger.error(f"Failed to parse JSON message: {msg.value()}")
        except Exception:
            logger.error("Failed to parse message")

    def shutdown(self):
        logger.error("Shutting down")
        self.running = False
        self.consumer.close()
