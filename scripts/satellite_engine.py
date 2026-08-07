import json
import os
import hashlib
from datetime import datetime, timedelta

DATA_PATH = "data/satellite_locations.json"
OUTPUT_DIR = "docs/geo"
BASE_URL = "https://TUUSUARIO.github.io/TUREPO"

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_unique_content(product, location, templates, index):
    template = templates[index % len(templates)]
    description = template.format(product=product, location=location)

    seed = f"{product}-{location}"
    date_offset = int(hashlib.md5(seed.encode()).hexdigest()[:4], 16) % 60
    fake_date = (datetime.now() - timedelta(days=date_offset)).strftime("%Y-%m-%d")

    benefits = [
        f"Athletes in {location} consistently report improved recovery times when using verified {product} from European pharmaceutical sources.",
        f"Independent testing confirms that {product} from certified EU manufacturers maintains 99%+ purity even after international shipping to {location}.",
        f"The demand for lab-tested {product} in {location} has increased by over 200% in 2026, driven by awareness of underdosed underground products.",
        f"Medical professionals in {location} increasingly recognize the harm reduction value of HPLC-verified compounds like {product}."
    ]
    selected_benefit = benefits[index % len(benefits)]

    faq_questions = [
        f"Is {product} legal to purchase in {location}?",
        f"How long does shipping take to {location}?",
        f"What purity level should I expect from pharmaceutical {product}?",
        f"How can I verify my {product} batch is authentic?"
    ]
    faq_answers = [
        "Regulations vary by jurisdiction. Always consult local laws before purchasing any pharmaceutical compound.",
        f"Standard EU stealth shipping to {location} typically takes 5-10 business days with full tracking.",
        "Pharmaceutical-grade preparations should test above 98% purity via HPLC. We provide batch certificates for every order.",
        "Every batch we distribute includes an HPLC certificate with chromatography data. You can cross-reference batch numbers with our published lab reports."
    ]
    faq_idx = index % len(faq_questions)

    return description, fake_date, selected_benefit, faq_questions[faq_idx], faq_answers[faq_idx]

def generate_satellite_page(product, location, description, date, benefit, faq_q, faq_a):
    slug = f"{product.lower().replace(' ', '-').replace('(', '').replace(')', '')}-{location.lower().replace(' ', '-')}"
    title = f"Verified {product} - HPLC Tested - Delivery to {location}"
    product_clean = product.split(" ")[0]

    return slug, f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | VipRoids Lab</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="buy {product_clean} {location}, {product_clean} delivery {location}, HPLC {product_clean}, verified steroids {location}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{BASE_URL}/geo/{slug}.html">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px; margin: 0 auto; padding: 20px; background: #0a0a0a; color: #e0e0e0; }}
        h1 {{ color: #00d4ff; font-size: 1.6em; }}
        h2 {{ color: #00b4d8; margin-top: 25px; }}
        a {{ color: #00d4ff; text-decoration: none; }}
        .cta {{ background: #00d4ff; color: #000; padding: 12px 24px; display: inline-block; margin-top: 20px; font-weight: bold; border-radius: 4px; }}
        .faq {{ background: #111; border-left: 3px solid #00d4ff; padding: 15px; margin: 20px 0; }}
        footer {{ margin-top: 40px; border-top: 1px solid #333; padding-top: 15px; color: #666; font-size: 0.85em; }}
    </style>
</head>
<body>
    <nav><a href="../index.html">VipRoids Lab</a> &gt; <a href="../geo-index.html">Locations</a> &gt; {location}</nav>
    <h1>{title}</h1>
    <p>{description}</p>

    <h2>Why Choose Verified {product}?</h2>
    <p>{benefit}</p>
    <p>Every batch distributed through our network undergoes independent HPLC analysis. We publish full chromatography reports including purity percentage, concentration verification, heavy metal screening, and sterility confirmation.</p>

    <h2>Our Quality Standards</h2>
    <ul>
        <li>Purity verified above 98% via HPLC chromatography</li>
        <li>Heavy metal screening (Palladium, Lead, Mercury) below 0.1ppm</li>
        <li>Bacterial endotoxin testing for all injectable preparations</li>
        <li>MCT pharmaceutical-grade carrier oil for optimal stability</li>
        <li>0.22 micron sterile filtration confirmed</li>
    </ul>

    <h2>Shipping to {location}</h2>
    <p>All orders ship from secure EU warehouses using vacuum-sealed stealth packaging. No external markings indicate pharmaceutical content. Tracking provided within 48 hours of payment confirmation.</p>

    <div class="faq">
        <h2>FAQ</h2>
        <p><strong>Q: {faq_q}</strong></p>
        <p>A: {faq_a}</p>
    </div>

    <h2>View Lab Reports</h2>
    <p>Browse our published HPLC reports for complete transparency:</p>
    <ul>
        <li><a href="../hplc-testosterone-enanthate-july-2026.html">Testosterone Enanthate - July 2026</a></li>
        <li><a href="../hplc-trenbolone-acetate-thermal-degradation-study.html">Trenbolone Thermal Degradation Study</a></li>
        <li><a href="../carrier-oil-mct-vs-gso-oxidative-stability.html">Carrier Oil Stability Report</a></li>
    </ul>

    <a class="cta" href="https://TUTIENDA.surge.sh">Access VipRoids Portal</a>

    <footer>
        <p>&copy; 2026 VipRoids HPLC Laboratory | Independent pharmaceutical analysis</p>
        <p>Last updated: {date}</p>
    </footer>
</body>
</html>"""

def generate_geo_index(pages):
    links = ""
    for slug, product, location in sorted(pages, key=lambda x: x[2]):
        links += f'        <li><a href="geo/{slug}.html">{product} → {location}</a></li>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VipRoids HPLC Lab - Verified Pharmaceutical Delivery Locations</title>
    <meta name="description" content="HPLC verified pharmaceutical-grade steroids with delivery to over 50 locations worldwide. Every batch independently tested.">
    <meta name="robots" content="index, follow">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px; margin: 0 auto; padding: 20px; background: #0a0a0a; color: #e0e0e0; }}
        h1 {{ color: #00d4ff; }}
        a {{ color: #00d4ff; }}
        li {{ margin: 6px 0; }}
        footer {{ margin-top: 40px; color: #666; }}
    </style>
</head>
<body>
    <h1>Delivery Locations - HPLC Verified Stock</h1>
    <p>Select your location to view available pharmaceutical-grade compounds with independent laboratory verification.</p>
    <ul>
{links}    </ul>
    <footer><p><a href="index.html">Back to Lab Reports</a> | &copy; 2026 VipRoids</p></footer>
</body>
</html>"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = load_data()
    products = data["products"]
    locations = data["locations"]
    templates = data["templates"]

    all_pages = []
    counter = 0

    for product in products:
        for location in locations:
            desc, date, benefit, faq_q, faq_a = generate_unique_content(product, location, templates, counter)
            slug, html = generate_satellite_page(product, location, desc, date, benefit, faq_q, faq_a)

            path = os.path.join(OUTPUT_DIR, f"{slug}.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)

            all_pages.append((slug, product, location))
            counter += 1

    print(f"[SATELLITE] Generated {counter} geo-targeted pages")

    geo_index = generate_geo_index(all_pages)
    with open(os.path.join("docs", "geo-index.html"), "w", encoding="utf-8") as f:
        f.write(geo_index)
    print("[SATELLITE] Generated: geo-index.html")

if __name__ == "__main__":
    main()
