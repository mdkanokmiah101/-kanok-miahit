#!/usr/bin/env python3
"""Analyze a single blog post: landlord-certificates-seo-case-study"""
import re, json

# Read data.js
with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract full post object for the slug
slug = "landlord-certificates-seo-case-study"
pattern = r'slug:\s*"' + re.escape(slug) + r'"'

# Find post start (the opening { before slug)
# Strategy: find the slug, then find the content backtick, extract everything between
slug_match = re.search(pattern, js_content)
if not slug_match:
    print("ERROR: slug not found")
    exit(1)

slug_pos = slug_match.start()

# Go backwards to find post opening {
pre_content = js_content[:slug_pos]
# Find the last "  {" before the slug that's not inside a backtick
# Look for newline + spaces + {
brace_matches = list(re.finditer(r'\n\s*\{', pre_content))
post_start = brace_matches[-1].start() + 1  # +1 to skip newline

post_text = js_content[post_start:]

# Find content opening
content_open = re.search(r'content:\s*`', post_text)
content_start = content_open.end()
remaining = post_text[content_start:]

# Find closing backtick followed by comma/newline + }
end_match = re.search(r'`\s*(?://[^\n]*)?,?\s*\n\s*\}', remaining)
if not end_match:
    # try just the backtick
    end_match = re.search(r'`', remaining)
    
content_end = content_start + end_match.start()
raw_content = post_text[content_start:content_end]

# Extract fields
def extract_field(text, field):
    m = re.search(rf'{field}:\s*"((?:[^"\\]|\\.)*)"', text)
    return m.group(1) if m else ''

def extract_tags(text):
    m = re.search(r'tags:\s*\[([^\]]*)\]', text)
    if m:
        return re.findall(r'"([^"]*)"', m.group(1))
    return []

title = extract_field(post_text, 'title')
date_val = extract_field(post_text, 'date')
excerpt = extract_field(post_text, 'excerpt')
author = extract_field(post_text, 'author')
tags = extract_tags(post_text)

print(f"=== POST DATA ===")
print(f"Slug: {slug}")
print(f"Title: {title}")
print(f"Date: {date_val}")
print(f"Author: {author}")
print(f"Tags: {tags}")
print(f"Excerpt: {excerpt}")
print(f"Content length: {len(raw_content)} chars")
print()

print(f"=== FULL CONTENT ===")
print(raw_content)
print()

# ========== CHECK A: TF-IDF (Keyword Coverage) ==========
print(f"{'='*60}")
print(f"CHECK A: TF-IDF COVERAGE")
print(f"{'='*60}")

STOPWORDS = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'by', 'with', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'shall', 'can', 'need', 'dare',
    'ought', 'used', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
    'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my',
    'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours',
    'theirs', 'what', 'which', 'who', 'whom', 'whose', 'when', 'where',
    'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
    'so', 'than', 'too', 'very', 'just', 'because', 'as', 'until', 'while',
    'about', 'between', 'through', 'during', 'before', 'after', 'above',
    'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there'}

def extract_keyword(title):
    # Try parenthesized term first
    paren_match = re.search(r'\(([^)]+)\)', title)
    if paren_match:
        kw = paren_match.group(1).strip()
        first_word = kw.split()[0].lower() if kw.split() else ''
        is_abbreviation = (len(kw) <= 8 and kw.isupper() and kw.isalpha())
        is_number = bool(re.match(r'^[\d,.%+]', kw))
        is_conjunction = first_word in ('and', 'or', 'but', 'how', 'what', 'why', 'the', 'a', 'an')
        if (is_abbreviation or len(kw) > 2) and not is_number and not is_conjunction:
            return kw

    # Remove trailing parenthetical and subtitle after colon/dash for core keyword
    core = title.split(':')[0].split('—')[0].split('–')[0].strip()
    core = re.sub(r'\([^)]*\)', '', core).strip()
    # Remove common prefixes
    core = re.sub(r'^(Why|How|What|When|Where|Top\s+\d+|The|A|An)\s+', '', core, flags=re.IGNORECASE).strip()
    words = re.findall(r"[A-Za-z0-9\x80-\xFF']+", core)
    meaningful = [w for w in words if w.lower() not in STOPWORDS and len(w) > 2]
    if not meaningful:
        meaningful = [w for w in words if w.lower() not in STOPWORDS and len(w) > 1]
    if meaningful:
        return ' '.join(meaningful[:2])
    all_words = re.findall(r"[A-Za-z0-9\x80-\xFF']+", title)
    meaningful = [w for w in all_words if w.lower() not in STOPWORDS and len(w) > 1]
    return ' '.join(meaningful[:2]) if meaningful else title

def count_keyword_occurrences(keyword, content):
    if not keyword:
        return 0
    content_lower = content.lower()
    keyword_lower = keyword.lower()
    phrase_count = len(re.findall(re.escape(keyword_lower), content_lower))
    words = keyword_lower.split()
    word_counts = []
    for w in words:
        word_counts.append(len(re.findall(r'\b' + re.escape(w) + r'\b', content_lower)))
    if word_counts:
        min_word_count = min(word_counts)
        return max(phrase_count, min_word_count)
    return phrase_count

keyword = extract_keyword(title)
kw_count = count_keyword_occurrences(keyword, raw_content)

# Also check alternative keywords
alt_keywords = ["landlord certificates", "organic leads", "local SEO"]
alt_results = {}
for ak in alt_keywords:
    alt_results[ak] = count_keyword_occurrences(ak, raw_content)

print(f"Primary keyword: '{keyword}' -> {kw_count} occurrences")
for ak, cnt in alt_results.items():
    print(f"  Alt keyword '{ak}': {cnt} occurrences")
print(f"Result: {'✅ PASS' if kw_count >= 5 else '❌ FAIL'} (threshold: 5)")

# ========== CHECK B: Entities ==========
print()
print(f"{'='*60}")
print(f"CHECK B: ENTITIES COVERAGE")
print(f"{'='*60}")

entity_checks = {
    'SEO': r'\b[Ss][Ee][Oo]\b',
    'Local SEO': r'\blocal\s+seo\b',
    'Google Business Profile': r'Google\s*(Business\s*Profile|My\s*Business|GBP|Maps)',
    'Kanok Miah': r'Kanok\s+Miah',
    'UK': r'\bUK\b',
    'London/Manchester/Birmingham': r'\b(London|Manchester|Birmingham|Glasgow|Leeds|Liverpool)\b',
    'Organic Leads': r'\borganic\s+(leads?|traffic|visitors?)\b',
    'Landlord': r'\b[Ll]andlord[s]?\b',
    'Certificates': r'\b[Cc]ertificates?\b',
    'Case Study': r'\bcase\s+study\b',
    'Results/ROI': r'\b(increase|growth|traffic|result|revenue|rank|organic|monthly|leads)\b',
    'Property Safety': r'\b(property|safety|gas|EICR|EPC|PAT)\b',
}

entity_results = {}
for entity_name, pattern in entity_checks.items():
    found = bool(re.search(pattern, raw_content, re.IGNORECASE))
    entity_results[entity_name] = found
    print(f"  {entity_name}: {'✅' if found else '❌ MISSING'}")

missing_entities = [name for name, found in entity_results.items() if not found]
print(f"Missing entities: {missing_entities if missing_entities else 'None'}")
print(f"Result: {'✅ PASS' if not missing_entities else '❌ FAIL'}")

# ========== CHECK C: Pillar-Cluster ==========
print()
print(f"{'='*60}")
print(f"CHECK C: PILLAR-CLUSTER ALIGNMENT")
print(f"{'='*60}")

def determine_pillar(tags):
    tag_lower = [t.lower() for t in tags]
    if any('case study' in t.lower() for t in tags):
        return "Case Studies"
    if any('local seo' in t.lower() or 'gbp' in t.lower() or 'google maps' in t.lower() for t in tag_lower):
        return "Local SEO"
    if any('technical' in t.lower() for t in tag_lower):
        return "Technical SEO"
    if any('content' in t.lower() for t in tag_lower):
        return "Content Marketing"
    if any('seo' in t.lower() for t in tag_lower):
        return "SEO"
    return "General"

pillar = determine_pillar(tags)
print(f"Pillar determined: {pillar} (from tags: {tags})")

# Pillar pages to check
pillar_pages = {
    "Case Studies": [
        "/services/seo-case-studies",
        "/blog/seo-case-study-dhaka-businesses-increased-organic-traffic"
    ],
    "Local SEO": [
        "/services/local-seo",
        "/blog/local-seo-tips-dhaka-businesses-google-maps"
    ],
    "SEO": [
        "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "/services"
    ],
    "General": ["/blog", "/"],
}

pages_to_check = pillar_pages.get(pillar, ["/blog/"])
linked_pages = []
for page in pages_to_check:
    if page in raw_content:
        linked_pages.append(page)

print(f"Expected pillar pages: {pages_to_check}")
print(f"Linked to pillar: {linked_pages if linked_pages else 'None'}")
print(f"Result: {'✅ PASS' if linked_pages else '❌ FAIL'}")

# ========== CHECK D: AEO/GEO Optimization ==========
print()
print(f"{'='*60}")
print(f"CHECK D: AEO/GEO OPTIMIZATION")
print(f"{'='*60}")

QUESTION_WORDS = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are']

def count_question_headings(content):
    q_pattern = '|'.join(re.escape(w) for w in QUESTION_WORDS)
    pattern = re.compile(
        r'^#{1,6}\s+(?:' + q_pattern + r')\b',
        re.MULTILINE | re.IGNORECASE
    )
    return len(pattern.findall(content))

q_count = count_question_headings(raw_content)

# Also check for question marks in headings
question_mark_headings = len(re.findall(r'^#{1,6}\s+.*\?', raw_content, re.MULTILINE))

# Check for FAQ sections
has_faq = bool(re.search(r'\bFAQ\b', raw_content, re.IGNORECASE))

# Count all headings
heading_count = len(re.findall(r'^#{1,6}\s+', raw_content, re.MULTILINE))

print(f"Question-based headings (How/What/Why/etc): {q_count}")
print(f"Headings ending with '?': {question_mark_headings}")
print(f"Has FAQ section: {has_faq}")
print(f"Total headings: {heading_count}")

# List all headings
all_headings = re.findall(r'^#{1,6}\s+(.+)', raw_content, re.MULTILINE)
for h in all_headings:
    q_mark = " ❓" if '?' in h else ""
    question_start = any(h.strip().startswith(w + " ") or h.strip().startswith(w.lower() + " ") for w in QUESTION_WORDS)
    print(f"  {'🤔' if question_start else '  '} {h}{' ❓' if '?' in h else ''}")

print(f"Result: {'✅ PASS' if q_count >= 2 or question_mark_headings >= 2 else '❌ FAIL'} (threshold: 2 question headings)")

# ========== CHECK E: Internal Links ==========
print()
print(f"{'='*60}")
print(f"CHECK E: INTERNAL LINKING")
print(f"{'='*60}")

def count_internal_links(content):
    # Markdown links
    md_links = re.findall(
        r'\[([^\]]*)\]\((/blog/[^)]*|/services/[^)]*|/industries/[^)]*|/locations/[^)]*)\)',
        content
    )
    # Bare links
    bare_links = re.findall(
        r'(?<!\()(?:/blog/|/services/|/industries/|/locations/)[a-zA-Z0-9_-]+',
        content
    )
    all_links = set()
    for text, path in md_links:
        all_links.add(path)
    for link in bare_links:
        all_links.add(link)
    valid_links = {l for l in all_links if len(l) > 10}
    return len(valid_links), valid_links

link_count, links = count_internal_links(raw_content)
print(f"Internal links found: {link_count}")
for l in sorted(links):
    print(f"  - {l}")
print(f"Result: {'✅ PASS' if link_count >= 3 else '❌ FAIL'} (threshold: 3)")

# ========== CHECK F: Schema Readiness ==========
print()
print(f"{'='*60}")
print(f"CHECK F: SCHEMA READINESS")
print(f"{'='*60}")

schema_checks = {
    'title': bool(title),
    'excerpt': bool(excerpt),
    'date': bool(date_val),
    'author': bool(author),
    'tags': len(tags) > 0,
}

for field, present in schema_checks.items():
    print(f"  {field}: {'✅' if present else '❌ MISSING'}")

missing_schema = [f for f, p in schema_checks.items() if not p]
print(f"Missing schema fields: {missing_schema if missing_schema else 'None'}")
print(f"Result: {'✅ PASS' if not missing_schema else '❌ FAIL'}")

# ========== WORD COUNT & READABILITY ==========
print()
print(f"{'='*60}")
print(f"ADDITIONAL METRICS")
print(f"{'='*60}")

word_count = len(raw_content.split())
print(f"Word count: {word_count}")

# Count paragraphs
paragraphs = [p for p in raw_content.split('\n\n') if p.strip()]
print(f"Paragraphs: {len(paragraphs)}")

# Sentiment/analysis of key sections
print()
print("--- INTERNAL LINKS (all forms) ---")
# Full link extraction
all_md = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', raw_content)
for text, url in all_md:
    if url.startswith('/'):
        print(f"  Markdown: [{text}]({url})")
    elif url.startswith('http'):
        print(f"  External: [{text}]({url})")

print()
print("=== OVERALL SUMMARY ===")
flags = 0
if kw_count < 5: flags += 1
if missing_entities: flags += 1
if not linked_pages: flags += 1
if q_count < 2 and question_mark_headings < 2: flags += 1
if link_count < 3: flags += 1
if missing_schema: flags += 1

print(f"Total flags: {flags}/6")
if flags == 0:
    print("Status: ✅ PASS")
elif flags <= 2:
    print("Status: ⚠️  WARN")
else:
    print("Status: ❌ FAIL")
