#!/usr/bin/env python3
"""
Analyze Semantic Entities & AEO/GEO for ALL blog posts in data.js
Computes entity_count, question_headings, geo_ready, entity_density, etc.
"""

import re
import sys
import math

# ─── Named entity lists ──────────────────────────────────────────────
BANGLADESHI_CITIES = [
    'Dhaka', 'Chittagong', 'Sylhet', 'Khulna', 'Rajshahi', 'Barisal',
    'Rangpur', 'Mymensingh', 'Bogura', 'Comilla', 'Gazipur', 'Narayanganj',
    'Gulshan', 'Banani', 'Dhanmondi', 'Uttara', 'Motijheel', 'Mirpur',
    'Bashundhara', 'Mohakhali', 'Farmgate', 'Tejgaon', 'Shahbagh',
    'Old Dhaka', 'Kakrail', 'Paltan', 'Kawran Bazar', 'Niketan',
    'Baridhara', 'Badda', 'Rampura', 'Malibagh', 'Shyamoli', 'Savar',
    'Tongi', 'Kaptai', 'Cox\'s Bazar', "Cox's Bazar",
    # Bengali names
    'ঢাকা', 'চট্টগ্রাম', 'সিলেট', 'খুলনা', 'রাজশাহী', 'বরিশাল',
    'রংপুর', 'ময়মনসিংহ', 'বগুড়া', 'কুমিল্লা', 'গাজীপুর', 'নারায়ণগঞ্জ',
    'গুলশান', 'বনানী', 'ধানমন্ডি', 'উত্তরা', 'মতিঝিল', 'মিরপুর',
]

COMPANIES_ORGS = [
    'Google', 'Facebook', 'YouTube', 'Daraz', 'Shopify', 'Amazon',
    'Apple', 'Microsoft', 'Twitter', 'LinkedIn', 'Instagram', 'WhatsApp',
    'YouTube', 'WordPress', 'WooCommerce', 'Ahrefs', 'SEMrush', 'Moz',
    'Cloudflare', 'Shopify', 'BigCommerce', 'Wix', 'Squarespace',
    'HubSpot', 'Mailchimp', 'Canva', 'Adobe', 'TikTok', 'Snapchat',
    'Pinterest', 'Reddit', 'Quora', 'Medium', 'Upwork', 'Fiverr',
    'Freelancer', 'Bdjobs', 'The Daily Star', 'Dhaka Tribune',
    'Prothom Alo', 'BDNews24', 'DataReportal', 'StatCounter',
    'SimilarWeb', 'CommonFloor', 'Bikroy', 'Evaly', 'Chaldal',
    'Pathao', 'Uber', 'Foodpanda', 'HungryNaki',
    'SHEIN', 'Alibaba', 'AliExpress', 'Spider', 'Robi',
    'Grameenphone', 'Banglalink', 'Airtel', 'Teletalk',
    'Nagad', 'bKash', 'Rocket', 'iPay', 'SSLCOMMERZ',
    'Shohoz', 'Busbd', 'YouTube', 'Yandex', 'DuckDuckGo',
]

TECHNOLOGIES = [
    'ChatGPT', 'Bing', 'Gemini', 'Perplexity', 'Claude', 'Copilot',
    'Google SGE', 'Search Generative Experience', 'AI Overview',
    'BERT', 'MUM', 'RankBrain', 'NLP', 'Natural Language Processing',
    'GPT', 'LLM', 'GEO', 'Generative Engine Optimization',
    'AEO', 'Answer Engine Optimization',
    'Schema', 'JSON-LD', 'Structured Data', 'Rich Snippets',
    'Core Web Vitals', 'LCP', 'INP', 'CLS', 'PageSpeed',
    'AMP', 'PWA', 'SPA', 'SSR', 'CSR', 'CDN', 'DNS', 'HTTPS',
    'SEO', 'EEAT', 'E-E-A-T',
    'Hreflang', 'Canonical', 'Robots.txt', 'Sitemap',
    'Google Analytics', 'Google Search Console', 'Google Tag Manager',
    'Google Business Profile', 'GBP', 'Google Maps',
    'Facebook', 'Instagram', 'Twitter', 'YouTube',
    'Ahrefs', 'SEMrush', 'Moz', 'Screaming Frog',
    'Yoast', 'Rank Math', 'All in One SEO',
    'Python', 'JavaScript', 'PHP', 'HTML', 'CSS', 'React', 'Node.js',
    'MySQL', 'PostgreSQL', 'Linux', 'Apache', 'Nginx',
    'TensorFlow', 'PyTorch', 'Hugging Face',
    'OpenAI', 'DeepMind', 'Anthropic', 'Meta AI',
    'RankBrain', 'MUM', 'BERT', 'LaMDA', 'PaLM',
    'LSI', 'Latent Semantic Indexing',
    'AI', 'Machine Learning', 'Deep Learning', 'ML',
]

PEOPLE = [
    'Kanok Miah', 'Md Kanok Miah', 'Kanok', 'Miah',
    'কানক মিয়া', 'Kanok Miah',
]

COUNTRIES = ['Bangladesh', 'Bangladeshi', 'বাংলাদেশ']

# All entities combined for lookup
ALL_ENTITIES = list(set(
    [c.lower() for c in BANGLADESHI_CITIES] +
    [c.lower() for c in COMPANIES_ORGS] +
    [t.lower() for t in TECHNOLOGIES] +
    [p.lower() for p in PEOPLE] +
    [c.lower() for c in COUNTRIES]
))

# Sort by length descending to match longer entities first
ALL_ENTITIES.sort(key=len, reverse=True)


def extract_posts(filepath):
    """Extract all blog posts from the JS file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    posts = []
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Find slug line
        slug_match = re.match(r'^\s+slug:\s+"([^"]+)"', line)
        if not slug_match:
            i += 1
            continue

        slug = slug_match.group(1)

        # Now find the content: ` line
        content_start = -1
        for j in range(i, min(i + 100, len(lines))):
            if 'content: `' in lines[j]:
                content_start = j
                break

        if content_start == -1:
            i += 1
            continue

        # Extract content between backticks
        # The content starts after `content: ` and after the opening backtick
        raw_content = ''
        # Find the position of the opening backtick
        open_line = lines[content_start]
        bt_pos = open_line.find('`')
        if bt_pos == -1:
            i += 1
            continue

        # Content starts after the first backtick
        rest_of_line = open_line[bt_pos + 1:]
        if rest_of_line:
            raw_content += rest_of_line + '\n'

        # Now find the closing backtick
        k = content_start + 1
        while k < len(lines):
            l = lines[k]
            # The closing backtick is the first unescaped backtick
            # We need to handle escaped backticks within the content
            # But for simplicity, find the first line with a backtick (not preceded by \)
            # Actually, escaped backticks are \\` so let's just find ` that's not preceded by \
            bt_idx = -1
            for idx, ch in enumerate(l):
                if ch == '`' and (idx == 0 or l[idx-1] != '\\'):
                    bt_idx = idx
                    break

            if bt_idx != -1:
                # This is the closing backtick
                # Content before the backtick belongs to the post
                before_bt = l[:bt_idx]
                if before_bt:
                    raw_content += before_bt
                break
            else:
                raw_content += l + '\n'
            k += 1

        posts.append({
            'slug': slug,
            'content': raw_content,
            'start_line': i,
            'end_line': k,
        })
        i = k + 1

    return posts


def count_words(text):
    """Count words in text."""
    return len(text.split())


def extract_headings(content):
    """Extract all H2 (##) and H3 (###) headings from markdown content."""
    headings = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('## '):
            headings.append(('h2', stripped[3:].strip()))
        elif stripped.startswith('### '):
            headings.append(('h3', stripped[4:].strip()))
    return headings


def is_question_heading(heading_text):
    """Check if a heading is phrased as a question."""
    text = heading_text.strip()
    if '?' in text:
        return True
    # Check if it starts with question words
    question_starters = [
        'how', 'what', 'why', 'where', 'when', 'who', 'which',
        'can', 'is', 'are', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'has', 'have', 'had', 'was', 'were',
        'আছে', 'কি', 'কিভাবে', 'কেন', 'কখন', 'কোথায়', 'কে', 'কোন',
        'কেমন', 'কত', 'কী', 'কার', 'কারা',
    ]
    first_word = text.split()[0].lower().strip('"\'«»')
    for qs in question_starters:
        if first_word == qs:
            return True
    return False


def count_entities(text):
    """Count unique named entities found in text."""
    text_lower = text.lower()
    found = set()
    for entity in ALL_ENTITIES:
        if entity in text_lower:
            found.add(entity)
    return len(found)


def check_geo_ready(content):
    """Determine if content has conversational phrasing, FAQ, QA format suitable for AI search."""
    text = content.lower()
    geo_signals = 0

    # FAQ sections (### FAQ, ## FAQ, FAQ schema, etc.)
    if re.search(r'(?i)(###\s*faq|##\s*faq|faq\s*section|frequently asked|people also ask)', text):
        geo_signals += 2

    # Question headings (with ?)
    headings = extract_headings(content)
    q_headings = [h for h in headings if '?' in h[1]]
    if q_headings:
        geo_signals += 2

    # Question-answer pairs
    qa_patterns = re.findall(r'(?m)^\*\*(.*?\?)\*\*\s*\n(.*?)$', text)
    if qa_patterns:
        geo_signals += 2

    # Conversational phrases
    conv_phrases = [
        'you might wonder', 'you may ask', 'common questions',
        'let me explain', 'here\'s how', 'this means that',
        'in simple terms', 'think of it as', 'for example',
        'conversational', 'natural language', 'voice search',
    ]
    for phrase in conv_phrases:
        if phrase in text:
            geo_signals += 0.5
            break

    # Schema markup mention
    if re.search(r'(?i)(faq\s*schema|qa\s*page|question\s*schema|howto\s*schema)', text):
        geo_signals += 1

    # Tables with Q&A format
    if re.search(r'(?i)(question|answer)\s*\|', text):
        geo_signals += 1.5

    return 'YES' if geo_signals >= 2 else 'NO'


def main():
    filepath = '/root/kanok-miahit/src/app/blog/data.js'
    print(f"Parsing {filepath}...", file=sys.stderr)
    
    posts = extract_posts(filepath)
    print(f"Extracted {len(posts)} posts", file=sys.stderr)

    # Print header
    header = 'slug|entity_count|question_headings|geo_ready|entity_density|geo_opportunity|entity_gap'
    print(header)

    geo_opp_posts = []
    entity_gap_posts = []

    for post in posts:
        slug = post['slug']
        content = post['content']

        word_count = count_words(content)
        if word_count == 0:
            word_count = 1  # Avoid division by zero

        headings = extract_headings(content)
        question_headings = sum(1 for h in headings if is_question_heading(h[1]))

        entity_count = count_entities(content)
        entity_density = round((entity_count / word_count) * 100, 2)

        geo_ready = check_geo_ready(content)

        geo_opportunity = 'YES' if question_headings == 0 else 'NO'
        entity_gap = 'YES' if entity_density < 1.0 else 'NO'

        if geo_opportunity == 'YES':
            geo_opp_posts.append(slug)
        if entity_gap == 'YES':
            entity_gap_posts.append(slug)

        print(f"{slug}|{entity_count}|{question_headings}|{geo_ready}|{entity_density}|{geo_opportunity}|{entity_gap}")

    # Summary stats to stderr
    total = len(posts)
    with_questions = sum(1 for p in posts if sum(1 for h in extract_headings(p['content']) if is_question_heading(h[1])) > 0)
    geo_ready_count = sum(1 for p in posts if check_geo_ready(p['content']) == 'YES')
    entity_gap_count = sum(1 for p in posts if count_entities(p['content']) / max(count_words(p['content']), 1) * 100 < 1.0)
    
    print(file=sys.stderr)
    print(f"Total posts analyzed: {total}", file=sys.stderr)
    print(f"Posts with question headings: {with_questions}", file=sys.stderr)
    print(f"Posts without question headings (GEO opportunity): {len(geo_opp_posts)}", file=sys.stderr)
    print(f"Posts with entity gap (density < 1.0): {entity_gap_count}", file=sys.stderr)
    print(f"Posts geo_ready: {geo_ready_count}", file=sys.stderr)
    print(file=sys.stderr)
    print(f"GEO opportunity posts ({len(geo_opp_posts)}):", file=sys.stderr)
    for s in geo_opp_posts:
        print(f"  {s}", file=sys.stderr)
    print(file=sys.stderr)
    print(f"Entity gap posts ({entity_gap_count}):", file=sys.stderr)
    for s in entity_gap_posts:
        print(f"  {s}", file=sys.stderr)


if __name__ == '__main__':
    main()
