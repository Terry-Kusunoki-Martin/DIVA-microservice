"""
You should not need to edit this file. It houses the code to serve the health
status endpoint which only interacts with app.py via a shared variable.
"""

import json
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer

from loguru import logger

from service.app import App


class QuietHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Wrapper class to prevent logging requests. Docker will periodically trigger
    GET requests to check the health status.
    """

    def log_message(self, format, *args):
        return


class HealthHandler(QuietHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.enrichment_app = kwargs.pop("enrichment_app")
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # TODO: do we want to parse self.path?
        logger.debug(self.enrichment_app.running)
        status = "UP" if self.enrichment_app.running else "DOWN"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({"status": status}), "utf-8"))


class HealthServer:
    def __init__(self, enrichment_app: App, server_port: int = 8080, server_host: str = "0.0.0.0"):
        logger.info(f"Starting {self.__class__.__name__}")
        self.server_port = server_port
        self.server_host = server_host
        self.health_handler = partial(HealthHandler, enrichment_app=enrichment_app)

    def start(self):
        httpd = HTTPServer((self.server_host, self.server_port), self.health_handler)
        httpd.serve_forever()
