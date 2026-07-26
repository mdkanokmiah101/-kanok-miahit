#!/usr/bin/env python3
"""Combine all audit data and generate a prioritized SEO Content Audit report."""

import csv

# Read content quality data
quality = {}
with open('/root/kanok-miahit/content_quality_analysis.csv') as f:
    reader = csv.DictReader(f, delimiter='|')
    for row in reader:
        slug = row['slug']
        quality[slug] = {
            'word_count': int(row['word_count']),
            'sections': int(row['sections']),
            'para_count': int(row['para_count']),
            'heading_depth_OK': row['heading_depth_OK'],
            'primary_keywords_covered': row['primary_keywords_covered'],
            'avg_sentence_len': float(row['avg_sentence_len']),
            'passive_voice_count': int(row['passive_voice_count']),
        }

# Read entity data
entities = {}
with open('/root/kanok-miahit/blog_entity_analysis.txt') as f:
    reader = csv.DictReader(f, delimiter='|')
    for row in reader:
        slug = row['slug']
        entities[slug] = {
            'entity_count': int(row['entity_count']),
            'question_headings': int(row['question_headings']),
            'geo_ready': row['geo_ready'],
            'entity_density': float(row['entity_density']),
            'geo_opportunity': row['geo_opportunity'],
            'entity_gap': row['entity_gap'],
        }

# Read link data
links = {}
with open('/root/kanok-miahit/link_analysis_final.json') as f:
    import json
    data = json.load(f)
    for post in data['posts']:
        slug = post['slug']
        links[slug] = {
            'internal_links': post.get('internal_count', 0),
            'external_links': post.get('external_count', 0),
            'broken_blog_links': post.get('broken_blog_count', 0),
            'link_density': post.get('link_density', 0),
            'missing_blog_prefix': post.get('missing_blog_prefix_count', 0),
        }

# All slugs
all_slugs = set(quality.keys()) | set(entities.keys()) | set(links.keys())

# Titles map (from quality data or extract from data.js)
titles = {}
import re
with open('/root/kanok-miahit/src/app/blog/data.js') as f:
    text = f.read()
    # Find all title/slug pairs
    slug_title_pairs = re.findall(r'slug:\s*"([^"]+)"[^}]*?title:\s*"([^"]+)"', text, re.DOTALL)
    for s, t in slug_title_pairs:
        titles[s] = t

print("=" * 100)
print("SEO CONTENT AUDIT REPORT — kanokmiah.com.bd")
print(f"Generated: 2026-07-26 | Posts Analyzed: {len(all_slugs)}")
print("=" * 100)

# ============================================
# 1. TOP 10 POSTS NEEDING IMMEDIATE ATTENTION
# ============================================
print("\n" + "=" * 100)
print("SECTION 1: TOP 10 POSTS NEEDING IMMEDIATE ATTENTION")
print("(Based on composite score: low word count, low entity density, low internal links, zero question headings)")
print("=" * 100)

# Compute composite priority score (lower = needs more attention)
scored = []
for slug in all_slugs:
    q = quality.get(slug, {})
    e = entities.get(slug, {})
    l = links.get(slug, {})
    
    # Score components (0 = bad, 1 = good)
    word_score = min(q.get('word_count', 0) / 1500, 1.0)  # under 1500 words is thin
    entity_score = min(e.get('entity_density', 0) / 1.5, 1.0)  # density under 1.5 is low
    link_score = min(l.get('link_density', 0) / 0.5, 1.0)  # link density under 0.5 is low
    question_score = 1.0 if e.get('question_headings', 0) > 0 else 0.0
    keyword_score = 1.0  # estimated from keyword coverage data
    
    # Composite (lower = worse)
    composite = (word_score + entity_score + link_score + question_score) / 4.0
    
    title = titles.get(slug, slug)
    scored.append({
        'slug': slug,
        'title': title,
        'composite': composite,
        'word_count': q.get('word_count', 0),
        'entity_density': e.get('entity_density', 0),
        'link_density': l.get('link_density', 0),
        'question_headings': e.get('question_headings', 0),
        'internal_links': l.get('internal_links', 0),
        'broken_links': l.get('broken_blog_links', 0),
        'geo_opportunity': e.get('geo_opportunity', 'NO'),
        'entity_gap': e.get('entity_gap', 'NO'),
        'sections': q.get('sections', 0),
        'avg_sentence_len': q.get('avg_sentence_len', 0),
    })

# Sort by composite ascending (worst first)
scored.sort(key=lambda x: x['composite'])

for i, p in enumerate(scored[:10], 1):
    flags = []
    if p['word_count'] < 1000:
        flags.append("THIN CONTENT")
    if p['entity_density'] < 1.0:
        flags.append("ENTITY GAP")
    if p['link_density'] < 0.5:
        flags.append("LOW LINK DENSITY")
    if p['question_headings'] == 0:
        flags.append("NO QUESTION HEADINGS")
    if p['broken_links'] > 0:
        flags.append("BROKEN LINKS")
    if p['geo_opportunity'] == 'YES':
        flags.append("GEO OPPORTUNITY")
    if p['entity_gap'] == 'YES':
        flags.append("ENTITY GAP")
    if p['sections'] <= 1 and p['word_count'] > 500:
        flags.append("FLAT STRUCTURE")
    
    flag_str = ", ".join(flags) if flags else "OK"
    print(f"\n  #{i}: {p['title']}")
    print(f"      Slug: {p['slug']}")
    print(f"      Words: {p['word_count']} | Sections: {p['sections']} | Internal Links: {p['internal_links']}")
    print(f"      Entity Density: {p['entity_density']:.2f} | Q-headings: {p['question_headings']}")
    print(f"      Composite Score: {p['composite']:.3f} | Issues: {flag_str}")

# ============================================
# 2. TF-IDF GAPS
# ============================================
print("\n" + "=" * 100)
print("SECTION 2: TF-IDF / KEYWORD COVERAGE GAPS")
print("(Posts whose primary keywords are barely mentioned in content)")
print("=" * 100)

# Posts where primary keyword coverage is 0 (primary keywords not found in content)
keyword_gaps = []
for slug in all_slugs:
    q = quality.get(slug, {})
    kw_str = q.get('primary_keywords_covered', '')
    # Parse "keyword1:count, keyword2:count" or "keyword:count"
    title = titles.get(slug, slug)
    
    # Check if keyword coverage shows 0 count
    parts = kw_str.split(',')
    missing_keywords = []
    for part in parts:
        part = part.strip()
        if ':' in part:
            kw_name = part.rsplit(':', 1)[0].strip()
            kw_count_str = part.rsplit(':', 1)[1].strip()
            if kw_count_str == '0':
                missing_keywords.append(kw_name)
    
    if missing_keywords:
        keyword_gaps.append({
            'slug': slug,
            'title': title,
            'missing_keywords': missing_keywords,
            'kw_str': kw_str,
        })

keyword_gaps.sort(key=lambda x: len(x['missing_keywords']), reverse=True)
for p in keyword_gaps[:20]:
    print(f"\n  ✗ {p['title']}")
    print(f"    Slug: {p['slug']}")
    print(f"    Missing: {', '.join(p['missing_keywords'])}")
    print(f"    Full coverage: {p['kw_str']}")

if not keyword_gaps:
    print("\n  No primary keyword coverage gaps detected (all posts have their keywords).")

# ============================================
# 3. AEO/GEO OPPORTUNITIES
# ============================================
print("\n" + "=" * 100)
print("SECTION 3: AEO/GEO OPPORTUNITIES")
print("(Posts with zero question headings — need conversational AEO/GEO structure)")
print("=" * 100)

geo_opps = [p for p in scored if p['question_headings'] == 0]
geo_opps.sort(key=lambda x: x['word_count'], reverse=True)

for p in geo_opps:
    print(f"\n  🎯 {p['title']}")
    print(f"    Slug: {p['slug']}")
    print(f"    Words: {p['word_count']} | Sections: {p['sections']} | Entity Density: {p['entity_density']:.2f}")
    print(f"    Fix: Add 3-5 question-format headings (H2/H3 with ? or How/What/Why) to capture AI search traffic")

print(f"\n  Total posts with zero question headings: {len(geo_opps)}")

# ============================================
# 4. INTERNAL LINKING ISSUES
# ============================================
print("\n" + "=" * 100)
print("SECTION 4: INTERNAL LINKING ISSUES")
print("(Posts with low internal link counts or broken links)")
print("=" * 100)

# Posts with few internal links (≤ 5)
low_link_posts = [p for p in scored if p['internal_links'] <= 5]
low_link_posts.sort(key=lambda x: x['internal_links'])

for p in low_link_posts:
    print(f"\n  🔗 {p['title']}")
    print(f"    Slug: {p['slug']}")
    print(f"    Internal Links: {p['internal_links']} | Link Density: {p['link_density']:.2f} | External: -")

# Broken links
broken_posts = [p for p in scored if p['broken_links'] > 0]
if broken_posts:
    print("\n  BROKEN LINKS FOUND:")
    for p in broken_posts:
        print(f"  ⚠ {p['title']} — {p['broken_links']} broken blog link(s)")
else:
    print("\n  ✓ No broken blog links detected.")

print(f"\n  Posts with ≤5 internal links: {len(low_link_posts)}")
print(f"  Posts with broken links: {len(broken_posts)}")

# ============================================
# 5. ENTITY GAPS
# ============================================
print("\n" + "=" * 100)
print("SECTION 5: ENTITY DENSITY GAPS")
print("(Posts with low named entity density — < 1.0 entities per 100 words)")
print("=" * 100)

entity_gap_posts = [p for p in scored if p['entity_density'] < 1.0]
entity_gap_posts.sort(key=lambda x: x['entity_density'])

for p in entity_gap_posts:
    print(f"\n  🧩 {p['title']}")
    print(f"    Slug: {p['slug']}")
    print(f"    Entity Density: {p['entity_density']:.2f} (target: ≥ 1.0) | Words: {p['word_count']}")
    print(f"    Fix: Add more named entities (cities like Dhaka/Chittagong, companies, technologies, people names)")

entity_gap_slugs = [p['slug'] for p in entity_gap_posts]
print(f"\n  Total posts with entity gap: {len(entity_gap_posts)}")

# Also list geo_opportunity posts
geo_opp_slugs = [p['slug'] for p in geo_opps]
print(f"  Total posts needing GEO work: {len(geo_opps)}")

# ============================================
# 6. RECOMMENDED ACTIONS PER POST
# ============================================
print("\n" + "=" * 100)
print("SECTION 6: PRIORITIZED ACTIONS PER POST")
print("(Top 25 posts needing action — max 3 recommendations each)")
print("=" * 100)

for p in scored[:25]:
    actions = []
    
    # Check content thinness
    if p['word_count'] < 1000:
        actions.append(f"EXPAND CONTENT: currently {p['word_count']} words, aim for 1500+")
    elif p['word_count'] < 1500:
        actions.append(f"STRENGTHEN CONTENT: currently {p['word_count']} words, aim for 2000+")
    
    # Check heading count
    if p['sections'] <= 1 and p['word_count'] > 500:
        actions.append(f"ADD SECTIONS: currently only {p['sections']} H2 section(s), add 5+ for better structure")
    elif p['sections'] <= 3:
        actions.append(f"MORE SECTIONS: currently {p['sections']} H2 sections, add 3-5 more")
    
    # Check entity density
    if p['entity_density'] < 1.0:
        actions.append(f"IMPROVE ENTITY DENSITY: currently {p['entity_density']:.2f}/100 words, target ≥1.5")
    
    # Check internal links
    if p['internal_links'] < 5:
        actions.append(f"ADD INTERNAL LINKS: currently {p['internal_links']}, link to related blog posts/services")
    elif p['internal_links'] < 10:
        actions.append(f"STRENGTHEN INTERNAL LINKS: currently {p['internal_links']}, aim for 15+")
    
    # Check question headings
    if p['question_headings'] == 0:
        actions.append(f"ADD QUESTION HEADINGS: currently 0, add FAQ section + question-format H2s for AEO/GEO")
    elif p['question_headings'] <= 3:
        actions.append(f"MORE QUESTIONS: currently {p['question_headings']} question headings, add 3+ for AEO")
    
    # Check sentence length
    if p['avg_sentence_len'] > 25:
        actions.append(f"REDUCE SENTENCE LENGTH: currently avg {p['avg_sentence_len']:.0f} words, break into shorter sentences")
    
    # Limit to top 3
    actions = actions[:3]
    
    if actions:
        print(f"\n  📌 {p['title']}")
        print(f"     Slug: {p['slug']}")
        for a in actions:
            print(f"     ▶ {a}")

# ============================================
# OVERALL SUMMARY
# ============================================
print("\n" + "=" * 100)
print("EXECUTIVE SUMMARY")
print("=" * 100)

avg_words = sum(q.get('word_count', 0) for q in quality.values()) / max(len(quality), 1)
avg_entity = sum(e.get('entity_density', 0) for e in entities.values()) / max(len(entities), 1)
avg_links = sum(l.get('link_density', 0) for l in links.values()) / max(len(links), 1)
total_broken = sum(l.get('broken_blog_links', 0) for l in links.values())
total_internal = sum(l.get('internal_links', 0) for l in links.values())

print(f"""
  Total Posts Analyzed:    {len(all_slugs)}
  Avg Word Count:          {avg_words:.0f}
  Avg Entity Density:      {avg_entity:.2f}/100 words
  Avg Link Density:        {avg_links:.2f}/100 words
  Total Internal Links:    {total_internal}
  Total Broken Links:      {total_broken}
  Posts w/ GEO Gap:        {len(geo_opps)} ({len(geo_opps)/len(all_slugs)*100:.1f}%)
  Posts w/ Entity Gap:     {len(entity_gap_posts)} ({len(entity_gap_posts)/len(all_slugs)*100:.1f}%)
  Posts w/ Low Links (≤5): {len(low_link_posts)} ({len(low_link_posts)/len(all_slugs)*100:.1f}%)

  WEBSITE OVERALL HEALTH: {'🟢 GOOD' if avg_words > 1500 and avg_entity > 1.0 and total_broken == 0 else '🟡 NEEDS WORK'}

  TOP PRIORITY ACTIONS:
  1. Expand thin case study posts (460-586 words) to 1500+ words
  2. Add question-format headings to {len(geo_opps)} posts for AEO/GEO readiness
  3. Improve entity density in {len(entity_gap_posts)} low-entity posts
  4. Fix 2 broken example links in schema posts
  5. Strengthen internal linking in shorter/industry-specific posts
  6. Add Bengali-language GEO optimization (major untapped opportunity)
""")

print("=" * 100)
print("END OF REPORT")
print("=" * 100)
