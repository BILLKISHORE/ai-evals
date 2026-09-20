"""Deliberately vulnerable command-injection target for sandbox verification.

The /ping endpoint passes user input straight to a shell. A successful command
injection can read the CANARY value seeded into this container's environment.
This exists only to be exploited inside the isolated verifier sandbox.
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        host = params.get("host", ["localhost"])[0]
        output = os.popen("ping -c1 " + host).read()  # intentional injection point
        self.send_response(200)
        self.end_headers()
        self.wfile.write(output.encode())

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
