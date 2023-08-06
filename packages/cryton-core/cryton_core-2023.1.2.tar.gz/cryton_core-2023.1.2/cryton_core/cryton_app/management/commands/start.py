from threading import Thread
from django.core.management.base import BaseCommand
from click import echo

from cryton_core.asgi import application
from cryton_core.lib.services.gunicorn import GunicornApplication
from cryton_core.lib.services.listener import Listener
from cryton_core.lib.util.logger import logger_object


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--bind", type=str, help="ADDRESS:PORT to serve the server at.")
        parser.add_argument("--workers", type=int, help="The NUMBER of worker processes for handling requests.")

    def handle(self, *args, **options):
        """
        Starts logger processor, listener, and gunicorn app.
        :param args: Arguments passed to the handle
        :param options: Options passed to the handle
        :return: None
        """
        hard_options = {
            "bind": options.get("bind", "0.0.0.0:8000"),
            "worker_class": "uvicorn.workers.UvicornWorker",
            "workers": options.get("workers", 2)
        }

        echo("Set up... ", nl=False)
        gunicorn_app = GunicornApplication(application, hard_options)
        listener = Listener()

        # Start log_handler in a thread to ensure the logs from multiprocessing aren't missing
        logger_processor_thread = Thread(target=logger_object.log_handler)
        logger_processor_thread.start()
        echo("OK")

        try:
            echo("Starting RabbitMQ listener... ", nl=False)
            listener.begin()
            echo("OK")
            gunicorn_app.run()
        finally:
            echo("Stopping REST API... OK")  # Gunicorn doesn't have user-friendly output
            echo("Stopping RabbitMQ listener... ", nl=False)
            listener.stop()
            echo("OK")

            echo("Cleaning up... ", nl=False)
            logger_object.log_queue.put(None)  # Ensure the log_handler will stop
            echo("OK")
