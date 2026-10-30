"""Check the actual static output, including project-Pages-relative links."""

from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.references = []
        self.h1_count = 0
        self.main_count = 0
        self.is_draft = False
        self.language = None
        self.base_path = ""
        self.errors = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate id: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if tag == "meta" and attrs.get("name") == "robots":
            self.is_draft = "noindex" in attrs.get("content", "")
        if tag == "meta" and attrs.get("name") == "site-base-path":
            self.base_path = attrs.get("content", "")
        for key in ("href", "src"):
            if key in attrs:
                self.references.append(attrs[key])
        if tag == "img" and "alt" not in attrs:
            self.errors.append("Image without alternative text attribute")


def check():
    if not (SITE / "index.html").is_file():
        raise SystemExit("Build the site first: python -m zensical build --strict")
    pages = {path.resolve(): Page(path) for path in SITE.rglob("*.html")}
    errors = []
    references_checked = 0
    for path, page in pages.items():
        label = path.relative_to(SITE)
        problems = page.errors[:]
        if page.h1_count != 1:
            problems.append(f"Expected one h1, found {page.h1_count}")
        if page.main_count != 1 or "main" not in page.ids:
            problems.append("Expected one main landmark with a skip-link target")
        if page.language != "en":
            problems.append("Missing English document language")
        if not page.is_draft:
            problems.append("Missing draft noindex metadata")
        for ref in page.references:
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc:
                continue
            if parsed.path.startswith("/"):
                # Zensical uses site-root paths on 404 pages, which can be
                # displayed at arbitrary nesting depths by the host.
                prefix = page.base_path + "/"
                if path.name != "404.html" or not parsed.path.startswith(prefix):
                    problems.append(f"Unexpected root-relative URL: {ref}")
                    continue
                destination = (SITE / unquote(parsed.path[len(prefix):])).resolve()
            else:
                destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not destination.is_relative_to(SITE.resolve()):
                problems.append(f"Reference leaves site output: {ref}")
                continue
            if destination.is_dir():
                destination /= "index.html"
            if not destination.is_file():
                problems.append(f"Missing local target: {ref}")
                continue
            references_checked += 1
            if not ref.strip():
                problems.append("Empty link or asset URL")
            if parsed.fragment and destination in pages:
                if unquote(parsed.fragment) not in pages[destination].ids:
                    problems.append(f"Missing fragment target: {ref}")
        errors.extend(f"{label}: {problem}" for problem in problems)

    directory = json.loads((SITE / "assets/data/network.json").read_text(encoding="utf-8"))
    network_html = (SITE / "network/index.html").read_text(encoding="utf-8")
    # HTMLParser normalizes entities, so compare rendered visible text and hrefs.
    class Text(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.parts = []
        def handle_data(self, text):
            self.parts.append(text)

    visible = Text()
    visible.feed(network_html)
    network_text = " ".join(visible.parts)
    network_links = pages[(SITE / "network/index.html").resolve()].references
    ids = set()
    for org in directory["organisations"]:
        if org["id"] in ids:
            errors.append(f"Duplicate organisation identifier: {org['id']}")
        ids.add(org["id"])
        for name in [org["name"], *org["people"]]:
            if name not in network_text:
                errors.append(f"Directory entry missing from network page: {name}")
        if org["url"] not in network_links:
            errors.append(f"Directory URL missing from network page: {org['url']}")
        if not org["sources"] or not org["review_status"]:
            errors.append(f"Missing provenance/review state: {org['id']}")
    if not (SITE / "robots.txt").read_text(encoding="utf-8").strip().endswith("Disallow: /"):
        errors.append("Draft robots.txt does not block crawling")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {len(pages)} pages, {references_checked} local links/assets and {len(ids)} directory entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
