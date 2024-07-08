"""
This is the entrypoint for your service. Not a lot will live here other than
starting the application as well as a minimal HTTP server to provide a health
status endpoint.
"""

from threading import Thread

from service import config, logger
from service.app import App
from service.health import HealthServer


def main():
    # Start app on thread
    app = App()
    enrich_thread = Thread(name="enrich_thread", target=app.start)
    enrich_thread.start()

    # Start basic http server for health check on another thread
    health_server = HealthServer(app)
    health_thread = Thread(name="health_thread", target=health_server.start)
    health_thread.start()

    logger.info(f"Service '{config.application_name}' ready.")


if __name__ == "__main__":
    main()
