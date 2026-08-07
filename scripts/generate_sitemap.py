import glob
import os
from datetime import datetime

BASE_URL = "https://vp97lg.github.io/pharma-research-data-2026"
OUTPUT_DIR = "docs"

def generate_full_sitemap():
    today = datetime.now().strftime("%Y-%m-%d")
    urls = f'  <url><loc>{BASE_URL}/</loc><priority>1.0</priority></url>\n'

    # Artículos HPLC
    hplc_files = glob.glob("docs/*.html")
    for f in sorted(hplc_files):
        filename = os.path.basename(f)
        if filename != "index.html":
            urls += f'  <url><loc>{BASE_URL}/{filename}</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>\n'

    # Páginas GEO
    geo_files = glob.glob("docs/geo/*.html")
    print(f"[SITEMAP] Found {len(geo_files)} geo pages")
    for f in sorted(geo_files):
        slug = f.replace("docs/", "").replace("\\", "/")
        urls += f'  <url><loc>{BASE_URL}/{slug}</loc><lastmod>{today}</lastmod><priority>0.6</priority></url>\n'

    # Guías
    guide_files = glob.glob("docs/guides/*.html")
    print(f"[SITEMAP] Found {len(guide_files)} guide pages")
    for f in sorted(guide_files):
        slug = f.replace("docs/", "").replace("\\", "/")
        urls += f'  <url><loc>{BASE_URL}/{slug}</loc><lastmod>{today}</lastmod><priority>0.7</priority></url>\n'

    # Índices
    for index_page in ["geo-index.html", "guides-index.html"]:
        urls += f'  <url><loc>{BASE_URL}/{index_page}</loc><lastmod>{today}</lastmod><priority>0.5</priority></url>\n'

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""

    path = os.path.join(OUTPUT_DIR, "sitemap.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(sitemap)

    total = len(hplc_files) + len(geo_files) + len(guide_files) + 3
    print(f"[SITEMAP] Generated sitemap.xml with {total} URLs")

if __name__ == "__main__":
    generate_full_sitemap()
