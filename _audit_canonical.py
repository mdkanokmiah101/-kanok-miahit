import re

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Find the post
start = content.find("slug: \"seo-canonical-url-guide-bd\"")
if start == -1:
    start = content.find("slug: 'seo-canonical-url-guide-bd'")

# Find end - next post slug or end of this post
post_end = content.find("},\n  {\n    slug:", start)
if post_end == -1:
    post_end = content.find("slug:", start + 200)

post_text = content[start:post_end]

# Extract content field
content_start_marker = "content: `"
ci = post_text.find(content_start_marker)
if ci == -1:
    # Try with different spacing
    content_start_marker = "content: `"
    ci = post_text.find(content_start_marker)

ci_start = ci + len(content_start_marker)
# Find the closing backtick followed by comma and newline
ci_end = post_text.find("`,\n", ci_start)
if ci_end == -1:
    ci_end = post_text.find("`,", ci_start)
content_text = post_text[ci_start:ci_end]

print(f"Content length: {len(content_text)} chars")
print()

# A. TF-IDF - count 'ক্যানোনিকাল ইউআরএল'
kw_count = content_text.count("ক্যানোনিকাল ইউআরএল")
print("=== A. TF-IDF Coverage ===")
print(f"Keyword: ক্যানোনিকাল ইউআরএল")
print(f"Occurrences in content: {kw_count}")
print(f"Status: {'PASS' if kw_count >= 5 else 'FAIL'} (< 5)")
print()

# B. Entities
has_dhaka = "ঢাকা" in content_text
has_bangladesh = "বাংলাদেশ" in content_text or "বাংলাদেশি" in content_text
has_technical_seo = "টেকনিকেল SEO" in content_text or "টেকনিক্যাল SEO" in content_text
has_ecommerce = "ই-কমার্স" in content_text
has_news = "নিউজ" in content_text

print("=== B. Semantic Entity Coverage ===")
print(f"Dhaka/Bangladesh: Dhaka={'ঢাকা' in content_text}, Bangladesh={'বাংলাদেশ' in content_text or 'বাংলাদেশি' in content_text}")
print(f"Technical SEO: {has_technical_seo}")
print(f"E-commerce: {has_ecommerce}")
print(f"News: {has_news}")
missing = []
if not has_dhaka:
    missing.append("ঢাকা (location)")
if not has_bangladesh:
    missing.append("বাংলাদেশ (location)")
if not has_technical_seo:
    missing.append("টেকনিকেল SEO (service type)")
if not has_ecommerce:
    missing.append("ই-কমার্স (industry)")
print(f"Missing: {missing if missing else 'None'}")
print()

# C. Pillar link
has_pillar_link = "/services/technical-seo" in content_text
print("=== C. Pillar-Cluster Alignment ===")
print(f"Tags: ক্যানোনিকাল ইউআরএল, ডুপ্লিকেট কন্টেন্ট, টেকনিকেল SEO, ক্যানোনিকাল ট্যাগ, বাংলাদেশ")
print(f"Pillar topic: টেকনিকেল SEO → /services/technical-seo")
print(f"Link to pillar page: {has_pillar_link}")
print()

# D. AEO/GEO - count question headings
lines = content_text.split("\n")
question_headings = []
bengali_q_starters = ["কী", "কেন", "কখন", "কোথায়", "কিভাবে", "কীভাবে"]
eng_q_starters = ["How", "What", "Why", "When", "Where", "Can", "Do", "Is", "Are"]

for line in lines:
    stripped = line.strip()
    if stripped.startswith("##") or stripped.startswith("###"):
        heading_text = stripped.lstrip("#").strip()
        for qs in bengali_q_starters:
            if heading_text.startswith(qs):
                question_headings.append(stripped)
                break
        else:
            for qs in eng_q_starters:
                if heading_text.startswith(qs):
                    question_headings.append(stripped)
                    break

print("=== D. AEO/GEO Optimization ===")
print(f"Question headings (starting with question word): {len(question_headings)}")
for qh in question_headings:
    print(f"  - {qh}")
print(f"Status: {'PASS' if len(question_headings) >= 2 else 'FAIL'} (< 2)")
print()

# Also count ALL headings for reference
all_headings = []
for line in lines:
    stripped = line.strip()
    if stripped.startswith("##") or stripped.startswith("###"):
        all_headings.append(stripped)
print("All headings in post:")
for h in all_headings:
    print(f"  {h}")
print()

# E. Internal links
internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content_text)
internal_links_filtered = [(text, url) for text, url in internal_links if url.startswith('/') and not url.startswith('//')]
print("=== E. Internal Linking ===")
print(f"Total internal links: {len(internal_links_filtered)}")
for text, url in internal_links_filtered:
    print(f"  - [{text}]({url})")
print(f"Status: {'PASS' if len(internal_links_filtered) >= 3 else 'FAIL'} (< 3)")
print()

# F. Schema
has_title = "title:" in post_text
has_excerpt = "excerpt:" in post_text
has_date = "date:" in post_text
print("=== F. Schema Ready ===")
print(f"Title set: {has_title}")
print(f"Excerpt set: {has_excerpt}")
print(f"Date set: {has_date}")
print(f"All set: {has_title and has_excerpt and has_date}")

# Print details
print()
print("=== DETAILED INFO ===")
print(f"Post slug: seo-canonical-url-guide-bd")
# Extract actual values
for field in ['title:', 'date:', 'author:', 'excerpt:', 'tags:']:
    idx = post_text.find(field)
    if idx != -1:
        line_end = post_text.find('\n', idx)
        print(f"  {post_text[idx:line_end]}")
