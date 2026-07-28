#!/usr/bin/env python3
"""Run framework checks A (TF-IDF keyword count), E (internal links), F (schema fields) on blog posts."""

import re
import json

# Read the data file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

# Extract the posts array
# Find the posts array content
match = re.search(r'const posts = \[(.*)\];\s*export default posts;', content, re.DOTALL)
if not match:
    print("ERROR: Could not find posts array")
    exit(1)

posts_text = match.group(1)

# Parse individual post objects - split by lines starting with "  {"
# We'll use a state machine approach
posts_raw = []
depth = 0
current = []
in_string = False
string_char = None
in_template = False

for char in posts_text:
    if char == '`' and not in_string:
        in_template = not in_template
    if not in_template:
        if char in ('"', "'") and not in_string:
            in_string = True
            string_char = char
        elif in_string and char == string_char:
            in_string = False
    
    if not in_template and not in_string:
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
    
    current.append(char)
    
    if not in_template and not in_string and depth == 0 and char == '}':
        posts_raw.append(''.join(current))
        current = []

# Map of slugs we care about
target_slugs = [
    "locksmith-dundee-seo-case-study",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "watchzonebd-seo-case-study",
]

def extract_field(post_text, field):
    """Extract a field value from a post object text."""
    # Match field: "value" or field:\n    "value"
    patterns = [
        rf'{field}:\s*"([^"]*)"',
        rf'{field}:\s*\'([^\']*)\'',
        rf"{field}:\s*`([^`]*)`",
    ]
    for p in patterns:
        m = re.search(p, post_text)
        if m:
            return m.group(1)
    return None

def extract_content(post_text):
    """Extract the content field (template literal)."""
    m = re.search(r'content:\s*`((?:[^`]|\\`)*)`', post_text, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def count_keyword(content, keyword):
    """Count occurrences of a keyword (case-insensitive)."""
    if not content or not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

def find_internal_links(content):
    """Find all internal links in the content."""
    if not content:
        return []
    # Internal links start with / (site-relative) or contain kanokmiah.com.bd
    links = []
    # Match markdown links: [text](/path) or [text](https://kanokmiah.com.bd/path)
    md_links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    for text, url in md_links:
        if url.startswith('/') or 'kanokmiah.com.bd' in url:
            links.append((text, url))
    return links

def check_schema_mentions(content):
    """Check if the content mentions schema markup types."""
    if not content:
        return []
    schema_types = [
        "LocalBusiness schema", "Organization schema", "Article schema",
        "FAQ schema", "Product schema", "Review schema", "Breadcrumb schema",
        "HowTo schema", "Service schema", "schema markup", "Schema.org",
        "structured data", "JSON-LD", "schema markup"
    ]
    found = []
    for st in schema_types:
        if st.lower() in content.lower():
            found.append(st)
    return found

# Now let's manually extract each post since the template literals cause parsing issues
# We'll use line-based extraction based on known line numbers

posts_line_ranges = {
    "locksmith-dundee-seo-case-study": (24681, 24879),
    "how-to-choose-best-seo-expert-dhaka-15-things": (25417, 25619),
    "seo-expert-vs-seo-agency-dhaka-which-is-right": (25622, 25849),
    "top-10-seo-mistakes-dhaka-businesses-fix": (25852, 26046),
    "what-does-seo-expert-do-guide-business-owners": (26051, 26389),
    "seo-case-study-dhaka-businesses-increased-organic-traffic": (26392, 26718),
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": (26721, 26997),
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": (27001, 27289),
    "watchzonebd-seo-case-study": (27292, 27510),
}

lines = content.split('\n')

def get_post_text(start_line, end_line):
    """Get the raw text of a post from line numbers (1-indexed)."""
    return '\n'.join(lines[start_line-1:end_line])

def get_slug(post_text):
    m = re.search(r'slug:\s*"([^"]*)"', post_text)
    return m.group(1) if m else "unknown"

def get_title(post_text):
    m = re.search(r'title:\s*"([^"]*)"', post_text)
    if m:
        return m.group(1)
    m = re.search(r'title:\s*\n\s+"([^"]*)"', post_text)
    return m.group(1) if m else "unknown"

def get_content_text(post_text):
    """Extract the content template literal from a post."""
    m = re.search(r'content:\s*`((?:.|\n)*?)`,\s*\n', post_text, re.DOTALL)
    if m:
        return m.group(1)
    # Try to find the closing backtick
    idx = post_text.find('content:')
    if idx == -1:
        return ""
    rest = post_text[idx:]
    # Find the opening backtick
    start = rest.find('`')
    if start == -1:
        return ""
    rest = rest[start+1:]
    # Find the closing backtick (followed by , or end)
    # Need to handle nested backticks? No, JS template literals don't nest
    end = rest.rfind('`')
    if end == -1:
        return ""
    return rest[:end]

# Define primary keywords for each post
primary_keywords = {
    "locksmith-dundee-seo-case-study": "locksmith dundee",
    "how-to-choose-best-seo-expert-dhaka-15-things": "SEO expert in Dhaka",
    "seo-expert-vs-seo-agency-dhaka-which-is-right": "SEO expert",
    "top-10-seo-mistakes-dhaka-businesses-fix": "SEO mistakes",
    "what-does-seo-expert-do-guide-business-owners": "SEO expert",
    "seo-case-study-dhaka-businesses-increased-organic-traffic": "SEO case study",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": "SEO",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": "AI SEO",
    "watchzonebd-seo-case-study": "WatchZoneBD",
}

def count_internal_links(content):
    """Count internal links (starting with / or containing kanokmiah.com.bd)."""
    if not content:
        return 0, []
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    internal = []
    for text, url in links:
        if url.startswith('/') and not url.startswith('//'):
            internal.append((text, url))
    return len(internal), internal

def check_schema(content):
    """Check for schema/structured data mentions."""
    schema_terms = [
        'schema', 'structured data', 'JSON-LD', 'Schema.org',
        'schema markup', 'rich snippet', 'LocalBusiness',
        'Organization', 'Product schema', 'Review schema',
        'FAQ schema', 'Breadcrumb', 'HowTo'
    ]
    found = []
    for term in schema_terms:
        if term.lower() in content.lower():
            found.append(term)
    return found

print("=" * 120)
print(f"{'Slug':50s} {'Title':65s} {'Keyword Count':15s} {'Int Links':10s} {'Schema Found'}")
print("=" * 120)

results = []

for slug in target_slugs:
    start, end = posts_line_ranges[slug]
    post_text = get_post_text(start, end)
    post_slug = get_slug(post_text)
    post_title = get_title(post_text)
    content_text = get_content_text(post_text)
    
    # Check A: Keyword count
    keyword = primary_keywords.get(slug, slug.replace('-', ' '))
    kw_count = count_keyword(content_text, keyword)
    
    # Check E: Internal links
    int_count, int_links = count_internal_links(content_text)
    int_links_str = ', '.join([f"[{t}]({u})" for t, u in int_links[:5]])
    if len(int_links) > 5:
        int_links_str += f" ... (+{len(int_links)-5} more)"
    
    # Check F: Schema
    schema_found = check_schema(content_text)
    schema_str = ', '.join(schema_found[:5]) if schema_found else "NONE"
    if len(schema_found) > 5:
        schema_str += f" (+{len(schema_found)-5} more)"
    
    results.append((post_slug, post_title, kw_count, keyword, int_count, int_links_str, schema_str))

for slug, title, kw_count, kw, int_count, int_links_str, schema_str in results:
    short_title = title[:62] + ".." if len(title) > 64 else title
    print(f"{slug:50s} {short_title:65s} {kw} ({kw_count}){'':5s} {int_count:3d}  {schema_str}")
    
print()
print("=" * 120)
print("DETAILED RESULTS PER POST")
print("=" * 120)

for slug, title, kw_count, kw, int_count, int_links_str, schema_str in results:
    print(f"\n{'─'*80}")
    print(f"📄 {title}")
    print(f"   Slug: {slug}")
    print(f"   ├── [A] TF-IDF Keyword '{kw}': {kw_count} occurrences")
    print(f"   ├── [E] Internal links: {int_count}")
    if int_links_str:
        print(f"   │   Links: {int_links_str}")
    print(f"   └── [F] Schema mentions: {schema_str if schema_str else 'NONE'}")
