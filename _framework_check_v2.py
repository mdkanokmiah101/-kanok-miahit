#!/usr/bin/env python3
"""Refined framework checks for Bengali posts."""
import re, json

with open("src/app/blog/data.js", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')

def extract_post_improved(slug):
    """Better extraction for Bengali posts."""
    for i, line in enumerate(lines):
        if f'slug: "{slug}"' in line:
            # Go back to find opening brace
            start = i
            while start > 0 and lines[start].strip() != '{':
                start -= 1
            
            # Find closing }, with proper brace counting
            brace_count = 0
            end = start
            for j in range(start, min(start + 2000, len(lines))):
                brace_count += lines[j].count('{') - lines[j].count('}')
                if brace_count == 0 and j > start:
                    end = j
                    break
            
            block = '\n'.join(lines[start:end+1])
            
            result = {'slug': slug}
            
            # Extract fields more carefully
            for field in ['title', 'date', 'author', 'imagePlaceholder']:
                m = re.search(rf'{field}:\s*"([^"]*)"', block)
                if m:
                    result[field] = m.group(1)
            
            # excerpt - can be multi-line
            excerpt_m = re.search(r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', block, re.DOTALL)
            if excerpt_m:
                result['excerpt'] = excerpt_m.group(1).strip()
            else:
                excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', block)
                if excerpt_m:
                    result['excerpt'] = excerpt_m.group(1)
            
            # tags
            tags_m = re.search(r'tags:\s*\[([^\]]+)\]', block)
            if tags_m:
                result['tags'] = [t.strip().strip('"') for t in tags_m.group(1).split(',')]
            
            # meta fields
            result['metaTitle'] = bool(re.search(r'metaTitle:', block))
            result['metaDescription'] = bool(re.search(r'metaDescription:', block))
            result['dateModified'] = bool(re.search(r'dateModified:', block))
            
            # content - find the backtick
            ci = block.find('content: `')
            if ci >= 0:
                after = block[ci + len('content: `'):]
                # Find closing backtick followed by , or end
                # Need to find the closing ` that ends the content
                depth = 0
                end_pos = -1
                for pos in range(len(after)):
                    ch = after[pos]
                    if ch == '`':
                        if pos + 1 < len(after) and after[pos+1] == ',':
                            end_pos = pos
                            break
                        elif pos + 1 == len(after):
                            end_pos = pos
                            break
                    if ch == '\n':
                        pass
                        
                if end_pos >= 0:
                    result['content'] = after[:end_pos]
                else:
                    # Try finding `, at end of line
                    m2 = re.search(r'^([\s\S]*?)`,\s*$', after, re.MULTILINE)
                    if m2:
                        result['content'] = m2.group(1)
            
            return result
    return None

print("=" * 70)
print("REFINED FRAMEWORK CHECKS FOR CHANGED POSTS")
print("=" * 70)

for slug in [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "schema-markup-rich-snippets-techniques",
    "seo-canonical-url-guide-bd"
]:
    post = extract_post_improved(slug)
    if not post:
        print(f"\n## Post: {slug} - COULD NOT EXTRACT")
        continue
    
    title = post.get('title', 'N/A')
    content = post.get('content', '')
    tags = post.get('tags', [])
    
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    print(f"Title: {title}")
    print(f"Tags: {tags}")
    print(f"Content length: {len(content)} chars")
    print(f"metaTitle: {post.get('metaTitle')}, metaDescription: {post.get('metaDescription')}, dateModified: {post.get('dateModified')}")
    
    # ===== A. TF-IDF Coverage =====
    print(f"\n--- A. TF-IDF Coverage ---")
    
    # Detect language
    is_bengali = any(ord(c) > 0x0980 for c in title)
    
    if is_bengali:
        # For Bengali, use the keyword before colon or first phrase
        parts = title.split(':')
        keyword_phrase = parts[0].strip()  # e.g., "স্কিমা মার্কআপ"
        keyword_count = content.count(keyword_phrase)
        print(f"Keyword phrase: '{keyword_phrase}'")
        print(f"Occurrences: {keyword_count}")
        
        # Also check without spaces
        if keyword_count < 5:
            # Try with just the first 2 words
            words = keyword_phrase.split()
            if len(words) >= 2:
                kw2 = words[0] + ' ' + words[1]
                c2 = content.count(kw2)
                print(f"  (also checked '{kw2}': {c2})")
                keyword_count = max(keyword_count, c2)
    else:
        # English: first significant word
        stop_words = {'the', 'a', 'an', 'for', 'in', 'of', 'to', 'and', 'or', 'is', 'are', 'how', 'what', 'why', 'when', 'where', 'your', 'our', 'their', 'its', 'that', 'this', 'with', 'from', 'has', 'have', 'not', 'but', 'can', 'all', 'will', 'was', 'were', 'been', 'being', 'some', 'which', 'who', 'whom', 'does', 'do', 'did', 'may', 'might', 'must', 'shall', 'should', 'would', 'could'}
        words = [w for w in re.findall(r'\b[a-zA-Z]+\b', title.lower()) if w not in stop_words and len(w) > 2]
        keyword = words[0] if words else ''
        keyword_count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content.lower())) if keyword else 0
        print(f"Keyword: '{keyword}'")
        print(f"Occurrences: {keyword_count}")
    
    status_a = "✅" if keyword_count >= 5 else "❌"
    print(f"Status: {status_a} ({keyword_count} occurrences, need >= 5)")
    
    # ===== B. Entities =====
    print(f"\n--- B. Semantic Entity Coverage ---")
    cl = content.lower()
    
    entity_checks = {
        'Location: Dhaka': ['dhaka', 'ঢাকা'],
        'Location: Bangladesh': ['bangladesh', 'বাংলাদেশ'],
        'Location: Chittagong': ['chittagong', 'চট্টগ্রাম'],
        'Author: Kanok Miah': ['kanok miah', 'কনক মিঞা'],
        'Bangladesh (lang-neutral)': ['bangladesh'],
    }
    
    # Check tag-based service entities
    for tag in tags:
        tl = tag.lower()
        if 'mobile' in tl:
            entity_checks['Service: Mobile SEO'] = ['mobile seo', 'মোবাইল']
        if 'schema' in tl or 'rich snippet' in tl or 'structured data' in tl:
            entity_checks['Service: Schema'] = ['schema', 'স্কিমা']
        if 'canonical' in tl or 'canonical tag' in tl:
            entity_checks['Service: Canonical'] = ['canonical', 'ক্যানোনিকাল']
        if 'seo expert' in tl or 'hire seo' in tl:
            entity_checks['Service: SEO Expert'] = ['seo expert', 'এসইও']
        if 'technical' in tl:
            entity_checks['Service: Technical SEO'] = ['technical seo', 'টেকনিকেল']
    
    missing = []
    for entity, variants in entity_checks.items():
        found = any(v.lower() in cl for v in variants)
        if not found:
            missing.append(entity)
    
    status_b = "✅" if not missing else "❌"
    print(f"Status: {status_b}")
    if missing:
        print(f"Missing entities: {', '.join(missing)}")
    else:
        print("All key entities present")
    
    # ===== C. Pillar Link =====
    print(f"\n--- C. Pillar-Cluster Alignment ---")
    pillar_pages = [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/blog/mobile-seo-bangladesh-ranking-strategy',
        '/services/technical-seo',
        '/services/local-seo',
        '/services/on-page-seo',
        '/services/ecommerce-seo',
        '/services/geo-ai-search',
        '/',
        '/about',
    ]
    
    found_pillars = [p for p in pillar_pages if p.lower() in content.lower()]
    status_c = "✅" if found_pillars else "❌"
    print(f"Status: {status_c}")
    if found_pillars:
        print(f"Links to pillar: {found_pillars[0]}")
        if len(found_pillars) > 1:
            print(f"Other pillar links: {found_pillars[1:]}")
    else:
        print("No pillar page link found")
    
    # ===== D. AEO/GEO =====
    print(f"\n--- D. AEO/GEO Optimization ---")
    # Count question headings (## or ### starting with question words)
    # Works for both Bangla and English
    q_markers = ['How ', 'What ', 'Why ', 'When ', 'Where ', 'Can ', 'Do ', 'Is ', 'Are ', 'Does ',
                 'কী', 'কেন', 'কিভাবে', 'কীভাবে', 'কোন']
    q_count = 0
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('##') or stripped.startswith('###'):
            for qm in q_markers:
                if qm.lower() in stripped.lower():
                    q_count += 1
                    break
    
    status_d = "✅" if q_count >= 2 else "❌"
    print(f"Status: {status_d} ({q_count} question headings, need >= 2)")
    
    # Also check for FAQ section
    has_faq = 'faq' in content.lower() or 'প্রশ্ন' in content.lower()
    print(f"FAQ section: {'✅' if has_faq else '❌'}")
    
    # ===== E. Internal Links =====
    print(f"\n--- E. Internal Linking ---")
    # Find all [text](/path) patterns
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
    # Filter out anchors and protocol-relative
    internal_links = [(t, u) for t, u in internal_links if not u.startswith('#') and not u.startswith('//')]
    
    print(f"Total internal links: {len(internal_links)}")
    for text, url in internal_links[:15]:
        print(f"  [{text}]({url})")
    if len(internal_links) > 15:
        print(f"  ... and {len(internal_links) - 15} more")
    
    status_e = "✅" if len(internal_links) >= 3 else "❌"
    print(f"Status: {status_e} ({len(internal_links)} internal links, need >= 3)")
    
    # ===== F. Schema =====
    print(f"\n--- F. Schema Ready ---")
    has_title = bool(post.get('title'))
    has_excerpt = bool(post.get('excerpt'))
    has_date = bool(post.get('date'))
    has_metaTitle = post.get('metaTitle', False)
    has_metaDescription = post.get('metaDescription', False)
    has_dateModified = post.get('dateModified', False)
    
    print(f"title: {'✅' if has_title else '❌'}")
    print(f"excerpt: {'✅' if has_excerpt else '❌'}")
    print(f"date: {'✅' if has_date else '❌'}")
    print(f"metaTitle: {'✅' if has_metaTitle else '❌'}")
    print(f"metaDescription: {'✅' if has_metaDescription else '❌'}")
    print(f"dateModified: {'✅' if has_dateModified else '❌'}")
    
    missing_fields = []
    if not has_metaTitle: missing_fields.append('metaTitle')
    if not has_metaDescription: missing_fields.append('metaDescription')
    if not has_dateModified: missing_fields.append('dateModified')
    
    status_f = "✅" if not missing_fields else "❌"
    print(f"Status: {status_f}")
    if missing_fields:
        print(f"Missing: {', '.join(missing_fields)}")
    else:
        print("All ArticleSchema fields present")

print("\n\n" + "=" * 70)
print("FRAMEWORK CHECKS COMPLETE")
