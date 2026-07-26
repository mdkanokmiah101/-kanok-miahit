#!/usr/bin/env python3
"""
Analyze all blog posts in data.js for content quality metrics.
Outputs a pipe-delimited table.
"""

import re
import sys

# ──────────────────────────────────────────────────────────
# PARSING
# ──────────────────────────────────────────────────────────

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_posts(text):
    posts = []
    lines = text.split('\n')
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped == '{' and i + 1 < n and 'slug:' in lines[i + 1]:
            slug_m = re.search(r'slug:\s*"([^"]*)"', lines[i + 1])
            if not slug_m:
                i += 1
                continue
            slug = slug_m.group(1)

            title = None
            j = i + 2
            while j < min(i + 20, n):
                m = re.search(r'title:\s*"([^"]*)"', lines[j])
                if m:
                    title = m.group(1)
                    break
                j += 1

            content_start = None
            j = i + 2
            while j < min(i + 30, n):
                if 'content:' in lines[j] and '`' in lines[j]:
                    content_start = j
                    break
                j += 1

            if content_start is not None:
                parts = []
                sl = lines[content_start]
                bt = sl.find('`')
                after = sl[bt + 1:]
                if after.strip():
                    parts.append(after)
                k = content_start + 1
                while k < n:
                    cl = lines[k]
                    bt2 = cl.find('`')
                    if bt2 >= 0:
                        after2 = cl[bt2 + 1:].strip()
                        if after2 == '' or after2.startswith(',') or after2.startswith('//'):
                            before = cl[:bt2]
                            if before.strip():
                                parts.append(before)
                            break
                    parts.append(cl)
                    k += 1
                content_text = '\n'.join(parts)
                content_text = content_text.replace('\\`', '`')
                posts.append({'slug': slug, 'title': title, 'content': content_text})
                i = k
                continue
        i += 1

    return posts


# ──────────────────────────────────────────────────────────
# METRICS
# ──────────────────────────────────────────────────────────

def count_words(text):
    return len(re.findall(r'[\w\u0980-\u09FF]+', text))


def count_sentences(text):
    text = re.sub(r'[।]', '.', text)
    sents = re.split(r'[.!?]+', text)
    return len([s for s in sents if s.strip()])


def count_sections(text):
    return len(re.findall(r'^##\s', text, re.MULTILINE))


def get_headings(text):
    return [len(m.group(1)) for m in re.finditer(r'^(#{1,6})\s+', text, re.MULTILINE)]


def check_heading_depth(headings):
    relevant = [h for h in headings if h in (2, 3, 4)]
    if len(relevant) <= 1:
        return "YES"
    prev = relevant[0]
    for level in relevant[1:]:
        if level > prev + 1:
            return "NO"
        prev = level
    return "YES"


def count_paragraphs(text):
    blocks = re.split(r'\n\s*\n', text)
    return len([b for b in blocks if b.strip()])


def avg_sentence_length(text):
    wc = count_words(text)
    sc = count_sentences(text)
    return round(wc / sc, 1) if sc > 0 else 0.0


# ──────────────────────────────────────────────────────────
# KEYWORD EXTRACTION (improved)
# ──────────────────────────────────────────────────────────

STOP = frozenset({
    'a', 'an', 'the', 'in', 'of', 'for', 'to', 'and', 'or', 'is', 'are',
    'your', 'our', 'its', 'that', 'this', 'with', 'from', 'by', 'at',
    'on', 'be', 'has', 'have', 'do', 'does', 'not', 'no', 'but', 'how',
    'what', 'why', 'when', 'where', 'which', 'who', 'all', 'every',
    'more', 'most', 'some', 'any', 'best', 'top', 'guide', 'tips',
    'complete', 'ultimate', 'essential', 'expert', 'vs', 'vs',
    'for', 'of', 'in', 'the', 'a', 'an', 'to', 'and', 'or', 'is',
    'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'can', 'could', 'should',
    'may', 'might', 'shall', 'need', 'dare', 'ought', 'used',
    '2026', '2025', '2024', '2023', '2022', 'that', 'this', 'these',
    'those', 'it', 'its', 'you', 'your', 'our', 'they', 'them',
    'their', 'we', 'he', 'she', 'his', 'her', 'my', 'me', 'i',
    'about', 'into', 'over', 'after', 'before', 'between', 'under',
    'above', 'below', 'out', 'off', 'up', 'down', 'just', 'also',
    'very', 'too', 'really', 'already', 'still', 'even', 'much',
    'many', 'each', 'every', 'both', 'few', 'several',
})

GENERIC = frozenset({
    'seo', 'bangladesh', 'bangladeshi', 'dhaka', 'guide', 'tips',
    'checklist', 'strategy', 'strategies', 'optimization', 'marketing',
    'business', 'businesses', 'online', 'digital', 'best', 'top',
    'complete', 'ultimate', 'essential', 'expert', 'new', 'services',
    'service', 'bd', 'bengali', 'bengal', 'b2b',
})


def extract_primary_keywords(title, slug):
    """Extract 1-2 primary keywords from title/slug."""
    if not title:
        return _slug_keywords(slug)

    # Check if title has Bengali chars
    if re.search(r'[\u0980-\u09FF]', title):
        return _slug_keywords(slug)

    # Split on : — | to get the main topic
    main_part = title
    for sep in [':', '—', '–', '|', '•']:
        if sep in title:
            parts = title.split(sep)
            main_part = parts[0].strip()
            # Also consider the part after for subtopics
            break

    # Clean and tokenize the main part
    clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', main_part.lower())
    words = [w for w in clean.split() if w not in STOP and len(w) > 2]

    # Also tokenize full title for secondary candidates
    full_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', title.lower())
    full_words = [w for w in full_clean.split() if w not in STOP and len(w) > 2]

    # Build bigrams from main part
    bigrams_main = []
    for i in range(len(words) - 1):
        bg = f"{words[i]} {words[i+1]}"
        if not all(w in GENERIC for w in bg.split()):
            bigrams_main.append(bg)

    # Build bigrams from full title
    bigrams_full = []
    for i in range(len(full_words) - 1):
        bg = f"{full_words[i]} {full_words[i+1]}"
        if not all(w in GENERIC for w in bg.split()):
            if bg not in bigrams_main:
                bigrams_full.append(bg)

    # Score bigrams
    def score_bigram(bg):
        bg_words = bg.split()
        generic_ct = sum(1 for w in bg_words if w in GENERIC)
        # Prefer bigrams with 0 generic words, then 1
        base = 10 - generic_ct * 5
        # Prefer longer words
        avg_len = sum(len(w) for w in bg_words) / len(bg_words)
        base += avg_len * 0.5
        # Prefer specific-sounding terms
        if any(w in ('google', 'maps', 'facebook', 'youtube', 'daraz', 'shopify') for w in bg_words):
            base += 3
        return base

    all_candidates = [(bg, 'main', score_bigram(bg)) for bg in bigrams_main]
    all_candidates.extend([(bg, 'full', score_bigram(bg) - 2) for bg in bigrams_full])

    # Sort by score descending
    all_candidates.sort(key=lambda x: -x[2])

    # Pick top 1-2 unique bigrams
    seen = set()
    result = []
    for bg, src, score in all_candidates:
        words_in_bg = set(bg.split())
        # Skip if too similar to already chosen
        if any(words_in_bg.intersection(set(r.split())) for r in result):
            # Only skip if completely overlapping
            if words_in_bg.issubset(set(' '.join(result).split())):
                continue
        result.append(bg)
        seen.update(words_in_bg)
        if len(result) >= 2:
            break

    # If no good bigrams, try single words
    if not result:
        # Score single words (non-generic, longer = better)
        scored = [(w, len(w)) for w in full_words if w not in GENERIC and len(w) > 3]
        scored.sort(key=lambda x: -x[1])
        for w, s in scored[:2]:
            result.append(w)

    if not result:
        return _slug_keywords(slug)

    return result


def _slug_keywords(slug):
    """Extract keywords from slug as fallback."""
    parts = [p for p in slug.split('-') if p not in GENERIC | STOP and len(p) > 2]
    if not parts:
        parts = slug.split('-')[:2]
    # Prefer multi-word phrases from slug
    phrases = []
    for i in range(len(parts) - 1):
        phrases.append(f"{parts[i]} {parts[i+1]}")
    if phrases:
        return phrases[:2]
    return parts[:2] if parts else ['none']


def count_keyword_occurrences(text, keywords):
    """Count occurrences of each keyword in text."""
    text_lower = text.lower()
    results = []
    for kw in keywords:
        if kw == 'none':
            results.append((kw, 0))
            continue
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        count = len(re.findall(pattern, text_lower))
        results.append((kw, count))
    return results


# ──────────────────────────────────────────────────────────
# PASSIVE VOICE
# ──────────────────────────────────────────────────────────

def count_passive_voice(text):
    """Rough count of passive voice constructions."""
    irregular = (
        r'built|done|made|written|known|given|taken|found|set|put|run|'
        r'bought|sold|sent|shown|kept|paid|led|held|met|won|lost|grown|'
        r'drawn|broken|driven|eaten|fallen|hidden|ridden|risen|spoken|'
        r'torn|worn|brought|caught|chosen|forgotten|frozen|hung|learnt|'
        r'meant|said|slept|spent|stood|struck|taught|thought|understood|'
        r'woken|begun|bitten|blown|dealt|dug|flown|laid|lain|overcome|'
        r'ridden|rung|sought|shaken|shot|shrunk|sung|sunk|sworn|swept|'
        r'swum|thrown|upset|woven'
    )

    patterns = [
        rf'\b(?:is|are)\s+(?:\w+ed|{irregular})\b',
        rf'\b(?:was|were)\s+(?:\w+ed|{irregular})\b',
        rf'\b(?:been|being)\s+(?:\w+ed|{irregular})\b',
        rf'\b(?:be|gets?|got|gotten)\s+(?:\w+ed|{irregular})\b',
        rf'\b(?:has been|have been|had been)\s+(?:\w+ed|{irregular})\b',
        rf'\b(?:is being|are being|was being|were being)\s+(?:\w+ed|{irregular})\b',
    ]

    total = 0
    for pat in patterns:
        total += len(re.findall(pat, text, re.IGNORECASE))
    return total


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def main():
    filepath = '/root/kanok-miahit/src/app/blog/data.js'
    sys.stderr.write("Reading file...\n")
    text = read_file(filepath)
    nlines = text.count('\n') + 1
    sys.stderr.write(f"File: {len(text)} chars, {nlines} lines\n")

    sys.stderr.write("Extracting posts...\n")
    posts = extract_posts(text)
    sys.stderr.write(f"Found {len(posts)} posts\n")

    if len(posts) == 0:
        sys.stderr.write("ERROR: No posts extracted!\n")
        sys.exit(1)

    cols = "slug|word_count|sections|para_count|heading_depth_OK|primary_keywords_covered|avg_sentence_len|passive_voice_count"
    print(cols)

    for post in posts:
        slug = post['slug']
        title = post['title'] or slug
        content = post['content']

        # Clean content: remove markdown links and images (keep visible text)
        clean = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', content)
        clean = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', clean)

        wc = count_words(clean)
        sections = count_sections(content)
        paras = count_paragraphs(clean)
        headings = get_headings(content)
        depth_ok = check_heading_depth(headings)

        keywords = extract_primary_keywords(title, slug)
        kw_occurrences = count_keyword_occurrences(content, keywords)

        kw_names = [k for k, c in kw_occurrences]
        kw_total = sum(c for k, c in kw_occurrences)
        kw_str = ", ".join(kw_names) if kw_names else "none"
        kw_field = f"{kw_str}:{kw_total}"

        avg_sent = avg_sentence_length(clean)
        passive = count_passive_voice(clean)

        print(f"{slug}|{wc}|{sections}|{paras}|{depth_ok}|{kw_field}|{avg_sent}|{passive}")


if __name__ == '__main__':
    main()
