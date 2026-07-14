#!/usr/bin/env python3
"""Fixed framework check for batch 3 blog posts - handles Markdown links."""
import re
import sys

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

# Read entire file
with open(FILEPATH, "r", encoding="utf-8") as f:
    text = f.read()

slugs_to_check = [
    "google-search-console-performance-guide",
    "schema-markup-rich-snippets-techniques",
    "seo-faq-schema-bangladesh",
    "seo-howto-schema-bangladesh",
    "seo-hreflang-guide-bangladesh",
    "seo-structured-data-guide-bd",
    "seo-json-ld-schema-bangladesh",
    "seo-breadcrumb-schema-bd",
    "seo-for-startups-bangladesh",
    "seo-for-law-firms-bangladesh",
    "seo-healthcare-medical-clinics-bangladesh",
]

# Split by post boundaries
post_pattern = re.compile(
    r'\{\s*\n\s+slug:\s*"([^"]+)"(.*?)\n\s+\},?\s*\n\s*(?=\{\s*\n\s+slug:)',
    re.DOTALL
)

# Find all posts
all_posts = {}
for m in post_pattern.finditer(text):
    slug = m.group(1)
    block = m.group(0)
    all_posts[slug] = block

print(f"Found {len(all_posts)} total posts in file")

def extract_field(block, field_name):
    """Extract a simple quoted field from a post block."""
    # Try same line
    m = re.search(rf'{field_name}:\s*"([^"]*)"', block)
    if m:
        return m.group(1)
    # Try next line with indentation
    m = re.search(rf'{field_name}:\s*\n\s+"((?:[^"\\]|\\.)*)"', block)
    if m:
        return m.group(1)
    return ""

def extract_tags(block):
    """Extract tags array."""
    m = re.search(r'tags:\s*\[(.*?)\]', block, re.DOTALL)
    if not m:
        return []
    tags_str = m.group(1)
    return re.findall(r'"([^"]*)"', tags_str)

def get_content_block(block):
    """Get content template literal - handles escaped backticks properly."""
    m = re.search(r'content:\s*`', block)
    if not m:
        return ""
    start = m.end()
    after = block[start:]
    # Find unescaped closing backtick
    i = 0
    while i < len(after):
        if after[i] == '\\' and i + 1 < len(after):
            i += 2  # skip escaped sequence
        elif after[i] == '`':
            return after[:i]
        else:
            i += 1
    return ""

def extract_primary_kw(title):
    """Extract primary keyword from title."""
    title_stripped = title.strip()
    # Split by common separators
    first_part = re.split(r'[:—–,-]', title_stripped)[0].strip()
    words = first_part.split()
    if len(words) >= 4:
        return ' '.join(words[:3])
    elif len(words) >= 2:
        return ' '.join(words[:2])
    else:
        return words[0] if words else title_stripped

# Run checks
results = []
for slug in slugs_to_check:
    if slug not in all_posts:
        print(f"WARNING: slug '{slug}' not found!")
        results.append((slug, "NOT FOUND", "", "", [], "", {}, {}))
        continue
    
    block = all_posts[slug]
    
    title = extract_field(block, "title")
    date_val = extract_field(block, "date")
    excerpt = extract_field(block, "excerpt")
    tags = extract_tags(block)
    content = get_content_block(block)
    
    # ---------- Check A: TF-IDF ----------
    primary_kw = extract_primary_kw(title)
    content_lower = content.lower()
    kw_count = content_lower.count(primary_kw.lower())
    check_a_flag = "PASS" if kw_count >= 5 else f"FAIL (count={kw_count})"
    
    # ---------- Check B: Entities ----------
    entities = ["Dhaka", "Bangladesh", "Google", "SEO"]
    missing_entities = []
    for ent in entities:
        if ent.lower() not in content_lower:
            missing_entities.append(ent)
    check_b_flag = "PASS" if not missing_entities else f"FAIL (missing: {', '.join(missing_entities)})"
    
    # ---------- Check C: Pillar ----------
    # Markdown links: [text](/services/...) or [text](/industries/...) or [text](/blog/...)
    pillar_links = re.findall(r'\]\((/services/[^)]*)\)', content)
    pillar_links += re.findall(r'\]\((/industries/[^)]*)\)', content)
    pillar_links += re.findall(r'\]\((/blog/[^)]*)\)', content)
    check_c_flag = "PASS" if pillar_links else "FAIL (no pillar links)"
    pillar_count = len(pillar_links)
    
    # ---------- Check D: AEO/GEO ----------
    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are']
    bengali_q_words = ['কী', 'কেন', 'কখন', 'কোথায়', 'কিভাবে', 'কি']
    
    headings = re.findall(r'^#{2,3}\s+(.+)', content, re.MULTILINE)
    q_count = 0
    for h in headings:
        h_stripped = h.strip()
        for qw in question_words:
            if h_stripped.lower().startswith(qw.lower()):
                q_count += 1
                break
        else:
            for bq in bengali_q_words:
                if h_stripped.startswith(bq):
                    q_count += 1
                    break
    
    check_d_flag = "PASS" if q_count >= 2 else f"FAIL (count={q_count})"
    
    # ---------- Check E: Internal Links ----------
    # Count Markdown links to internal paths
    internal_links = re.findall(r'\]\((/[^)]*)\)', content)
    # Filter meaningful internal links (not /, /#, /images, /files, etc.)
    skip_prefixes = ('/#', '/images/', '/files/', '/assets/', '/fonts/', '/css/', '/js/')
    meaningful_links = []
    for link in internal_links:
        path = link
        if path == '/' or path.startswith(skip_prefixes):
            continue
        meaningful_links.append(path)
    link_count = len(meaningful_links)
    
    check_e_flag = "PASS" if link_count >= 3 else f"FAIL (count={link_count})"
    
    # ---------- Check F: Schema ----------
    schema_missing = []
    if not title:
        schema_missing.append("title")
    if not excerpt:
        schema_missing.append("excerpt")
    if not date_val:
        schema_missing.append("date")
    
    check_f_flag = "PASS" if not schema_missing else f"FAIL (missing: {', '.join(schema_missing)})"
    
    results.append((slug, title, date_val, excerpt, tags, content, 
                    {"A": check_a_flag, "B": check_b_flag, "C": check_c_flag, 
                     "D": check_d_flag, "E": check_e_flag, "F": check_f_flag,
                     "kw": primary_kw, "kw_count": kw_count,
                     "q_count": q_count, "link_count": link_count,
                     "pillar_count": pillar_count, "meaningful_links": meaningful_links},
                    {"entities": entities, "missing_entities": missing_entities,
                     "pillar_links": pillar_links}))

# Print results table
print("\n" + "="*190)
print(f"{'Slug':<48} {'A (TF-IDF)':<22} {'B (Entities)':<30} {'C (Pillar)':<25} {'D (AEO/GEO)':<20} {'E (Int.Links)':<22} {'F (Schema)':<20}")
print("="*190)

for slug, title, date_val, excerpt, tags, content, flags, extra in results:
    if slug == "NOT FOUND":
        print(f"{'NOT FOUND':<48} {'N/A':<22} {'N/A':<30} {'N/A':<25} {'N/A':<20} {'N/A':<22} {'N/A':<20}")
        continue
    
    a = flags["A"]
    b = flags["B"]
    c = flags["C"]
    d = flags["D"]
    e = flags["E"]
    f = flags["F"]
    
    print(f"{slug:<48} {a:<22} {b:<30} {c:<25} {d:<20} {e:<22} {f:<20}")

print("\n\n========== DETAILED RESULTS ==========\n")
for slug, title, date_val, excerpt, tags, content, flags, extra in results:
    if slug == "NOT FOUND":
        print(f"\n--- {slug} --- NOT FOUND")
        continue
    
    print(f"\n--- {slug} ---")
    print(f"  Title: {title[:80]}...")
    print(f"  Date: {date_val}")
    print(f"  Excerpt: {excerpt[:80]}...")
    print(f"  Tags: {tags}")
    print(f"  Content length: {len(content)} chars")
    
    print(f"  Check A (TF-IDF): {flags['A']}")
    print(f"    Primary keyword: '{flags['kw']}'")
    print(f"    Occurrences: {flags['kw_count']}")
    
    print(f"  Check B (Entities): {flags['B']}")
    if extra['missing_entities']:
        print(f"    Missing: {extra['missing_entities']}")
    else:
        print(f"    All present")
    
    print(f"  Check C (Pillar): {flags['C']}")
    print(f"    Pillar links found: {flags['pillar_count']}")
    if extra['pillar_links']:
        for pl in extra['pillar_links']:
            print(f"      - {pl}")
    
    print(f"  Check D (AEO/GEO): {flags['D']}")
    print(f"    Question headings count: {flags['q_count']}")
    
    print(f"  Check E (Internal Links): {flags['E']}")
    print(f"    Internal links count: {flags['link_count']}")
    if flags['meaningful_links']:
        print(f"    Links: {flags['meaningful_links'][:10]}")
    
    print(f"  Check F (Schema): {flags['F']}")
    print(f"    title={bool(title)}, excerpt={bool(excerpt)}, date={bool(date_val)}")
