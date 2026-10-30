# Functional Juggling Network — website draft

A static Zensical website for an emerging European network for inclusive circus
and movement, rooted in Functional Juggling. The name, shared principles and
organisation profiles are provisional. This network has no separate legal entity.

## Run locally

Python 3.13 is the reference runtime. From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m zensical serve
```

Open http://127.0.0.1:8010/. On macOS/Linux use `.venv/bin/python`.

Build and check:

```powershell
.venv\Scripts\python -m zensical build --strict
.venv\Scripts\python tools/check_site.py
```

The checker verifies internal files and fragments, draft-indexing metadata,
page structure and agreement between the public directory and its JSON export.
It does not contact external sites or replace browser accessibility testing.

## Edit

- `docs/*.md`: English content; no translation or CMS layer in this first draft.
- `overrides/main.html`: original presentation template, navigation and footer.
- `docs/assets/stylesheets/network.css`: design tokens and responsive layouts.
- `docs/assets/images/`: original, code-native SVG graphics.
- `docs/assets/data/network.json`: draft structured directory, with source links
  and review status. Keep names, people and links aligned with `docs/network.md`.
- `notes/`: local editorial research; Git-ignored and excluded from publication.
- `site/`: generated output; ignored by Git.

The NICA website in the sibling checkout informed the Zensical configuration and
local-preview approach. This repo has an independent visual identity and does
not import NICA's translations, deployment credentials, photos or generated files.

## GitHub Pages review hosting

Repository: [abhuva/fj-network-website](https://github.com/abhuva/fj-network-website).
Review website: https://abhuva.github.io/fj-network-website/.

GitHub Pages uses **GitHub Actions** as its publishing source. Open a pull request
targeting `main` to build and check the proposed changes. Merging the PR into
`main` automatically builds and publishes the updated website. Direct pushes to
`main` also publish; manual workflow runs publish only when run on `main`.
Pull requests do not replace the live review website. Relative URLs support
both project Pages paths and a domain root.

The CI build helper derives the temporary Pages URL from `GITHUB_REPOSITORY`.
This also gives the error page correct asset paths when displayed at a missing
nested URL. Set `SITE_URL` when building for a custom host; this overrides the
derived URL. For a local subpath check, set `SITE_URL` to
`http://127.0.0.1:8010/fj-network-website/`, then run `python tools/build.py`
and `python tools/check_site.py`. Clear it before returning to normal preview.

There is intentionally no production domain or canonical URL configured yet.
The draft has `noindex, nofollow` metadata and `robots.txt` blocks crawling.
These do not make a public GitHub Pages preview private. Keep private project
documents and personal information out of `docs/`.

Before the final launch, confirm the name, profiles, responsible operator,
contact route, required legal information and content licences. Then set the
final `site_url`, remove the draft indexing restrictions, and review all draft
wording. Team discussion starts at `/review/`.

## Design and reuse

Warm paper, dark green ink, terracotta accents, generous serif headings, numbered
editorial sections and diagrams of movement pathways. All assets load locally.
Mobile navigation is native HTML; the site requires no JavaScript.

Original code and SVG illustrations: MIT, see `LICENSE`. Original editorial
text and directory data: collective licence decision pending. Linked resources
retain their own terms. No participant photos are included.
