"""Deliberately vulnerable path-traversal target for sandbox verification.

The /read endpoint joins a user path onto a base directory with no
sanitization, so ../ escapes the web root. On startup the server writes the
CANARY to a file outside that root; a successful traversal reads it. This
exists only to be exploited inside the isolated verifier sandbox.
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

BASE_DIR = "/srv/public"
SECRET_PATH = "/srv/secret/canary.txt"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        rel = params.get("path", ["index.html"])[0]
        target = os.path.join(BASE_DIR, rel)  # intentional traversal point
        try:
            with open(target, "rb") as fh:
                body = fh.read()
            self.send_response(200)
        except OSError:
            body = b"not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def _seed():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(SECRET_PATH), exist_ok=True)
    with open(os.path.join(BASE_DIR, "index.html"), "w") as fh:
        fh.write("ok")
    with open(SECRET_PATH, "w") as fh:
        fh.write(os.environ.get("CANARY", ""))


if __name__ == "__main__":
    _seed()
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
