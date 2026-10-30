# Working on the network website

- Keep the site static: Markdown, Zensical, HTML/CSS and only necessary browser JS.
- English is the initial review language. Do not publish machine translations by default.
- The network is informal and has no separate legal entity. Do not invent formal
  membership, representation, funding, partnerships, contact routes or outcomes.
- Preserve the difference between project partners, contributors and the current
  working group. Claims about people and organisations need supplied or cited sources.
- The working name and shared principles are provisional. Keep draft status visible
  until the team agrees otherwise. `noindex` is not access control.
- Keep internal research and private project records outside `docs/` and `site/`.
- Update the JSON directory when changing names, people or links on the network page.
- Reuse terms must be explicit. Do not treat free downloads as openly licensed.
- Do not publish participant photos without appropriate consent and usage rights.
- Build with `.venv/Scripts/python -m zensical build --strict`, then run
  `.venv/Scripts/python tools/check_site.py` (use `.venv/bin/python` on Unix).
- Review layout changes in a browser at desktop and mobile widths. Verify nested
  pages and GitHub Pages subpath URLs. A passing build is not visual QA.
