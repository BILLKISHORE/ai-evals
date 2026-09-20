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
