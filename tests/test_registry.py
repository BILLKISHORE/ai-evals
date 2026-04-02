from mordor.registry import Registry


def test_register_and_get():
    reg = Registry("test")
    reg.register("foo", str)
    assert reg.get("foo") is str


def test_list_registered():
    reg = Registry("test")
    reg.register("a", int)
    reg.register("b", float)
    assert sorted(reg.list()) == ["a", "b"]


def test_get_unknown_returns_none():
    reg = Registry("test")
    assert reg.get("nope") is None


def test_decorator():
    reg = Registry("test")

    @reg.decorator("bar")
    class Bar:
        pass

    assert reg.get("bar") is Bar
