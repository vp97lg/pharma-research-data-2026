import json
import os
from datetime import datetime

DATA_PATH = "data/backlink_targets.json"
OUTPUT_DIR = "docs/guides"
BASE_URL = "https://TUUSUARIO.github.io/TUREPO"

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_hub_page(hub, internal_links, external_links):
    int_links_html = ""
    for link in internal_links:
        int_links_html += f'        <li><a href="../{link["url"]}">{link["anchor"]}</a></li>\n'

    ext_links_html = ""
    for link in external_links:
        ext_links_html += f'        <li><a href="{link["url"]}" rel="noopener" target="_blank">{link["anchor"]}</a></li>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{hub["title"]} | VipRoids Lab</title>
    <meta name="description" content="{hub["meta_desc"]}">
    <meta name="keywords" content="{hub["keywords"]}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{BASE_URL}/guides/{hub["slug"]}.html">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px; margin: 0 auto; padding: 20px; background: #0a0a0a; color: #e0e0e0; }}
        h1 {{ color: #00d4ff; }}
        h2 {{ color: #00b4d8; margin-top: 25px; }}
        a {{ color: #00d4ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .cta {{ background: #00d4ff; color: #000; padding: 12px 24px; display: inline-block; margin-top: 20px; font-weight: bold; border-radius: 4px; }}
        .section {{ background: #111; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        footer {{ margin-top: 40px; border-top: 1px solid #333; padding-top: 15px; color: #666; }}
    </style>
</head>
<body>
    <nav><a href="../index.html">VipRoids Lab</a> &gt; <a href="../guides-index.html">Guides</a></nav>
    <h1>{hub["title"]}</h1>
    <p>{hub["meta_desc"]}</p>

    <div class="section">
        <h2>Our Published Lab Reports</h2>
        <p>Every claim we make is backed by independent chromatography data:</p>
        <ul>
{int_links_html}        </ul>
    </div>

    <div class="section">
        <h2>Reference Standards</h2>
        <p>Our testing methodology follows internationally recognized pharmaceutical standards:</p>
        <ul>
{ext_links_html}        </ul>
    </div>

    <h2>About VipRoids Laboratory</h2>
    <p>We are an independent pharmaceutical analysis project focused on harm reduction through batch-level transparency. Every compound distributed through our verified network undergoes HPLC testing with published results.</p>

    <a class="cta" href="https://TUTIENDA.surge.sh">Access VipRoids Portal</a>

    <footer>
        <p>&copy; 2026 VipRoids HPLC Laboratory</p>
        <p>Last updated: {datetime.now().strftime("%Y-%m-%d")}</p>
    </footer>
</body>
</html>"""

def generate_guides_index(hubs):
    links = ""
    for hub in hubs:
        links += f'        <li><a href="guides/{hub["slug"]}.html">{hub["title"]}</a></li>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VipRoids Guides - Evidence Based Steroid Education</title>
    <meta name="description" content="Comprehensive guides on steroid purity verification, carrier oils, PCT protocols and pharmaceutical source rankings. All backed by HPLC data.">
    <meta name="robots" content="index, follow">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px; margin: 0 auto; padding: 20px; background: #0a0a0a; color: #e0e0e0; }}
        h1 {{ color: #00d4ff; }}
        a {{ color: #00d4ff; }}
        li {{ margin: 10px 0; }}
        footer {{ margin-top: 40px; color: #666; }}
    </style>
</head>
<body>
    <h1>VipRoids Guides & Rankings</h1>
    <p>Evidence-based guides backed by our independent HPLC laboratory data.</p>
    <ul>
{links}    </ul>
    <footer><p><a href="index.html">Back to Lab Reports</a> | &copy; 2026 VipRoids</p></footer>
</body>
</html>"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = load_data()

    for hub in data["hub_pages"]:
        html = generate_hub_page(hub, data["internal_links"], data["external_authority_links"])
        path = os.path.join(OUTPUT_DIR, f"{hub['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[BACKLINK] Generated: {path}")

    guides_index = generate_guides_index(data["hub_pages"])
    with open(os.path.join("docs", "guides-index.html"), "w", encoding="utf-8") as f:
        f.write(guides_index)
    print(f"[BACKLINK] Generated: guides-index.html ({len(data['hub_pages'])} hubs)")

if __name__ == "__main__":
    main()
