# Sandbox fixtures

Disposable vulnerable targets for confirmed exploit verification via
`DockerVerifier` fixture mode (see `docs/design/agent-jail-threat-model.md`).

Convention: the verifier runs each target on an internal, no-egress network at
hostname `target`, and seeds a fresh random value into the `CANARY` environment
variable per run. A target must expose `CANARY` only through the vulnerability
under test, so a successful exploit is one whose output contains the canary.

## cmdi (command injection)

A minimal HTTP server whose `/ping` endpoint passes input straight to a shell.

- Build: `docker build -t aibt-fixture-cmdi:latest fixtures/cmdi`
- Exploit shape: `GET http://target:8000/ping?host=x;env` injects `;env` and
  leaks the seeded `CANARY`.

## pathtrav (path traversal)

An HTTP server whose `/read?path=` endpoint joins the path onto a web root with
no sanitization. The canary is written to a file outside that root at startup.

- Build: `docker build -t aibt-fixture-pathtrav:latest fixtures/pathtrav`
- Exploit shape: `GET http://target:8000/read?path=../secret/canary.txt`

## ssrf (server-side request forgery)

An HTTP server whose `/fetch?url=` endpoint retrieves any URL with no allowlist.
A metadata sidecar bound to loopback returns the canary and is reachable only
from inside the container, so only a successful SSRF reads it.

- Build: `docker build -t aibt-fixture-ssrf:latest fixtures/ssrf`
- Exploit shape: `GET http://target:8000/fetch?url=http://127.0.0.1:9000/`

## sqli (SQL injection)

An HTTP server whose `/user?name=` endpoint concatenates the name into a SQL
query. A UNION injection reads the secrets table, which holds the canary.

- Build: `docker build -t aibt-fixture-sqli:latest fixtures/sqli`
- Exploit shape: `GET http://target:8000/user?name=' UNION SELECT value FROM secrets--`
