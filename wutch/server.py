from http.server import ThreadingHTTPServer
from http.server import BaseHTTPRequestHandler
import threading

from loguru import logger

from .events import Event


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        claimed = self.server.dispatcher.claim(Event.JSInjectFinished)
        status = "changed" if claimed else "unchanged"

        reply = { "status": status }
        logger.debug(f"Serving GET request: {reply}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(f"{reply}".encode("utf-8"))

        return


class Server:
    def __init__(self, config, dispatcher) -> None:

        self.config = config
        self.dispatcher = dispatcher
        self.server = ThreadingHTTPServer(
            (config.host, config.port), RequestHandler
        )
        setattr(self.server, "dispatcher", dispatcher)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    def start(self):

        self.thread.start()
        logger.debug("Server started")

    def stop(self):

        self.server.shutdown()
        logger.debug("Server shutdown")
