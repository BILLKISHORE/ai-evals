import importlib
import pkgutil
from pathlib import Path


class Registry:
    def __init__(self, kind):
        self.kind = kind
        self._items = {}

    def register(self, name, cls):
        self._items[name] = cls

    def get(self, name):
        return self._items.get(name)

    def list(self):
        return list(self._items.keys())

    def decorator(self, name):
        def wrap(cls):
            self.register(name, cls)
            return cls
        return wrap

    def discover(self, package):
        pkg_path = Path(package.__file__).parent
        for info in pkgutil.iter_modules([str(pkg_path)]):
            if info.name.startswith("_"):
                continue
            importlib.import_module(f"{package.__name__}.{info.name}")

    def discover_folder(self, folder_path):
        folder = Path(folder_path)
        if not folder.exists():
            return
        for py_file in folder.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)


provider_registry = Registry("provider")
attack_registry = Registry("attack")

register_provider = provider_registry.decorator
register_attack = attack_registry.decorator
