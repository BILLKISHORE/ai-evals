"""Deliberately vulnerable SQL-injection target for sandbox verification.

The /user endpoint concatenates the name parameter straight into a SQL query,
so a UNION-based injection can read the secrets table, which holds the CANARY.
This exists only to be exploited inside the isolated verifier sandbox.
"""
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE users (name TEXT)")
db.execute("INSERT INTO users VALUES ('alice'), ('bob')")
db.execute("CREATE TABLE secrets (value TEXT)")
db.execute("INSERT INTO secrets VALUES (?)", (os.environ.get("CANARY", ""),))
db.commit()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        name = params.get("name", [""])[0]
        query = "SELECT name FROM users WHERE name = '" + name + "'"  # intentional injection point
        try:
            rows = db.execute(query).fetchall()
            body = ("\n".join(r[0] for r in rows if r[0] is not None)).encode()
            self.send_response(200)
        except Exception as exc:
            body = str(exc).encode()
            self.send_response(500)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
