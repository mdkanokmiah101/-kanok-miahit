#!/usr/bin/env python3
"""Framework checker for kanokmiah.com.bd blog posts v3.
Parses data.js directly and runs all 6 framework checks on recently modified posts."""

import re
import sys

# ─── PARSING ───────────────────────────────────────────────────────────────────

def extract_post_object(data_js, slug):
    """Extract the full object text for a given slug."""
    slug_pattern = rf'''slug:\s*"{re.escape(slug)}"'''
    slug_match = re.search(slug_pattern, data_js)
    if not slug_match:
        return None
    pos = slug_match.start()
    depth = 0
    start_pos = None
    for i in range(pos, -1, -1):
        c = data_js[i]
        if c == '}': depth += 1
        elif c == '{':
            if depth == 0:
                start_pos = i
                break
            depth -= 1
    if start_pos is None:
        return None
    depth = 0
    end_pos = None
    for i in range(start_pos, len(data_js)):
        c = data_js[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end_pos = i + 1
                break
    if end_pos is None:
        return None
    return {'text': data_js[start_pos:end_pos], 'start': start_pos, 'end': end_pos}


def extract_field_from_obj(obj_text, field_name):
    """Extract a simple string field value."""
    m = re.search(rf'{field_name}:\s*"([^"]*?)"', obj_text)
    if m:
        return m.group(1)
    m = re.search(rf'{field_name}:\s*\n\s*"([^"]*?)"', obj_text)
    if m:
        return m.group(1)
    return ''


def extract_tags_from_obj(obj_text):
    """Extract tags array."""
    m = re.search(r'tags:\s*\[(.*?)\]', obj_text, re.DOTALL)
    if not m:
        return []
    return re.findall(r'"([^"]*?)"', m.group(1))


def extract_content_from_obj(obj_text):
    """Extract content template literal."""
    m = re.search(r'content:\s*\n?\s*`', obj_text)
    if not m:
        return ''
    start_idx = m.end()
    for i in range(start_idx, len(obj_text)):
        if obj_text[i] == '`' and (i == 0 or obj_text[i-1] != '\\'):
            return obj_text[start_idx:i]
    return ''


# ─── HELPERS ───────────────────────────────────────────────────────────────────

STOP_WORDS = {
    'how','what','why','when','where','the','a','an','to','for',
    'of','in','is','are','do','does','and','or','but','vs','your',
    'that','this','with','from','best','top','guide','tips','check',
    'things','expert','need','get','make','more','its','all','new',
    'than','been','has','had','can','will','not','just','also','very',
    'should','about','which','who','whom','while','why','much','many',
    'some','any','each','every','their','them','they','our','its',
    'been','being','have','has','had','having','do','does','did',
    'doing','would','could','shall','should','may','might','must',
    'shall','let','one','two','three','really','actually','always',
    'never','often','usually','here','there','up','down','out',
    'over','under','again','further','then','once',
}

VERB_WORDS = {'choose','hire','pick','find','get','make','use','take',
    'give','show','know','need','help','learn','start','build','create',
    'grow','increase','improve','optimize','boost','drive','scale',
    'achieve','deliver','offer','provide','become','work','run','set'}

TOPIC_WORDS = {'seo','expert','agency','dhaka','bangladesh','guide',
    'service','services','marketing','digital','business','businesses',
    'case','study','mistakes','traffic','roi','paid','ads','ranking',
    'rankings','google','search','local','technical','ecommerce','content',
    'link','building','mobile','keyword','research','strategy','optimization',
    'checklist','tips','tricks','audit','analytics','report','reports',
    'growth','results','lead','leads','conversion','sales','revenue',
    'profit','cost','price','package','packages','plan','plans','website',
    'web','online','social','media','facebook','instagram','youtube',
    'shopify','daraz','watch','locksmith','dundee','scotland','expert'}

DOMAIN = 'kanokmiah.com.bd'


def extract_primary_keyword(title):
    """Extract primary keyword from title (first meaningful noun/topic phrase)."""
    clean = title.split(':')[0].strip()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    words = clean.split()

    # Strategy 1: Find first TOPIC_WORDS match (nouns/entities)
    for i, w in enumerate(words):
        wl = w.lower()
        if wl in TOPIC_WORDS and len(wl) >= 2:
            phrase = wl
            if i + 1 < len(words):
                nwl = words[i+1].lower()
                if nwl in TOPIC_WORDS or (nwl not in STOP_WORDS and nwl not in VERB_WORDS and len(nwl) >= 3):
                    phrase += ' ' + nwl
            return phrase

    # Strategy 2: First non-stop, non-verb word >=3 chars
    for i, w in enumerate(words):
        wl = w.lower()
        if wl not in STOP_WORDS and wl not in VERB_WORDS and len(wl) >= 3:
            phrase = wl
            if i + 1 < len(words):
                nwl = words[i+1].lower()
                if nwl not in STOP_WORDS and nwl not in VERB_WORDS and len(nwl) >= 3:
                    phrase += ' ' + nwl
            return phrase

    # Strategy 3: First non-stop word
    for w in words:
        wl = w.lower()
        if wl not in STOP_WORDS:
            return wl

    return words[0].lower() if words else title.lower()


def count_occurrences(text, keyword):
    """Count case-insensitive occurrences."""
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), text, re.IGNORECASE))


def count_question_headings(text):
    """Count headings starting with question words."""
    return len(re.findall(
        r'\n#{1,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b',
        text, re.IGNORECASE))


def count_internal_links(content):
    """Count internal links (relative or absolute to the domain)."""
    rel = re.findall(r'\]\(/(?:blog|industries|services|case-studies|about|contact|faq|#)', content)
    abs_links = re.findall(rf'\]\(https?://(?:www\.)?{re.escape(DOMAIN)}[^)]*\)', content)
    bare = re.findall(rf'\]\({re.escape(DOMAIN)}[^)]*\)', content)
    return len(rel) + len(abs_links) + len(bare)


PILLAR_MAP = [
    ('seo guide', 'Complete SEO Guide', '/blog/complete-seo-guide-bangladesh-businesses-2026'),
    ('local seo', 'Local SEO Guide', '/blog/local-seo-dhaka-google-maps-ranking'),
    ('technical seo', 'Technical SEO Guide', '/blog/technical-seo-checklist-bangladeshi-websites'),
    ('google business', 'Google Business Profile Guide', '/blog/google-business-profile-optimization-guide-bangladesh'),
    ('ecommerce', 'E-commerce SEO Guide', '/blog/ecommerce-seo-daraz-shopify-guide'),
    ('link building', 'Link Building Guide', '/blog/link-building-bangladesh-strategies'),
    ('content marketing', 'Content Marketing Guide', '/blog/content-marketing-seo-friendly-content-writing'),
    ('mobile seo', 'Mobile SEO Guide', '/blog/mobile-seo-bangladesh-ranking-strategy'),
    ('keyword research', 'Keyword Research Guide', '/blog/keyword-research-bangladesh-market'),
    ('geo', 'GEO/AI Search Guide', '/blog/geo-optimization-prepare-business-ai-search'),
    ('ai search', 'GEO/AI Search Guide', '/blog/geo-optimization-prepare-business-ai-search'),
    ('schema', 'Schema Markup Guide', '/blog/schema-markup-rich-snippets-techniques'),
    ('international seo', 'International SEO Guide', '/blog/international-seo-bangladesh-exporters-global-buyers'),
]


def check_pillar_link(content, tags):
    """Check if post links to any pillar page."""
    tags_lower = [t.lower() for t in tags]
    norm_content = content.replace('https://www.kanokmiah.com.bd', '').replace('https://kanokmiah.com.bd', '')
    norm_content = norm_content.replace('http://www.kanokmiah.com.bd', '')

    linked_pillars = []
    for keyword, pillar, url in PILLAR_MAP:
        if url in norm_content:
            linked_pillars.append((pillar, url))

    relevant_pillar = None
    relevant_pillar_url = None
    for keyword, pillar, url in PILLAR_MAP:
        if any(keyword in t for t in tags_lower):
            relevant_pillar = pillar
            relevant_pillar_url = url
            break

    if linked_pillars:
        return {'linked': True, 'pillar': linked_pillars[0][0], 'url': linked_pillars[0][1]}
    if relevant_pillar:
        return {'linked': False, 'pillar': relevant_pillar, 'url': relevant_pillar_url}
    return {'linked': False, 'pillar': 'Unknown', 'url': ''}


def check_entities(title, content, tags):
    """Check semantic entity coverage."""
    content_lower = content.lower()
    title_lower = title.lower()
    tags_lower = [t.lower() for t in tags]
    missing = []

    needs_dhaka = 'dhaka' in title_lower or any('dhaka' in t for t in tags_lower)
    needs_bangladesh = 'bangladesh' in title_lower or any('bangladesh' in t for t in tags_lower)

    if needs_dhaka and 'dhaka' not in content_lower:
        missing.append('Dhaka')
    if needs_bangladesh and 'bangladesh' not in content_lower:
        missing.append('Bangladesh')

    if any('case study' in t for t in tags_lower):
        if 'case study' not in content_lower:
            missing.append('"Case Study" keyword')

    return missing


# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    with open('src/app/blog/data.js', 'r') as f:
        data_js = f.read()

    target_slugs = [
        'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
        'locksmith-dundee-seo-case-study',
        'how-to-choose-best-seo-expert-dhaka-15-things',
        'seo-expert-vs-seo-agency-dhaka-which-is-right',
        'top-10-seo-mistakes-dhaka-businesses-fix',
        'what-does-seo-expert-do-guide-business-owners',
        'seo-case-study-dhaka-businesses-increased-organic-traffic',
        'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
        'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
        'watchzonebd-seo-case-study',
    ]

    print("# Content Framework Report — kanokmiah.com.bd")
    print(f"**Generated:** 2026-07-15")
    print(f"**Scope:** {len(target_slugs)} posts (new + modified in last 48h)")
    print()

    all_passed = True

    for slug in target_slugs:
        obj = extract_post_object(data_js, slug)
        if not obj:
            print(f"## Post: {slug}")
            print("⚠️  Could not parse post object\n")
            all_passed = False
            continue

        obj_text = obj['text']
        title = extract_field_from_obj(obj_text, 'title')
        excerpt = extract_field_from_obj(obj_text, 'excerpt')
        date = extract_field_from_obj(obj_text, 'date')
        tags = extract_tags_from_obj(obj_text)
        content = extract_content_from_obj(obj_text)

        print(f"## Post: `{slug}`")
        print(f"**Title:** {title}")
        print()
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")

        # A. TF-IDF Coverage
        keyword = extract_primary_keyword(title)
        occurrences = count_occurrences(content, keyword)
        tfidf_pass = occurrences >= 5
        if not tfidf_pass:
            all_passed = False
        print(f"| **TF-IDF:** `{keyword}` | {'✅' if tfidf_pass else '❌'} | {occurrences} occurrences in content (need ≥5) |")

        # B. Entities
        missing_entities = check_entities(title, content, tags)
        entity_pass = len(missing_entities) == 0
        if not entity_pass:
            all_passed = False
        detail = "All required entities present" if entity_pass else f"Missing: {', '.join(missing_entities)}"
        print(f"| **Entities** | {'✅' if entity_pass else '❌'} | {detail} |")

        # C. Pillar Link
        pillar_info = check_pillar_link(content, tags)
        if pillar_info['linked']:
            print(f"| **Pillar Link** | ✅ | Links to pillar: [{pillar_info['pillar']}]({pillar_info['url']}) |")
        else:
            all_passed = False
            if pillar_info['pillar'] != 'Unknown':
                print(f"| **Pillar Link** | ❌ | No link to pillar page — add link to [{pillar_info['pillar']}]({pillar_info['url']}) |")
            else:
                print(f"| **Pillar Link** | ❌ | No matching pillar topic found from tags |")

        # D. AEO/GEO
        question_headings = count_question_headings(content)
        aeo_pass = question_headings >= 2
        if not aeo_pass:
            all_passed = False
        print(f"| **AEO/GEO** | {'✅' if aeo_pass else '❌'} | {question_headings} question-based headings (need ≥2) |")

        # E. Internal Links
        internal_links = count_internal_links(content)
        link_pass = internal_links >= 3
        if not link_pass:
            all_passed = False
        print(f"| **Internal Links** | {'✅' if link_pass else '❌'} | {internal_links} internal links to posts/services/locations (need ≥3) |")

        # F. Schema
        title_ok = bool(title and len(title) > 0)
        excerpt_ok = bool(excerpt and len(excerpt) > 0)
        date_ok = bool(date and len(date) > 0)
        schema_all = title_ok and excerpt_ok and date_ok
        if not schema_all:
            all_passed = False
        schema_detail = f"Title: {'✅' if title_ok else '❌'}, Excerpt: {'✅' if excerpt_ok else '❌'}, Date: {'✅' if date_ok else '❌'}"
        print(f"| **Schema Ready** | {'✅' if schema_all else '❌'} | {schema_detail} |")

        # Fix instructions
        fixes = []
        if not tfidf_pass:
            fixes.append(f"- **TF-IDF:** Boost `{keyword}` from {occurrences} to ≥5 occurrences in headings/content")
        if not entity_pass:
            fixes.append(f"- **Entities:** Insert missing: {', '.join(missing_entities)}")
        if not pillar_info['linked'] and pillar_info['pillar'] != 'Unknown':
            fixes.append(f"- **Pillar:** Add link to [{pillar_info['pillar']}]({pillar_info['url']})")
        if not aeo_pass:
            fixes.append(f"- **AEO/GEO:** Add ≥2 question headings (How/What/Why…), currently {question_headings}")
        if not link_pass:
            fixes.append(f"- **Internal Links:** Add ≥3 internal links to posts/services, currently {internal_links}")
        if not schema_all:
            missing_f = [f for f, ok in [('title', title_ok), ('excerpt', excerpt_ok), ('date', date_ok)] if not ok]
            fixes.append(f"- **Schema:** Set missing fields: {', '.join(missing_f)}")

        if fixes:
            print()
            print("### Fix instructions:")
            for f in fixes:
                print(f)

        print()

    print("---")
    print("## Overall Result")
    if all_passed:
        print("✅ **ALL CHECKS PASSED** — Content framework fully compliant.")
    else:
        print("⚠️  **SOME CHECKS FAILED** — See per-post details above for fixes.")
    print()


if __name__ == '__main__':
    main()
