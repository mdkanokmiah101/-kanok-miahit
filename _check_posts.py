#!/usr/bin/env python3
"""Extract blog posts from data.js and run content framework checks."""
import re, sys, json

with open('src/app/blog/data.js') as f:
    text = f.read()

# Find all post blocks using a careful brace-matching approach
# The file format is: const posts = [\n  {\n    ...\n  },\n  {\n    ...\n  },\n];
# Each post ends with "}," or the last one with "}\n];"

posts_raw = []
depth = 0
current_start = -1
i = 0
while i < len(text):
    ch = text[i]
    if ch == '{':
        if depth == 0:
            current_start = i
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0 and current_start >= 0:
            # Check if this looks like a post object (has slug:)
            block = text[current_start:i+1]
            if 'slug:' in block and 'title:' in block:
                posts_raw.append(block)
            current_start = -1
    i += 1

print(f"Found {len(posts_raw)} post objects")

# Extract fields from each post
target_slugs = [
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

def get_field(block, field):
    """Extract a field value from a post block."""
    # Try different patterns
    patterns = [
        rf'{field}:\s*"([^"]*)"',
        rf'{field}:\s*`([^`]*)`',
    ]
    for pat in patterns:
        m = re.search(pat, block, re.DOTALL)
        if m:
            return m.group(1)
    
    # For multi-line content
    if field == 'content':
        # Find content: followed by backtick
        idx = block.find('content:')
        if idx >= 0:
            rest = block[idx:]
            bt_idx = rest.find('`')
            if bt_idx >= 0:
                bt_end = rest.rfind('`')
                if bt_end > bt_idx:
                    return rest[bt_idx+1:bt_end]
    return ''

def get_date(block):
    d = get_field(block, 'date')
    return d

# Find posts we care about
for block in posts_raw:
    slug = get_field(block, 'slug')
    if slug in target_slugs:
        title = get_field(block, 'title')
        date = get_field(block, 'date')
        excerpt = get_field(block, 'excerpt')
        tags_raw = get_field(block, 'tags')
        content = get_field(block, 'content')
        
        # Parse tags
        if tags_raw:
            tags = [t.strip().strip('"').strip("'") for t in tags_raw.split(',')]
        else:
            tags = []
        
        print(f"\n{'='*80}")
        print(f"POST: {slug}")
        print(f"TITLE: {title}")
        print(f"DATE: {date}")
        print(f"TAGS: {tags}")
        print(f"EXCERPT: {excerpt[:100] if excerpt else '(empty)'}")
        print(f"CONTENT_LENGTH: {len(content)} chars")
        
        # ---- FRAMEWORK CHECKS ----
        
        # A. TF-IDF Coverage - extract primary keyword from title
        # First significant noun phrase from title
        title_lower = title.lower()
        # Remove common leading phrases
        title_clean = re.sub(r'^(how to|what does|top \d+|why|is|are|can|do|does|the|a|an)\s+', '', title_lower)
        # Take first 2-3 words as keyword
        words = title_clean.split()
        # Filter out stop words for first meaningful phrase
        stops = {'a', 'an', 'the', 'in', 'for', 'of', 'to', 'and', 'or', 'is', 'are', 'was', 'were', 
                 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                 'can', 'could', 'shall', 'should', 'may', 'might', 'must', 'with', 'from', 'by',
                 'at', 'on', 'your', 'our', 'their', 'its', 'it', 'we', 'you', 'they', 'this', 'that'}
        keyword_words = []
        for w in words:
            if w not in stops and len(w) > 2:
                keyword_words.append(w)
            if len(keyword_words) >= 3:
                break
        if not keyword_words:
            keyword_words = words[:3]
        keyword = ' '.join(keyword_words)
        
        # Count occurrences
        keyword_counts = 0
        for kw in keyword_words:
            if len(kw) > 2:
                keyword_counts += content.lower().count(kw)
        
        # Better: count the full phrase occurrences
        phrase_count = content.lower().count(keyword)
        # And also count individual meaningful words
        unique_words_in_content = set(w.lower() for w in keyword.split())
        word_counts = {w: content.lower().count(w) for w in unique_words_in_content}
        
        print(f"\n--- A. TF-IDF COVERAGE ---")
        print(f"Primary keyword phrase: '{keyword}'")
        print(f"Phrase occurrences: {phrase_count}")
        for w, c in word_counts.items():
            print(f"  Word '{w}': {c} occurrences")
        tfidf_ok = any(c >= 5 for c in word_counts.values()) or phrase_count >= 3
        print(f"TF-IDF STATUS: {'✅' if tfidf_ok else '❌'} (threshold: ≥5 occurrences of key terms)")
        
        # B. Semantic Entity Coverage
        print(f"\n--- B. SEMANTIC ENTITY COVERAGE ---")
        entities = {
            'location_dhaka': ('Dhaka', content.lower().count('dhaka')),
            'location_bangladesh': ('Bangladesh', content.lower().count('bangladesh')),
            'service_seo': ('SEO', content.lower().count('seo')),
            'service_digital_marketing': ('Digital Marketing', content.lower().count('digital marketing')),
        }
        
        # Add industry-specific entities based on tags
        all_content_lower = content.lower()
        missing_entities = []
        entity_results = []
        
        for key, (label, count) in entities.items():
            if count >= 1:
                entity_results.append(f"{label}: ✅ ({count})")
            else:
                entity_results.append(f"{label}: ❌ (0)")
                missing_entities.append(label)
        
        # Check for Google/GBP mentions
        if 'google' in all_content_lower:
            entity_results.append(f"Google mentions: ✅ ({content.lower().count('google')})")
        else:
            missing_entities.append('Google')
            entity_results.append("Google mentions: ❌ (0)")
        
        # Check for author mention
        author = get_field(block, 'author')
        author_count = content.lower().count(author.lower().split()[-1]) if author else 0
        if author_count >= 1:
            entity_results.append(f"Author entity: ✅ ({author}, {author_count} mentions)")
        else:
            missing_entities.append(f'Author ({author})')
            entity_results.append(f"Author entity: ❌ (0)")
        
        print('\n'.join(entity_results))
        entities_ok = len(missing_entities) == 0
        
        # C. Pillar-Cluster Alignment
        print(f"\n--- C. PILLAR-CLUSTER ALIGNMENT ---")
        # Determine pillar from tags
        pillar_map = {
            'seo guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
            'local seo': '/services/local-seo',
            'technical seo': '/services/technical-seo',
            'seo services': '/',
            'seo case study': '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
            'case study': '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
            'ai seo': '/services/geo-ai-search',
            'geo': '/services/geo-ai-search',
            'ecommerce': '/services/ecommerce-seo',
            'e-commerce': '/services/ecommerce-seo',
            'hire seo': '/',
            'seo expert': '/',
            'seo agency': '/',
            'seo mistakes': '/',
            'seo roi': '/',
        }
        
        matched_pillar = None
        for tag in tags:
            tag_lower = tag.lower()
            for key, pillar_url in pillar_map.items():
                if key in tag_lower:
                    matched_pillar = pillar_url
                    break
            if matched_pillar:
                break
        
        if not matched_pillar:
            # Default pillar
            matched_pillar = '/'
        
        # Check if post links to its pillar
        pillar_links = content.count(matched_pillar)
        print(f"Detected pillar tag: {tags[0] if tags else '(none)'}")
        print(f"Pillar URL: {matched_pillar}")
        print(f"Links to pillar: {pillar_links} occurrences")
        pillar_ok = pillar_links >= 1
        
        # Check for internal links to other pillars
        other_pillar_links = 0
        for pil_url in set(pillar_map.values()):
            if pil_url != matched_pillar:
                other_pillar_links += content.count(pil_url)
        print(f"Links to other pillar pages: {other_pillar_links}")
        
        # D. AEO/GEO Optimization
        print(f"\n--- D. AEO/GEO OPTIMIZATION ---")
        question_starts = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Does', 'Is', 'Are', 'Which', 'Who']
        question_heading_count = 0
        question_headings = []
        
        lines = content.split('\n')
        for line in lines:
            stripped = line.strip()
            # Check for markdown headings (## or ###)
            if stripped.startswith('##') or stripped.startswith('###'):
                heading_text = stripped.lstrip('#').strip()
                first_word = heading_text.split()[0] if heading_text.split() else ''
                if first_word in question_starts:
                    question_heading_count += 1
                    question_headings.append(heading_text[:80])
        
        # Also check for questions in the FAQ section
        faq_questions = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('###') and '?' in stripped:
                faq_questions += 1
        
        print(f"Question-based headings: {question_heading_count}")
        for qh in question_headings:
            print(f"  - {qh}")
        print(f"FAQ questions (with ?): {faq_questions}")
        aeo_ok = question_heading_count >= 2
        
        # E. Internal Linking
        print(f"\n--- E. INTERNAL LINKING ---")
        # Count all markdown links starting with /
        internal_links = re.findall(r'\[([^\]]*)\]\((/[^\)]+)\)', content)
        viable_links = [(text, url) for text, url in internal_links 
                       if not url.startswith('//') and not url.startswith('/#')]
        
        # Also count links to /blog/, /services/, /industries/
        blog_links = sum(1 for _, url in viable_links if '/blog/' in url)
        service_links = sum(1 for _, url in viable_links if '/services/' in url)
        industry_links = sum(1 for _, url in viable_links if '/industries/' in url)
        home_links = sum(1 for _, url in viable_links if url == '/')
        
        print(f"Total internal links: {len(viable_links)}")
        print(f"  Blog links: {blog_links}")
        print(f"  Service links: {service_links}")
        print(f"  Industry links: {industry_links}")
        print(f"  Home links: {home_links}")
        for text, url in viable_links[:10]:
            print(f"    [{text}]({url})")
        if len(viable_links) > 10:
            print(f"    ... and {len(viable_links)-10} more")
        links_ok = len(viable_links) >= 3
        
        # F. Schema Ready
        print(f"\n--- F. SCHEMA READY ---")
        has_title = len(title) > 0
        has_excerpt = len(excerpt) > 0
        has_date = len(date) > 0
        has_author = len(author) > 0
        schema_ready = has_title and has_excerpt and has_date and has_author
        print(f"Title set: {'✅' if has_title else '❌'}")
        print(f"Excerpt set: {'✅' if has_excerpt else '❌'} ({len(excerpt)} chars)")
        print(f"Date set: {'✅' if has_date else '❌'} ({date})")
        print(f"Author set: {'✅' if has_author else '❌'} ({author})")
        
        # ---- SUMMARY ----
        print(f"\n{'='*40} SUMMARY {'='*40}")
        checks = {
            'TF-IDF Coverage': tfidf_ok,
            'Entity Coverage': entities_ok,
            'Pillar Link': pillar_ok,
            'AEO/GEO': aeo_ok,
            'Internal Links': links_ok,
            'Schema Ready': schema_ready,
        }
        details = {
            'TF-IDF Coverage': f"{'✅' if tfidf_ok else '❌'} — keyword '{keyword}', key term occurrences: {word_counts}",
            'Entity Coverage': f"{'✅' if entities_ok else '❌'} — {'All entities present' if entities_ok else 'Missing: ' + ', '.join(missing_entities)}",
            'Pillar Link': f"{'✅' if pillar_ok else '❌'} — Links to {matched_pillar}: {pillar_links}x",
            'AEO/GEO': f"{'✅' if aeo_ok else '❌'} — {question_heading_count} question headings",
            'Internal Links': f"{'✅' if links_ok else '❌'} — {len(viable_links)} internal links",
            'Schema Ready': f"{'✅' if schema_ready else '❌'} — {'All fields set' if schema_ready else 'Missing fields'}",
        }
        
        for check, ok in checks.items():
            print(f"{'✅' if ok else '❌'} {check}: {details[check]}")
        
        # Fix instructions
        print(f"\n{'='*40} FIX INSTRUCTIONS {'='*40}")
        fixes = []
        if not tfidf_ok:
            fixes.append(f"- Increase keyword '{keyword}' usage in content (currently {phrase_count} occurrences, need ≥5)")
        if not entities_ok:
            fixes.append(f"- Add missing entities: {', '.join(missing_entities)}")
        if not pillar_ok:
            fixes.append(f"- Add internal link to pillar page ({matched_pillar})")
        if not aeo_ok:
            fixes.append(f"- Add more question-based headings (currently {question_heading_count}, need ≥2)")
        if not links_ok:
            fixes.append(f"- Add more internal links (currently {len(viable_links)}, need ≥3)")
        if not schema_ready:
            missing_schema = []
            if not has_title: missing_schema.append('title')
            if not has_excerpt: missing_schema.append('excerpt')
            if not has_date: missing_schema.append('date')
            if not has_author: missing_schema.append('author')
            fixes.append(f"- Set missing schema fields: {', '.join(missing_schema)}")
        
        if fixes:
            print('\n'.join(fixes))
        else:
            print("✅ All checks pass — no fixes needed.")
        
        print(f"{'='*80}")
