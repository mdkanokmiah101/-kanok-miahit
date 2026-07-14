#!/usr/bin/env python3
"""Add H1 tags to Elementor pages missing them on kanokmiah.com"""
import requests, json, base64

BASE = "https://kanokmiah.com/wp-json/wp/v2"
AUTH = base64.b64encode(b"KM856W2s:f44#%W@$%ffefr4dS").decode()
HEADERS = {"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}

# Pages missing H1 with their new H1 text
pages_to_fix = {
    7706: "Photo Gallery — Kanok Miah",
    222: "Blog — Kanok Miah",
    5121: "Facebook Marketing Services in Bangladesh",
    5091: "Social Media Marketing Service in Bangladesh",
    5111: "Branding Services in Bangladesh",
    5101: "SEO Consulting Service in Bangladesh",
    5141: "Backlink Service in Bangladesh",
    5131: "Generative Engine Optimization (GEO) Service in Bangladesh"
}

for page_id, h1_text in pages_to_fix.items():
    # Get page meta
    r = requests.get(f"{BASE}/pages/{page_id}/meta", headers=HEADERS)
    if r.status_code != 200:
        print(f"❌ Page {page_id}: Failed to get meta ({r.status_code})")
        continue

    meta_list = r.json()
    elementor_data = None
    el_id = None
    for m in meta_list:
        if m.get("key") == "_elementor_data":
            elementor_data = json.loads(m.get("value", "[]"))
            el_id = m.get("id")
            break

    if not elementor_data or not el_id:
        print(f"❌ Page {page_id}: No Elementor data found")
        continue

    # Add heading widget
    widget = {
        "id": f"h1_{page_id}",
        "widgetType": "heading",
        "settings": {"title": h1_text, "tag": "h1", "header_size": "h1", "align": "center"},
        "elements": []
    }

    if isinstance(elementor_data, list) and len(elementor_data) > 0:
        if "elements" in elementor_data[0]:
            elementor_data[0]["elements"].insert(0, widget)
        else:
            elementor_data[0]["elements"] = [widget]
    else:
        elementor_data = [{"id": f"sec_{page_id}", "elType": "section", "settings": {},
            "elements": [{"id": f"col_{page_id}", "elType": "column", "settings": {"_column_size": 100}, "elements": [widget]}]}]

    r2 = requests.post(f"{BASE}/pages/{page_id}/meta/{el_id}",
        headers=HEADERS, json={"key": "_elementor_data", "value": json.dumps(elementor_data)})

    if r2.status_code in (200, 201):
        print(f"✅ Page {page_id}: H1 added — \"{h1_text}\"")
    else:
        print(f"❌ Page {page_id}: Failed ({r2.status_code}): {r2.text[:200]}")

    # Also set page title as H1 via post_content
    requests.post(f"{BASE}/pages/{page_id}", headers=HEADERS, json={"content": f"<!-- wp:heading --><h1>{h1_text}</h1><!-- /wp:heading -->"})

print("\n✅ Done!")
