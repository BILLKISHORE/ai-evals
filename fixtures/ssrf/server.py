"""Deliberately vulnerable SSRF target for sandbox verification.

The public /fetch endpoint retrieves any URL it is given, with no allowlist. A
metadata sidecar bound to loopback returns the CANARY and is reachable only
from inside this container, so only a successful SSRF can read it. This exists
only to be exploited inside the isolated verifier sandbox.
"""
import os
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

METADATA_PORT = 9000


class Metadata(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(os.environ.get("CANARY", "").encode())

    def log_message(self, *args):
        pass


class Fetcher(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        url = params.get("url", [""])[0]
        try:
            body = urllib.request.urlopen(url, timeout=2).read()  # intentional SSRF: no allowlist
            self.send_response(200)
        except Exception:
            body = b"fetch failed"
            self.send_response(502)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def _serve_metadata():
    HTTPServer(("127.0.0.1", METADATA_PORT), Metadata).serve_forever()


if __name__ == "__main__":
    threading.Thread(target=_serve_metadata, daemon=True).start()
    HTTPServer(("0.0.0.0", 8000), Fetcher).serve_forever()
