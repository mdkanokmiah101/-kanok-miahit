#!/usr/bin/env python3
"""Analyze the seo-tips-for-business-owners-bd post for all 6 framework checks."""
import re

# Read the data.js file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the post by slug
start_marker = "slug: \"seo-tips-for-business-owners-bd\""
idx = content.find(start_marker)
if idx == -1:
    print("ERROR: Could not find post slug")
    exit(1)

# Find the start of the content field - the backtick after "content: `"
content_start = content.find("content: `", idx)
if content_start == -1:
    print("ERROR: Could not find content field")
    exit(1)

# Find the closing backtick
content_tick_start = content_start + len("content: `")
# Look for the closing backtick pattern
content_end = content.find("    `,\n  },\n  {", content_tick_start)
if content_end == -1:
    content_end = content.find("    `,\n  },\n{", content_tick_start)
if content_end == -1:
    content_end = content.find("`,\n  },\n", content_tick_start)

post_content = content[content_tick_start:content_end].strip()

# Also extract the full post object metadata
post_start = idx
# Find the opening brace
obj_start = content.rfind("{\n", idx-50, idx)
if obj_start == -1:
    obj_start = idx
post_end = content_end + len("    `,")
post_section = content[obj_start:post_end]

print(f"=== POST CONTENT LENGTH: {len(post_content)} chars ===")
print(f"\n=== POST METADATA ===")
print(post_section[:800])

# ==========================================
# CHECK A: TF-IDF keyword analysis
# ==========================================
print("\n\n" + "="*70)
print("CHECK A: TF-IDF KEYWORD ANALYSIS")
print("="*70)

tfidf_keywords = {
    "DIY SEO": r'DIY\s*SEO',
    "ব্যবসায়ীদের জন্য SEO": r'ব্যবসায়ীদের\s*জন্য\s*SEO',
    "SEO টিপস": r'SEO\s*টিপস',
    "বাংলাদেশ": r'বাংলাদেশ',
    "লোকাল SEO": r'লোকাল\s*SEO',
    "কীওয়ার্ড রিসার্চ": r'কীওয়ার্ড\s*রিসার্চ',
    "গুগল বিজনেস প্রোফাইল": r'গুগল\s*বিজনেস\s*প্রোফাইল',
    "কন্টেন্ট": r'কন্টেন্ট',
    "র‍্যাংকিং": r'র‍্যাংকিং',
    "অন-পেজ SEO": r'অন-পেজ\s*SEO',
    "মোবাইল": r'মোবাইল',
    "রিভিউ": r'রিভিউ',
    "GEO": r'\bGEO\b',
    "AEO": r'\bAEO\b',
    "ওয়েবসাইট": r'ওয়েবসাইট',
    "গুগল": r'গুগল',
    "সার্চ ইঞ্জিন": r'সার্চ\s*ইঞ্জিন',
    "কাস্টমার": r'কাস্টমার',
    "ডিজিটাল": r'ডিজিটাল',
    "স্ট্র্যাটেজি": r'স্ট্র্যাটেজি',
    "ট্রাফিক": r'ট্রাফিক',
    "ব্যাকলিংক": r'ব্যাকলিংক',
    "E-E-A-T": r'E-E-A-T',
}

print("\nKeyword occurrences in post content:")
for kw, pattern in tfidf_keywords.items():
    matches = re.findall(pattern, post_content)
    count = len(matches)
    flag = "PASS" if count >= 3 else ("WARN" if count >= 1 else "FAIL")
    print(f"  [{flag}] {kw}: {count} occurrences")

# ==========================================
# CHECK B: Entity analysis
# ==========================================
print("\n\n" + "="*70)
print("CHECK B: ENTITY CHECK")
print("="*70)

expected_entities = {
    "Person: মোঃ কনক মিঞা (Kanok Miah)": r'মোঃ\s*কনক\s*মিঞা',
    "Location: ঢাকা": r'ঢাকা',
    "Location: বাংলাদেশ": r'বাংলাদেশ',
    "Location: গুলশান": r'গুলশান',
    "Brand: Google": r'গুগল',
    "Service: SEO": r'\bSEO\b',
    "Service: GMB/GBP": r'গুগল\s*বিজনেস\s*প্রোফাইল',
    "Service: কীওয়ার্ড রিসার্চ": r'কীওয়ার্ড\s*রিসার্চ',
    "Concept: E-E-A-T": r'E-E-A-T',
}

print("\nEntity presence:")
missing_entities = []
for entity, pattern in expected_entities.items():
    matches = re.findall(pattern, post_content)
    count = len(matches)
    if count > 0:
        print(f"  [PASS] {entity}: {count} occurrences")
    else:
        print(f"  [FAIL] {entity}: NOT FOUND")
        missing_entities.append(entity)

# ==========================================
# CHECK C: Pillar link
# ==========================================
print("\n\n" + "="*70)
print("CHECK C: PILLAR LINK ANALYSIS")
print("="*70)

# Check for links to pillar/guide pages
internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', post_content)

# Known pillar pages for the site
pillar_pages = [
    '/blog/complete-seo-guide-bangladesh-businesses-2026',
]

found_pillar = False
for pp in pillar_pages:
    if pp in post_content:
        print(f"  [PASS] Links to pillar: {pp}")
        found_pillar = True

if not found_pillar:
    print("  [FAIL] No link to known pillar page (complete-seo-guide-bangladesh-businesses-2026)")

# ==========================================
# CHECK D: AEO/GEO (Question headings)
# ==========================================
print("\n\n" + "="*70)
print("CHECK D: AEO/GEO CHECK")
print("="*70)

# Count question headings (## or ### that end with ?)
question_headings = re.findall(r'^#{2,3}\s+[^\n]*\?', post_content, re.MULTILINE)
print(f"\nQuestion headings found: {len(question_headings)}")
for qh in question_headings:
    print(f"  - {qh.strip()}")

# Check for FAQ section or question-answer format
has_qna_section = 'FAQ' in post_content or 'প্রশ্ন' in post_content or 'উত্তর' in post_content
print(f"\n  Q&A format: {'PASS' if has_qna_section else 'FAIL'}")

# Check for GEO/AEO topic sections
has_geo_section = 'GEO' in post_content or 'জেনারেটিভ ইঞ্জিন' in post_content
has_aeo_section = 'AEO' in post_content or 'অ্যানসার ইঞ্জিন' in post_content or 'AI সার্চ' in post_content
print(f"  GEO section: {'PASS' if has_geo_section else 'FAIL'}")
print(f"  AEO section: {'PASS' if has_aeo_section else 'FAIL'}")

# ==========================================
# CHECK E: Internal links count
# ==========================================
print("\n\n" + "="*70)
print("CHECK E: INTERNAL LINKS")
print("="*70)

all_internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', post_content)
print(f"\n  Total internal links: {len(all_internal_links)}")
for text, url in all_internal_links:
    print(f"    - [{text}]({url})")

# External links
external_links = re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', post_content)
print(f"\n  External links: {len(external_links)}")
for text, url in external_links:
    print(f"    - [{text}]({url})")

# ==========================================
# CHECK F: Schema readiness
# ==========================================
print("\n\n" + "="*70)
print("CHECK F: SCHEMA READY")
print("="*70)

print("Post metadata fields (from object header):")
meta_status = []
for field in ['slug', 'title', 'date', 'author', 'excerpt', 'tags', 'imagePlaceholder', 'content']:
    marker = f"{field}:"
    present = marker in post_section[:800]
    status = "PASS" if present else "FAIL"
    meta_status.append((field, status))
    print(f"  [{status}] {field}")

# Check for schema markup within content
has_jsonld = 'application/ld+json' in post_content or 'json-ld' in post_content.lower()
has_blogposting = 'BlogPosting' in post_content
has_faq_schema = 'FAQPage' in post_content or 'faqpage' in post_content.lower()
has_article_schema = 'Article' in post_content
has_schema_dot_org = 'schema.org' in post_content

print(f"\n  JSON-LD in content: {'PASS' if has_jsonld else 'INFO'}")
print(f"  BlogPosting: {'PASS' if has_blogposting else 'INFO'}")
print(f"  FAQPage: {'PASS' if has_faq_schema else 'INFO'}")
print(f"  Article: {'PASS' if has_article_schema else 'INFO'}")
print(f"  schema.org: {'PASS' if has_schema_dot_org else 'INFO'}")
print(f"  Note: Schema markup is typically rendered server-side or via component, not in raw content")

# ==========================================
# SUMMARY TABLE
# ==========================================
print("\n\n" + "="*70)
print("FINAL REPORT TABLE")
print("="*70)

# Determine overall TF-IDF status
tfidf_counts = []
for kw, pattern in tfidf_keywords.items():
    matches = re.findall(pattern, post_content)
    tfidf_counts.append(len(matches))
avg_density = sum(tfidf_counts) / len(tfidf_counts) if tfidf_counts else 0
high_count_keywords = sum(1 for c in tfidf_counts if c >= 3)
total_keywords = len(tfidf_counts)
tfidf_status = "PASS" if high_count_keywords >= total_keywords * 0.6 else "WARN"

# Entity status
entity_status = "PASS" if len(missing_entities) == 0 else "FAIL"

# Pillar status
pillar_status = "PASS" if found_pillar else "FAIL"

# AEO/GEO status
aeo_status = "PASS" if len(question_headings) >= 2 else "FAIL"
geo_aeo_detail = f"{len(question_headings)} question headings"
if has_geo_section:
    geo_aeo_detail += ", GEO section present"
if has_aeo_section:
    geo_aeo_detail += ", AEO section present"

# Internal links status
link_status = "PASS" if len(all_internal_links) >= 3 else "WARN" if len(all_internal_links) >= 1 else "FAIL"

# Schema status
schema_all_pass = all(s == "PASS" for _, s in meta_status)
schema_status = "PASS" if schema_all_pass else "FAIL"

print(f"""
## Post: seo-tips-for-business-owners-bd

| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: ব্যবসায়ীদের জন্য SEO, DIY SEO, বাংলাদেশ | {tfidf_status} | {high_count_keywords}/{total_keywords} keywords with >=3 occurrences; avg density {avg_density:.1f} |
| Entities | {entity_status} | Missing: {', '.join(missing_entities) if missing_entities else 'None'} |
| Pillar Link | {pillar_status} | Links to: {'/blog/complete-seo-guide-bangladesh-businesses-2026' if found_pillar else 'NOT FOUND'} |
| AEO/GEO | {aeo_status} | {geo_aeo_detail} |
| Internal Links | {link_status} | {len(all_internal_links)} total internal links |
| Schema Ready | {schema_status} | All metadata fields set ({sum(1 for _, s in meta_status if s == 'PASS')}/{len(meta_status)}) |
""")

# Detailed fix instructions if needed
print("### Fix instructions:")
fixes = []
if entity_status == "FAIL":
    fixes.append(f"- Add missing entities: {', '.join(missing_entities)}")
if pillar_status == "FAIL":
    fixes.append("- Add a pillar link to /blog/complete-seo-guide-bangladesh-businesses-2026")
if aeo_status == "FAIL":
    fixes.append("- Add more question-format headings (## or ### ending with ?)")
if link_status != "PASS":
    fixes.append(f"- Add more internal links (currently {len(all_internal_links)}, target 3+)")

if fixes:
    for f in fixes:
        print(f)
else:
    print("- No issues found. Post is well-optimized.")
