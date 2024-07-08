"""
Any application configuration should be ingested and housed within this file.
During application start, this will be the first code executed via __init__.py.
"""
from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    debug_enabled: bool = Field(default=False)
    application_name: str = Field(default="append-text-naive")
    log_dir: str = Field(default="/var/log")
    bootstrap_servers: str = Field(alias="kafka_bootstrap_servers", default="kafka:9092")
    consumer_topics: str = Field(alias="kafka_consumer_topics", default="unappended.text.naive")
    group_id: str = Field(alias="kafka_group_id", default="append-text")
    producer_topic: str = Field(alias="kafka_producer_topic", default="appended.text.naive")
    consumer_timeout: float = Field(alias="kafka_consumer_timeout", default=1)
    resources_dir: str = Field(default="resources")
    max_batch_size: int = Field(default=1)
    max_batch_ms: float = Field(default=1)
