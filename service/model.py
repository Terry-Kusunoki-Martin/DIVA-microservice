"""
This is where any data models you need should be defined. At a minimum, a
Request and Response class should be defined. Do not change the name of these
classes.

Received information should be propagated, never destroyed.
"""

from pydantic import BaseModel


class Request(BaseModel):
    baggage: dict = {}
    original_content: str


class Response(Request):
    appended_text: str
