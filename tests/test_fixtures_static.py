"""Offline check that the vulnerable fixture servers parse."""
import ast
import pathlib


def test_fixture_servers_parse():
    for name in ("pathtrav", "ssrf", "sqli"):
        source = (pathlib.Path("fixtures") / name / "server.py").read_text()
        ast.parse(source)
