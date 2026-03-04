# FlyPython

[python.flypython.com](https://python.flypython.com)

FlyPython is a bilingual Jekyll site focused on Python-based AI agent development and durable engineering learning resources.

## Site Structure

- [index.md](index.md) is the English landing page.
- [zh-cn.md](zh-cn.md) is the Chinese landing page.
- [_layouts/default.html](_layouts/default.html) contains the shared shell, TOC script, and language toggle.
- [assets/css/custom.css](assets/css/custom.css) contains the custom visual layer for cards, details sections, and layout polish.
- [tools/check_links.py](tools/check_links.py) audits external links used by the landing pages.

## Local Maintenance

- Install Python dependency: `python3 -m pip install -r requirements.txt`
- Run the link audit: `python3 tools/check_links.py`
- Jekyll dependencies are declared in [Gemfile](Gemfile)

## Notes

- Generated audit output under `reports/` is ignored and should not be committed.
- The current local Ruby runtime must be `3.x` or newer to install the `github-pages` dependency set successfully.
