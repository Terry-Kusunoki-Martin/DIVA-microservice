"""
This is where you will implement the logic to manage and process data through
your model or algorithm. Most of your development time will likely be spent in
this file. __All__ data preprocessing, model/algorithm processing, and output
postprocessing should be contained in this file. There should be no reference
to packages such as TensorFlow, PyTorch, OpenCV outside of this file.
"""


from typing import Generator

from pydantic import validate_call

from service.model import Request, Response


class Enricher:
    def __init__(self):
        pass

    @validate_call
    def __call__(self, requests) -> Generator[Response, None, None]:
        for r in requests:
            yield Response(
                baggage=r.baggage,
                original_content=r.original_content,
                appended_text=f"{r.original_content} goodbye",
            )
