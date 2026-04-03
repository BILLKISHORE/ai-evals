import json
import re
from pathlib import Path

SOURCE_EXTENSIONS = {".c", ".h", ".py", ".js", ".java", ".go", ".rs", ".sh", ".rb", ".php"}

MAX_LINES = 500


class CodeLoader:
    """Loads vulnerable code samples from a directory with optional manifest."""

    def __init__(self, base_path):
        self.base_path = Path(base_path)

    def load_all(self):
        manifest = self._load_manifest()
        cve_manifest = self._load_cve_manifest()

        if cve_manifest:
            return self._load_cve_samples(cve_manifest)
        elif manifest:
            return self._load_with_manifest(manifest)
        else:
            return self._load_raw()

    def _load_manifest(self):
        manifest_path = self.base_path / "manifest.json"
        if not manifest_path.exists():
            return None
        with open(manifest_path) as f:
            data = json.load(f)
        first_key = next(iter(data), "")
        if first_key.startswith("CVE-"):
            return None
        return data

    def _load_cve_manifest(self):
        manifest_path = self.base_path / "manifest.json"
        if not manifest_path.exists():
            return None
        with open(manifest_path) as f:
            data = json.load(f)
        first_key = next(iter(data), "")
        if first_key.startswith("CVE-"):
            return data
        return None

    def _load_with_manifest(self, manifest):
        samples = []
        for filename, meta in manifest.items():
            filepath = self.base_path / filename
            if not filepath.exists():
                continue
            code = filepath.read_text()
            samples.append({
                "filename": filename,
                "code": code,
                "language": meta.get("language", _detect_language(filename)),
                **meta,
            })
        return samples

    def _load_cve_samples(self, cve_manifest):
        samples = []
        for cve_id, summary in cve_manifest.items():
            cve_dir = self.base_path / cve_id
            if not cve_dir.exists():
                continue

            meta_path = cve_dir / "meta.json"
            meta = {}
            if meta_path.exists():
                with open(meta_path) as f:
                    meta = json.load(f)

            for src_file in cve_dir.iterdir():
                if src_file.suffix in SOURCE_EXTENSIONS:
                    code = src_file.read_text()
                    samples.append({
                        "filename": src_file.name,
                        "code": code,
                        "cve_id": cve_id,
                        "language": meta.get("language", _detect_language(src_file.name)),
                        **meta,
                    })
                    break

        return samples

    def _load_raw(self):
        samples = []
        for filepath in sorted(self.base_path.rglob("*")):
            if filepath.is_file() and filepath.suffix in SOURCE_EXTENSIONS:
                code = filepath.read_text()
                lines = code.splitlines()
                if len(lines) > MAX_LINES:
                    chunks = _split_at_functions(code, filepath.suffix)
                    for i, chunk in enumerate(chunks):
                        samples.append({
                            "filename": f"{filepath.relative_to(self.base_path)}:chunk{i}",
                            "code": chunk,
                            "language": _detect_language(filepath.name),
                        })
                else:
                    samples.append({
                        "filename": str(filepath.relative_to(self.base_path)),
                        "code": code,
                        "language": _detect_language(filepath.name),
                    })
        return samples


def _detect_language(filename):
    ext_map = {
        ".c": "c", ".h": "c", ".py": "python", ".js": "javascript",
        ".java": "java", ".go": "go", ".rs": "rust", ".sh": "bash",
        ".rb": "ruby", ".php": "php",
    }
    return ext_map.get(Path(filename).suffix, "text")


def _split_at_functions(code, ext):
    if ext in (".py",):
        pattern = r"^(?:def |class )"
    elif ext in (".c", ".h", ".java"):
        pattern = r"^(?:\w[\w\s\*]+\s+\w+\s*\()"
    elif ext in (".js",):
        pattern = r"^(?:function |const \w+ = |export )"
    else:
        pattern = r"^(?:func |fn |def )"

    lines = code.splitlines(True)
    chunks = []
    current_chunk = []
    for line in lines:
        if re.match(pattern, line, re.MULTILINE) and current_chunk:
            chunks.append("".join(current_chunk))
            current_chunk = []
        current_chunk.append(line)
    if current_chunk:
        chunks.append("".join(current_chunk))

    return chunks if chunks else [code]
