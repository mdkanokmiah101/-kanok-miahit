#!/usr/bin/env python3
"""
Content Framework Checker for kanokmiah.com.bd blog posts.
Version 3 - Final with &/and normalization and cleaner output.
"""
import re

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

TARGET_SLUGS = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-bangladesh-ranking-strategy",
    "seo-career-guide-bangladesh-2026",
    "affiliate-seo-bangladesh",
    "seo-google-penalty-recovery-bd",
    "b2b-lead-generation-seo-bangladesh",
    "seo-for-fitness-gyms-bangladesh",
    "seo-healthcare-medical-clinics-bangladesh",
    "seo-educational-institutions-bangladesh",
    "seo-travel-tourism-bangladesh",
]


def read_data_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_posts(text):
    posts = []
    i = 0
    length = len(text)

    while i < length:
        m = re.compile(r'^\s*\{\s*$', re.MULTILINE).search(text, i)
        if not m:
            break

        obj_start = m.start()
        depth = 0
        in_backtick = False
        in_single_string = False
        in_double_string = False
        escaped = False

        j = obj_start
        while j < length:
            ch = text[j]
            if escaped:
                escaped = False
                j += 1
                continue
            if ch == '\\' and (in_backtick or in_single_string or in_double_string):
                escaped = True
                j += 1
                continue
            if in_backtick:
                if ch == '`':
                    in_backtick = False
            elif in_single_string:
                if ch == "'":
                    in_single_string = False
            elif in_double_string:
                if ch == '"':
                    in_double_string = False
            else:
                if ch == '`':
                    in_backtick = True
                elif ch == "'":
                    in_single_string = True
                elif ch == '"':
                    in_double_string = True
                elif ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        obj_end = j + 1
                        obj_text = text[obj_start:obj_end]
                        post = parse_post_object(obj_text)
                        if post and post.get('slug'):
                            posts.append(post)
                        i = obj_end
                        break
            j += 1
        else:
            i = obj_start + 1

    return posts


def parse_post_object(obj_text):
    post = {}
    m = re.search(r'slug:\s*"([^"]+)"', obj_text)
    if m: post['slug'] = m.group(1)
    m = re.search(r'title:\s*"([^"]+)"', obj_text)
    if m: post['title'] = m.group(1)
    m = re.search(r'date:\s*"([^"]+)"', obj_text)
    if m: post['date'] = m.group(1)
    m = re.search(r'author:\s*"([^"]+)"', obj_text)
    if m: post['author'] = m.group(1)
    m = re.search(r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', obj_text)
    if m: post['excerpt'] = m.group(1)
    m = re.search(r'tags:\s*\[([^\]]+)\]', obj_text)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]+)"', tags_str)
        post['tags'] = tags
    m = re.search(r'metaTitle:\s*"([^"]*)"', obj_text)
    if m: post['metaTitle'] = m.group(1)
    m = re.search(r'metaDescription:\s*"([^"]*)"', obj_text)
    if m: post['metaDescription'] = m.group(1)
    m = re.search(r'dateModified:\s*"([^"]+)"', obj_text)
    if m: post['dateModified'] = m.group(1)
    m = re.search(r'content:\s*`(.*)', obj_text, re.DOTALL)
    if m:
        after_content = m.group(1)
        close_idx = after_content.rfind('`')
        if close_idx >= 0:
            post['content'] = after_content[:close_idx]
    m = re.search(r'imagePlaceholder:\s*"([^"]+)"', obj_text)
    if m: post['imagePlaceholder'] = m.group(1)
    m = re.search(r'readTime:\s*"([^"]+)"', obj_text)
    if m: post['readTime'] = m.group(1)
    return post


def normalize_text(text):
    """Normalize & ↔ and for matching."""
    return text.replace(' & ', ' and ').replace(' &amp; ', ' and ')


def extract_primary_keyword(title):
    """
    Extract primary keyword from title (first meaningful noun phrase).
    """
    if not title:
        return None

    keyword = title.strip()
    # Split on separator, take first part
    for sep in [' — ', ' – ', ' - ', ': ', '|', '—', '–', ':']:
        parts = keyword.split(sep, 1)
        if len(parts) > 1 and len(parts[0]) > 3:
            keyword = parts[0].strip()
            break

    keyword = keyword.rstrip(',;.:!?')

    # For English, strip common prefixes/suffixes
    if not any('\u0980' <= c <= '\u09FF' for c in keyword):
        keyword = re.sub(r'\s+in\s+Bangladesh.*$', '', keyword, flags=re.IGNORECASE).strip()
        keyword = re.sub(r'\s+for\s+Bangladesh.*$', '', keyword, flags=re.IGNORECASE).strip()

        m = re.match(r'^(SEO|Complete|The|A|Your)\s+(for|in|of|to|Guide)\s+(.+)$', keyword, re.IGNORECASE)
        if m:
            keyword = m.group(3).strip()

        words = keyword.split()
        if len(words) > 5:
            keyword = ' '.join(words[:4])

    keyword = keyword.rstrip(',;.:!?& ')
    return keyword.strip() if keyword else None


# ─── CHECKS ─────────────────────────────────────────────────────────────────

def check_tfidf(title, content):
    if not title or not content:
        kw = extract_primary_keyword(title) if title else "N/A"
        return kw, "❌", "Missing title or content"

    keyword = extract_primary_keyword(title)
    if not keyword:
        return "N/A", "❌", "Could not extract keyword"

    # Normalize both for &/and equivalence
    kw_norm = normalize_text(keyword.lower())
    content_norm = normalize_text(content.lower())

    count = len(re.findall(re.escape(kw_norm), content_norm))

    if count >= 5:
        return keyword, "✅", f"{count} occurrences (normalized)"
    else:
        return keyword, "❌", f"{count} occurrences (need ≥5, normalized)"


def check_entities(title, content, tags):
    if not content:
        return "❌", "Missing content"

    missing_entities = []

    location_found = any([
        re.search(r'\bBangladesh\b', content, re.IGNORECASE),
        re.search(r'\bঢাকা\b', content),
        re.search(r'\bDhaka\b', content),
        re.search(r'বাংলাদেশ', content),
    ])
    if not location_found:
        missing_entities.append('Location (Bangladesh/Dhaka)')

    seo_found = any(re.search(p, content, re.IGNORECASE) for p in [
        r'\bSEO\b', r'\bGEO\b', r'\bsearch engine\b', r'\branking\b',
        r'\boptimization\b', r'এসইও', r'সার্চ ইঞ্জিন',
    ])
    if not seo_found:
        missing_entities.append('Service type (SEO/digital marketing)')

    if tags:
        for tag in tags:
            tl = tag.lower()
            if any(kw in tl for kw in ['garment', 'textile', 'rmg']):
                if not re.search(r'\bgarment|\btextile|\bRMG|\bapparel', content, re.IGNORECASE):
                    missing_entities.append(f'Industry: {tag}')
            elif 'b2b' in tl:
                if not re.search(r'\bB2B\b', content):
                    missing_entities.append(f'Entity: B2B')
            elif any(kw in tl for kw in ['health', 'medical', 'clinic', 'healthcare']):
                if not re.search(r'\bmedical|\bhealthcare|\bclinic|\bdoctor|\bhospital|চিকিৎসা', content, re.IGNORECASE):
                    missing_entities.append(f'Industry: {tag}')
            elif any(kw in tl for kw in ['education', 'school', 'educational', 'student', 'university']):
                if not re.search(r'\beducation|\bschool|\buniversity|\bcollege|শিক্ষা|বিদ্যালয়', content, re.IGNORECASE):
                    missing_entities.append(f'Industry: {tag}')
            elif any(kw in tl for kw in ['travel', 'tourism', 'tour', 'hospitality']):
                if not re.search(r'\btravel|\btourism|\btour|ভ্রমণ|পর্যটন', content, re.IGNORECASE):
                    missing_entities.append(f'Industry: {tag}')
            elif any(kw in tl for kw in ['fitness', 'gym']):
                if not re.search(r'\bfitness|\bgym|\bexercise|\bworkout|ফিটনেস', content, re.IGNORECASE):
                    missing_entities.append(f'Industry: {tag}')
            elif any(kw in tl for kw in ['mobile', 'মোবাইল']):
                if not re.search(r'\bmobile|মোবাইল', content, re.IGNORECASE):
                    missing_entities.append(f'Entity: Mobile')
            elif any(kw in tl for kw in ['career', 'job', 'ক্যারিয়ার', 'চাকরি']):
                if not re.search(r'\bcareer|\bjob|ক্যারিয়ার|চাকরি', content, re.IGNORECASE):
                    missing_entities.append(f'Entity: {tag}')
            elif any(kw in tl for kw in ['affiliate', 'অ্যাফিলিয়েট']):
                if not re.search(r'\baffiliate|অ্যাফিলিয়েট', content, re.IGNORECASE):
                    missing_entities.append(f'Entity: Affiliate')
            elif any(kw in tl for kw in ['penalty', 'recovery', 'পেনাল্টি', 'রিকভারি']):
                if not re.search(r'\bpenalty|\brecovery|পেনাল্টি|রিকভারি', content, re.IGNORECASE):
                    missing_entities.append(f'Entity: {tag}')

    if missing_entities:
        return "❌", f"Missing: {', '.join(missing_entities)}"
    else:
        return "✅", "All key entities present"


def check_pillar_link(content, tags):
    if not content:
        return "❌", "No content"

    pillar_map = [
        (['seo guide', 'bangladesh seo', 'digital marketing', '2026'], ['/', '/services'], 'Homepage / Services'),
        (['geo', 'ai search', 'generative engine optimization', 'future of seo'], ['/', '/services'], 'Homepage / Services'),
        (['garments', 'textile', 'rmg', 'b2b seo', 'garments seo', 'textile industry', 'bangladesh rmg'],
         ['/services', '/industries/manufacturing'], 'Services / Manufacturing'),
        (['মোবাইল', 'mobile first', 'mobile optimization', 'ভয়েস সার্চ', 'bangladesh mobile'], ['/', '/services'], 'Homepage / Mobile SEO'),
        (['seo ক্যারিয়ার', 'ক্যারিয়ার', 'চাকরি', 'পেশা', 'বাংলাদেশ ২০২৬', 'seo career', 'career'],
         ['/', '/about', '/services'], 'Homepage / About / Services'),
        (['affiliate marketing seo', 'affiliate seo bangladesh', 'অ্যাফিলিয়েট মার্কেটিং', 'seo কৌশল', 'bangladesh affiliate', 'affiliate'],
         ['/services', '/blog', '/'], 'Services / Homepage'),
        (['গুগল পেনাল্টি', 'পেনাল্টি রিকভারি', 'গুগল অ্যালগরিদম', 'বাংলাদেশ', 'penalty', 'recovery'],
         ['/services', '/', '/blog'], 'Services / Homepage'),
        (['b2b seo', 'lead generation', 'bangladesh business', 'industrial seo', 'b2b'], ['/services', '/'], 'Services / Homepage'),
        (['fitness seo', 'gym marketing', 'local seo', 'bangladesh fitness', 'fitness', 'gym'],
         ['/industries/fitness', '/industries'], 'Fitness industry page'),
        (['healthcare seo', 'medical seo', 'patient acquisition', 'health', 'medical', 'clinic', 'healthcare'],
         ['/industries/medical', '/industries'], 'Medical industry page'),
        (['education seo', 'student enrollment', 'university seo', 'bangladesh education', 'education', 'school', 'student'],
         ['/industries/education', '/industries'], 'Education industry page'),
        (['travel seo', 'tourism marketing', 'hospitality seo', 'bangladesh travel', 'travel', 'tourism', 'tour'],
         ['/industries/travel', '/industries'], 'Travel industry page'),
    ]

    tag_lower = [t.lower() for t in (tags or [])]

    matched_pillar = None
    for keywords, pillar_pages, pillar_name in pillar_map:
        if any(any(kw in t for kw in keywords) for t in tag_lower):
            matched_pillar = (pillar_pages, pillar_name)
            break

    if not matched_pillar:
        return "⚠️", "Could not determine pillar from tags"

    pillar_pages, pillar_name = matched_pillar

    markdown_links = re.findall(r'\((/[^)]+)\)', content)

    linked_pillars = []
    for page in pillar_pages:
        for link in markdown_links:
            if link == page or link.startswith(page + '/') or (page != '/' and page in link):
                linked_pillars.append(link)

    if linked_pillars:
        unique_links = list(set(linked_pillars))
        return "✅", f"Links to: {', '.join(unique_links[:3])}"
    else:
        return "❌", f"No link to pillar page(s): {pillar_name}"


def check_aeo_geo(content):
    if not content:
        return "❌", "No content"

    headings = re.findall(r'^#{1,6}\s+(.+)', content, re.MULTILINE)

    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are',
                      'Does', 'Will', 'Would', 'Should', 'Could', 'Which', 'Who',
                      'কিভাবে', 'কী', 'কেন', 'কখন', 'কোথায়', 'কি', 'কে', 'কার', 'কোন', 'কোনটি']

    question_headings = []
    for h in headings:
        hs = h.strip()
        for qw in question_words:
            if hs.lower().startswith(qw.lower()):
                question_headings.append(hs)
                break

    count = len(question_headings)
    if count >= 2:
        return "✅", f"{count} question headings"
    else:
        return "❌", f"{count} question headings (need ≥2)"


def check_internal_links(content):
    if not content:
        return "❌", "No content"

    links = re.findall(r'\((/[^)]+)\)', content)
    internal_links = [l for l in links if len(l) > 1]

    count = len(internal_links)
    if count >= 3:
        return "✅", f"{count} total"
    else:
        return "❌", f"{count} total (need ≥3)"


def check_schema(post):
    missing = []
    if not post.get('title'): missing.append('title')
    if not post.get('excerpt'): missing.append('excerpt')
    if not post.get('date'): missing.append('date')
    if not post.get('author'): missing.append('author')
    if not post.get('metaTitle'): missing.append('metaTitle')
    if not post.get('metaDescription'): missing.append('metaDescription')
    if not missing:
        return "✅", "All fields set"
    else:
        return "❌", f"Missing: {', '.join(missing)}"


# ─── MAIN ───────────────────────────────────────────────────────────────────

def main():
    text = read_data_file(DATA_FILE)
    all_posts = extract_posts(text)

    target_posts = []
    for slug in TARGET_SLUGS:
        found = [p for p in all_posts if p.get('slug') == slug]
        if found:
            target_posts.append(found[0])

    print(f"Checked {len(target_posts)} posts\n")

    for post in target_posts:
        slug = post.get('slug', 'unknown')
        title = post.get('title', '')
        content = post.get('content', '')
        tags = post.get('tags', [])
        excerpt = post.get('excerpt', '')
        date = post.get('date', '')

        print(f"## Post: {slug}")
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")

        keyword, tfidf_status, tfidf_detail = check_tfidf(title, content)
        print(f"| TF-IDF: `{keyword}` | {tfidf_status} | {tfidf_detail} |")

        ent_status, ent_detail = check_entities(title, content, tags)
        print(f"| Entities | {ent_status} | {ent_detail} |")

        pil_status, pil_detail = check_pillar_link(content, tags)
        print(f"| Pillar Link | {pil_status} | {pil_detail} |")

        aeo_status, aeo_detail = check_aeo_geo(content)
        print(f"| AEO/GEO | {aeo_status} | {aeo_detail} |")

        il_status, il_detail = check_internal_links(content)
        print(f"| Internal Links | {il_status} | {il_detail} |")

        sch_status, sch_detail = check_schema(post)
        print(f"| Schema Ready | {sch_status} | {sch_detail} |")

        print(f"\n### Fix instructions:")
        fixes = []

        if tfidf_status == "❌":
            count_part = tfidf_detail.split()[0]
            fixes.append(f"- TF-IDF: Add more occurrences of primary keyword `{keyword}` in content (currently {count_part})")

        if ent_status == "❌":
            missing_str = ent_detail.replace('Missing: ', '')
            fixes.append(f"- Entities: Add missing entities: {missing_str}")

        if pil_status == "❌":
            fixes.append(f"- Pillar: {pil_detail}")

        if aeo_status == "❌":
            fixes.append(f"- AEO/GEO: Add more question-based headings (How, What, Why, etc.) — currently {aeo_detail.split()[0]}")

        if il_status == "❌":
            fixes.append(f"- Internal Links: Add more internal links — currently {il_detail.split()[0]}")

        if sch_status == "❌":
            fixes.append(f"- Schema: Set missing fields: {sch_detail.replace('Missing: ', '')}")

        if not fixes:
            fixes.append("- All checks pass — no fixes needed.")

        for f in fixes:
            print(f)

        content_len = len(content) if content else 0
        heading_count = len(re.findall(r'^#{1,6}\s+', content, re.MULTILINE)) if content else 0
        print(f"\n_~{content_len:,} chars, {heading_count} headings_")
        print()


if __name__ == "__main__":
    main()
