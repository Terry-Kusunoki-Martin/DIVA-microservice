import os

import pytest

# This needs to be set before the config is loaded
os.environ["DEBUG_ENABLED"] = "True"

from service.enrich import Enricher  # noqa: E402
from service.model import Request  # noqa: E402


@pytest.fixture
def enricher():
    return Enricher()


class TestEnricher:
    def test_normal_text(self, enricher: Enricher):
        request = Request(original_content="text")
        for response in enricher([request]):
            assert response.appended_text == "text goodbye"

    def test_empty_text(self, enricher: Enricher):
        request = Request(original_content="")
        for response in enricher([request]):
            assert response.appended_text == " goodbye"
