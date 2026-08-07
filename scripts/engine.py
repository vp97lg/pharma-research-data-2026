import json
import os

TEMPLATE_PATH = "templates/article.html"
DATA_PATH = "data/hplc_logs.json"
OUTPUT_DIR = "docs"
BASE_URL = "https://TUUSUARIO.github.io/TUREPO"

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def load_articles():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_article(template, article):
    html = template
    replacements = {
        "{{TITLE}}": article["title"],
        "{{META_DESC}}": article["meta_desc"],
        "{{KEYWORDS}}": article["keywords"],
        "{{SLUG}}": article["slug"],
        "{{DATE}}": article["date"],
        "{{CONTENT}}": article["content"]
    }
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)
    return html

def generate_index(articles):
    links = ""
    for a in sorted(articles, key=lambda x: x["date"], reverse=True):
        links += f'''        <li>
            <a href="{a["slug"]}.html">{a["title"]}</a>
            <span class="meta"> — {a["date"]}</span>
        </li>\n'''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VipRoids HPLC Laboratory - Independent Batch Verification Reports</title>
    <meta name="description" content="Independent HPLC purity reports for pharmaceutical-grade anabolic steroids. Batch transparency and harm reduction data.">
    <meta name="keywords" content="HPLC steroids, steroid purity test, anabolic lab reports, pharmaceutical steroids verification">
    <meta name="robots" content="index, follow">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px; margin: 0 auto; padding: 20px; background: #0a0a0a; color: #e0e0e0; }}
        h1 {{ color: #00d4ff; }}
        a {{ color: #00d4ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        li {{ margin: 12px 0; }}
        .meta {{ color: #888; font-size: 0.85em; }}
        .cta {{ background: #00d4ff; color: #000; padding: 12px 24px; display: inline-block; margin-top: 30px; font-weight: bold; border-radius: 4px; }}
        footer {{ margin-top: 50px; border-top: 1px solid #333; padding-top: 20px; color: #666; }}
    </style>
</head>
<body>
    <h1>VipRoids HPLC Laboratory</h1>
    <p>Independent batch verification reports for pharmaceutical-grade compounds. Every report includes full chromatography methodology and results.</p>
    <h2>Published Reports ({len(articles)} available)</h2>
    <ul>
{links}    </ul>
    <section>
        <h2>About This Project</h2>
        <p>VipRoids HPLC Laboratory provides independent purity analysis of anabolic compounds distributed through European pharmaceutical channels. Our mission is transparency and harm reduction through verifiable data.</p>
        <a class="cta" href="https://TUTIENDA.surge.sh">Visit VipRoids Portal</a>
    </section>
    <footer>
        <p>&copy; 2026 VipRoids HPLC Laboratory | <a href="sitemap.xml">Sitemap</a></p>
    </footer>
</body>
</html>"""

def generate_sitemap(articles):
    urls = f"  <url><loc>{BASE_URL}/</loc><priority>1.0</priority></url>\n"
    for a in articles:
        urls += f"  <url><loc>{BASE_URL}/{a['slug']}.html</loc><lastmod>{a['date']}</lastmod><priority>0.8</priority></url>\n"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    template = load_template()
    articles = load_articles()

    for article in articles:
        html = generate_article(template, article)
        path = os.path.join(OUTPUT_DIR, f"{article['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[ENGINE] Generated: {path}")

    index = generate_index(articles)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index)
    print(f"[ENGINE] Generated: index.html ({len(articles)} articles)")

    sitemap = generate_sitemap(articles)
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("[ENGINE] Generated: sitemap.xml")

if __name__ == "__main__":
    main()
