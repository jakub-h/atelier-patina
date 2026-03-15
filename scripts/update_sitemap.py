"""
Update sitemap.xml with today's date for all HTML pages.

Usage:
    python scripts/update_sitemap.py [--date YYYY-MM-DD]

By default uses today's date. Run this after adding or editing pages.
"""

import argparse
import shutil
import subprocess
from datetime import date
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent
BASE_URL = "https://restaurovanipatina.cz"

# Metadata for known pages: (changefreq, priority)
PAGE_META: dict[str, tuple[str, str]] = {
    "index.html": ("monthly", "1.0"),
    "contact.html": ("yearly", "0.8"),
    "our-services.html": ("yearly", "0.8"),
    "about-us.html": ("yearly", "0.7"),
    "realizations.html": ("yearly", "0.7"),
}
GALLERY_META = ("yearly", "0.6")


def get_last_modified(path: Path) -> str:
    """Return the date of the last git commit that touched this file, or today."""
    git_cmd = shutil.which("git")
    if not git_cmd:
        return str(date.today())
    try:
        # path is from repo (collect_urls), not user input
        result = subprocess.run(
            [git_cmd, "log", "-1", "--format=%cs", "--", str(path)],
            capture_output=True,
            text=True,
            cwd=SITE_ROOT,
            check=False,
        )
        date_str = result.stdout.strip()
        if date_str:
            return date_str
    except OSError as e:
        print(f"git log failed for {path}: {e}")
    return str(date.today())


def collect_urls() -> list[dict]:
    urls = []

    # Root HTML pages in a fixed priority order
    root_pages = [
        "index.html",
        "contact.html",
        "our-services.html",
        "about-us.html",
        "realizations.html",
    ]
    for filename in root_pages:
        page_path = SITE_ROOT / filename
        if not page_path.exists():
            continue
        changefreq, priority = PAGE_META.get(filename, ("yearly", "0.5"))
        urls.append(
            {
                "loc": f"{BASE_URL}/{filename}",
                "lastmod": get_last_modified(page_path),
                "changefreq": changefreq,
                "priority": priority,
            }
        )

    # Gallery pages
    gallery_dir = SITE_ROOT / "gallery_pages"
    for page_path in sorted(gallery_dir.glob("*.html")):
        changefreq, priority = GALLERY_META
        urls.append(
            {
                "loc": f"{BASE_URL}/gallery_pages/{page_path.name}",
                "lastmod": get_last_modified(page_path),
                "changefreq": changefreq,
                "priority": priority,
            }
        )

    return urls


def build_sitemap(urls: list[dict], override_date: str | None = None) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in urls:
        lastmod = override_date or url["lastmod"]
        lines.append("  <url>")
        lines.append(f"    <loc>{url['loc']}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{url['changefreq']}</changefreq>")
        lines.append(f"    <priority>{url['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate sitemap.xml")
    parser.add_argument(
        "--date",
        default=None,
        help="Override lastmod date for all URLs (format: YYYY-MM-DD). "
        "By default uses the date of each file's last git commit.",
    )
    args = parser.parse_args()

    urls = collect_urls()
    sitemap = build_sitemap(urls, override_date=args.date)

    sitemap_path = SITE_ROOT / "sitemap.xml"
    sitemap_path.write_text(sitemap, encoding="utf-8")
    print(f"Updated {sitemap_path} with {len(urls)} URLs.")
    for url in urls:
        print(f"  {url['loc']}  [{args.date or url['lastmod']}]")


if __name__ == "__main__":
    main()
