"""Build locally or for GitHub Pages, including assets on nested 404 routes.

SITE_URL overrides the destination; otherwise GitHub Actions supplies the
repository identity. Normal local Zensical commands do not need this helper.
"""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    site_url = os.environ.get("SITE_URL", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not site_url and repository:
        owner, name = repository.split("/", 1)
        host = f"{owner.lower()}.github.io"
        site_url = f"https://{host}/" + ("" if name.lower() == host else f"{name}/")
    if not site_url:
        return subprocess.call([sys.executable, "-m", "zensical", "build", "--strict"], cwd=ROOT)
    parsed = urlsplit(site_url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc or parsed.query or parsed.fragment:
        raise SystemExit("SITE_URL must be a complete HTTP(S) site URL without query or fragment")
    site_url = site_url.rstrip("/") + "/"
    config = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    config = config.replace("[project]\n", f"[project]\nsite_url = {json.dumps(site_url)}\n", 1)
    config = config.replace("[project.extra]\n", f"[project.extra]\nbase_path = {json.dumps(parsed.path.rstrip('/'))}\n", 1)
    # Keep relative source/asset paths anchored in this checkout.
    config_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", prefix=".zensical-build-", dir=ROOT, encoding="utf-8", delete=False) as handle:
            handle.write(config)
            config_path = Path(handle.name)
        return subprocess.call([sys.executable, "-m", "zensical", "build", "--strict", "-f", str(config_path)], cwd=ROOT)
    finally:
        if config_path:
            config_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
