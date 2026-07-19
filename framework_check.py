#!/usr/bin/env python3
"""Framework compliance checker for kanokmiah.com.bd blog posts."""

import re
import json
import sys

# Modified slugs from git diff
MODIFIED_SLUGS = [
    "affiliate-seo-bangladesh",
    "b2b-lead-generation-seo-bangladesh",
    "building-seo-roadmap-bangladesh-business",
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "enterprise-seo-large-organizations-bangladesh",
    "google-tag-manager-seo-bd",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "landlord-certificates-seo-case-study",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "morethanpanel-seo-case-study",
    "seo-audit-checklist-bangladesh",
    "seo-branded-vs-non-branded-bd",
    "seo-canonical-url-guide-bd",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-dashboard-tools-bangladesh",
    "seo-direct-traffic-bangladesh",
    "seo-educational-institutions-bangladesh",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "seo-faq-schema-bangladesh",
    "seo-featured-snippet-bangladesh",
    "seo-for-cleaning-services-bangladesh",
    "seo-for-fitness-gyms-bangladesh",
    "seo-for-restaurants-cafe-dhaka",
    "seo-healthcare-medical-clinics-bangladesh",
    "seo-hreflang-guide-bangladesh",
    "seo-https-ssl-impact-bangladesh",
    "seo-hubspot-vs-wordpress-bd",
    "seo-information-gain-optimization",
    "seo-keyword-clustering-bangladesh",
    "seo-knowledge-panel-bangladesh",
    "seo-legal-compliance-bangladesh",
    "seo-mistakes-to-avoid-bangladesh",
    "seo-non-profit-organizations-bangladesh",
    "seo-passage-ranking-bangladesh",
    "seo-people-also-ask-optimization",
    "seo-photographers-videographers-bangladesh",
    "seo-real-estate-agents-property-developers-bangladesh",
    "seo-redirects-guide-bangladesh",
    "seo-referral-traffic-bangladesh",
    "seo-robots-txt-guide-bangladesh",
    "seo-search-intent-optimization",
    "seo-services-cost-bangladesh-pricing-guide",
    "seo-structured-data-guide-bd",
    "seo-website-migration-guide-bd",
    "seo-wedding-event-planners-bangladesh",
    "seo-xml-sitemap-guide-bd",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "voice-search-seo-bengali-bangladesh",
    "watchzonebd-seo-case-study",
    "website-speed-optimization-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
]

def extract_post_objects(filepath):
    """Extract post objects from data.js using regex parsing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the array content between const posts = [ and ];
    # Use a simple approach: find each { ... } block that contains slug:
    posts = []
    
    # Split by slug: to find start of each post
    # Each post starts with { and has slug: "...",
    # Simple extraction: find blocks starting with { and ending with },
    
    # Use regex to find slug values and their surrounding blocks
    slug_pattern = re.compile(r'^\s*slug:\s*"([^"]+)"', re.MULTILINE)
    
    # Get all slug positions
    matches = list(slug_pattern.finditer(content))
    
    for i, match in enumerate(matches):
        slug = match.group(1)
        start = match.start()
        
        # Find the start of this post object (the { before slug)
        obj_start = content.rfind('{', 0, start)
        
        # Find end of this post object
        if i + 1 < len(matches):
            obj_end = content.rfind('{', 0, matches[i+1].start())
            # Actually, the next post starts with { before its slug
            # So let's find the { before the next slug
            next_start = content.rfind('{', 0, matches[i+1].start())
            obj_end = next_start
        else:
            # Last post - find the end of the array
            obj_end = content.rfind('];')
            if obj_end == -1:
                obj_end = len(content)
        
        # Extract this post's text
        post_text = content[obj_start:obj_end]
        posts.append((slug, post_text))
    
    return posts

def extract_field(post_text, field_name):
    """Extract a field value from post text. Works for simple string values."""
    # Pattern for fields like: fieldName: "value",
    pattern = re.compile(rf'{field_name}:\s*"((?:[^"\\]|\\.)*)"', re.DOTALL)
    match = pattern.search(post_text)
    if match:
        return match.group(1)
    
    # Pattern for fields like: tags: [...],
    array_pattern = re.compile(rf'{field_name}:\s*\[(.*?)\]', re.DOTALL)
    match = array_pattern.search(post_text)
    if match:
        return match.group(1)
    
    return None

def extract_content(post_text):
    """Extract the content field (template literal)."""
    # Content starts with content: ` and ends with `,
    pattern = re.compile(r'content:\s*`(.*?)`\s*,?\s*\}', re.DOTALL)
    match = pattern.search(post_text)
    if match:
        return match.group(1)
    
    # Try without trailing comma
    pattern2 = re.compile(r'content:\s*`(.*?)`\s*\}', re.DOTALL)
    match = pattern2.search(post_text)
    if match:
        return match.group(1)
    
    return ""

def extract_faqs(post_text):
    """Extract FAQ items if present."""
    # Look for faq: [{...}]
    pattern = re.compile(r'faq:\s*\[(.*?)\]', re.DOTALL)
    match = pattern.search(post_text)
    if match:
        return match.group(1)
    return ""

def run_checks(slug, title, excerpt, date, tags_str, content, post_text):
    """Run all framework checks on a post."""
    results = {}
    
    # --- A. TF-IDF Coverage ---
    # Extract first meaningful noun phrase from title (first 2-3 words excluding stop words)
    stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'is', 'and', 'or', 'vs', 'vs.', 'your', 'our', 'its', 'their', 'this', 'that', 'are', 'be', 'has', 'have', 'not', 'with', 'from', 'at', 'by', 'on', 'it', 'as', 'but'}
    title_lower = title.lower() if title else slug.replace('-', ' ')
    
    # For SEO-oriented posts, extract the core topic
    # Remove common prefixes
    clean_title = title_lower if title else slug.replace('-', ' ')
    
    words = clean_title.split()
    # Take first 2-4 meaningful words as keyword phrase
    keyword_parts = []
    for w in words:
        w_clean = w.strip('.,;:!?"\'()[]{}')
        if w_clean not in stop_words and len(w_clean) > 1:
            keyword_parts.append(w_clean)
            if len(keyword_parts) >= 3:
                break
    
    # Prefer the slug-derived topic if it's SEO-oriented
    # Actually, let's derive from the title/slug semantic meaning
    if not keyword_parts:
        keyword_parts = words[:3]
    
    primary_keyword = ' '.join(keyword_parts[:2])
    
    # Count occurrences in content (case-insensitive)
    if content:
        content_lower = content.lower()
        # Count exact phrase
        phrase_count = content_lower.count(primary_keyword.lower())
        # Also count individual keyword parts
        word_counts = {}
        for kp in keyword_parts:
            word_counts[kp] = content_lower.count(kp.lower())
        
        # Use max of phrase count or individual word counts
        effective_count = max(phrase_count, max(word_counts.values()) if word_counts else 0)
    else:
        effective_count = 0
    
    tfidf_pass = effective_count >= 5
    results['tfidf'] = {
        'keyword': primary_keyword,
        'count': effective_count,
        'pass': tfidf_pass
    }
    
    # --- B. Semantic Entity Coverage ---
    entities = {
        'location_bd': 'Bangladesh',
        'location_dhaka': 'Dhaka',
        'service_seo': 'SEO',
    }
    
    # Detect entities from content
    content_lower_for_entities = content.lower() if content else ''
    
    entity_results = {}
    missing_entities = []
    
    # Check Bangladesh
    if 'bangladesh' in content_lower_for_entities or 'bangladesh' in str(tags_str).lower():
        entity_results['🇧🇩 Bangladesh'] = True
    else:
        entity_results['🇧🇩 Bangladesh'] = False
        missing_entities.append('Bangladesh (location)')
    
    # Check Dhaka
    if 'dhaka' in content_lower_for_entities:
        entity_results['🏙️ Dhaka'] = True
    else:
        entity_results['🏙️ Dhaka'] = False
        missing_entities.append('Dhaka (location)')
    
    # Check for service type mention based on tags
    tags_lower = tags_str.lower() if tags_str else ''
    service_terms = {
        'local seo': 'local seo',
        'technical seo': 'technical seo',
        'on-page seo': 'on-page seo',
        'off-page seo': 'off-page seo',
        'ecommerce seo': 'ecommerce',
        'link building': 'link building',
        'content marketing': 'content marketing',
        'keyword research': 'keyword research',
        'google business profile': 'google business profile',
        'geo': 'geo',
        'enterprise seo': 'enterprise',
        'mobile seo': 'mobile seo',
        'voice search': 'voice search',
    }
    
    services_found = []
    for term, label in service_terms.items():
        if term in content_lower_for_entities or term in tags_lower:
            services_found.append(label)
    
    entity_results['📋 Service type'] = bool(services_found)
    if not services_found:
        missing_entities.append('Service type mention')
    
    # Check for industry/vertical mention
    industry_terms = [
        'business', 'industry', 'sme', 'small business', 'enterprise',
        'e-commerce', 'ecommerce', 'retail', 'garment', 'textile',
        'real estate', 'healthcare', 'medical', 'restaurant', 'hotel',
        'law firm', 'legal', 'fitness', 'gym', 'ngo', 'non-profit',
        'education', 'photographer', 'videographer', 'wedding', 'event'
    ]
    industries_found = [t for t in industry_terms if t in content_lower_for_entities]
    entity_results['🏢 Industry mention'] = bool(industries_found)
    if not industries_found:
        missing_entities.append('Industry/vertical mention')
    
    entity_pass = len(missing_entities) == 0
    results['entities'] = {
        'pass': entity_pass,
        'found': entity_results,
        'missing': missing_entities,
        'services_found': services_found,
        'industries_found': industries_found
    }
    
    # --- C. Pillar-Cluster Alignment ---
    # Determine pillar from tags
    tags_lower = tags_str.lower() if tags_str else ''
    
    pillar_map = {
        'seo guide': 'complete-seo-guide-bangladesh-businesses-2026',
        'bangladesh seo': 'complete-seo-guide-bangladesh-businesses-2026',
        'technical seo': 'technical-seo-checklist-bangladeshi-websites',
        'local seo': 'local-seo-tips-dhaka-businesses-google-maps',
        'link building': 'link-building-strategies-bangladesh-market',
        'keyword research': 'keyword-research-bangladesh-market',
        'content marketing': 'content-marketing-seo-friendly-content-writing',
        'on-page seo': 'on-page-seo-guide-bangladesh-2026',
        'ecommerce': 'why-ecommerce-store-needs-seo-bangladesh',
        'google business profile': 'google-business-profile-optimization-guide-bangladesh',
        'mobile seo': 'mobile-seo-bangladesh-ranking-strategy',
        'core web vitals': 'technical-seo-core-web-vitals-optimization',
        'schema': 'schema-markup-rich-snippets-techniques',
        'structured data': 'schema-markup-rich-snippets-techniques',
        'enterprise': 'enterprise-seo-large-organizations-bangladesh',
        'geo': 'geo-optimization-prepare-business-ai-search',
        'ai search': 'geo-optimization-prepare-business-ai-search',
        'voice search': 'voice-search-seo-bengali-bangladesh',
        'seo services': 'seo-services-cost-bangladesh-pricing-guide',
    }
    
    # Check which pillar page this post might link to
    if content:
        # Look for /blog/ links
        blog_links = re.findall(r'/blog/([^"\')\s]+)', content)
        # Look for /services/ links
        service_links = re.findall(r'/services/([^"\')\s]+)', content)
        # Look for /locations/ links
        location_links = re.findall(r'/locations/([^"\')\s]+)', content)
        
        # Check if any of the known pillar slug patterns appear in the content
        pillar_slugs = set(pillar_map.values())
        linked_pillars = [l for l in blog_links if l in pillar_slugs]
    else:
        blog_links = []
        service_links = []
        location_links = []
        linked_pillars = []
    
    # Determine which pillar this post likely belongs to
    assigned_pillar = None
    for tag_term, pillar_slug in pillar_map.items():
        if tag_term in tags_lower:
            assigned_pillar = pillar_slug
            break
    
    # Check if post has an explicit link to its pillar page
    has_pillar_link = False
    if assigned_pillar and content:
        # Check for direct link to pillar
        has_pillar_link = f'/blog/{assigned_pillar}' in content
    
    results['pillar'] = {
        'assigned_pillar': assigned_pillar,
        'has_pillar_link': has_pillar_link,
        'linked_pillars': linked_pillars,
        'all_blog_links': blog_links,
        'service_links': service_links,
        'location_links': location_links,
    }
    
    # --- D. AEO/GEO Optimization ---
    q_markers = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who']
    if content:
        # Find all h2/h3 headings
        headings = re.findall(r'#{2,3}\s+(.+?)(?:\n|$)', content)
        question_headings = []
        for h in headings:
            h_stripped = h.strip().rstrip('?')
            for marker in q_markers:
                if h_stripped.startswith(marker) or h_stripped.startswith(marker + ' '):
                    question_headings.append(h_stripped)
                    break
                # Also check Bengali Q markers
                if any(h_stripped.startswith(bq) for bq in ['কী', 'কেন', 'কিভাবে', 'কখন', 'কোথায়', 'কোন']):
                    question_headings.append(h_stripped)
                    break
    else:
        question_headings = []
    
    aeo_pass = len(question_headings) >= 2
    results['aeo'] = {
        'pass': aeo_pass,
        'question_headings': question_headings,
        'count': len(question_headings)
    }
    
    # --- E. Internal Linking ---
    if content:
        # Internal links to /blog/, /services/, /locations/, /about, /contact
        internal_links = set()
        # Blog links
        for link in re.findall(r'/blog/[^"\')\s]+', content):
            internal_links.add(link)
        # Service links
        for link in re.findall(r'/services/[^"\')\s]+', content):
            internal_links.add(link)
        # Location links
        for link in re.findall(r'/locations/[^"\')\s]+', content):
            internal_links.add(link)
        # Other internal links
        for link in re.findall(r'"/[^"\']+"', content):
            clean = link.strip('"\'')
            if clean in ['/about', '/contact', '/', '/blog', '/services', '/locations']:
                internal_links.add(clean)
            elif clean.startswith('/about') or clean.startswith('/contact'):
                internal_links.add(clean)
        
        # Also check for markdown-style links
        for match in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content):
            link_url = match[1]
            if link_url.startswith('/') or link_url.startswith('https://kanokmiah.com.bd'):
                internal_links.add(link_url)
    else:
        internal_links = set()
    
    internal_pass = len(internal_links) >= 3
    results['internal_links'] = {
        'pass': internal_pass,
        'links': sorted(internal_links),
        'count': len(internal_links)
    }
    
    # --- F. Schema Ready ---
    schema_fields = {'title': title, 'excerpt': excerpt, 'date': date}
    missing_schema = [k for k, v in schema_fields.items() if not v]
    # Also check dateModified
    date_modified = extract_field(post_text, 'dateModified')
    if not date_modified and 'dateModified' not in post_text:
        missing_schema.append('dateModified (recommended)')
    
    schema_pass = len([m for m in missing_schema if m != 'dateModified (recommended)']) == 0
    results['schema'] = {
        'pass': schema_pass,
        'fields': schema_fields,
        'date_modified': date_modified,
        'missing': missing_schema
    }
    
    return results


def main():
    filepath = '/root/kanok-miahit/src/app/blog/data.js'
    
    posts = extract_post_objects(filepath)
    print(f"Extracted {len(posts)} posts from data.js")
    
    slug_map = {s: t for s, t in posts}
    
    slug_list = MODIFIED_SLUGS
    
    # Read the full file for fallback extraction
    with open(filepath, 'r', encoding='utf-8') as f:
        full_content = f.read()
    
    for slug in slug_list:
        if slug not in slug_map:
            print(f"\n⚠️  Post '{slug}' not found via parser, trying direct search...")
            # Try to find it in the full content
            idx = full_content.find(f'slug: "{slug}"')
            if idx >= 0:
                # Find the start of this post object
                obj_start = full_content.rfind('{', 0, idx)
                # Find the end (next { before another slug, or end of array)
                next_slug = full_content.find('slug: "', idx + 1)
                if next_slug >= 0:
                    obj_end = full_content.rfind('{', 0, next_slug)
                else:
                    obj_end = full_content.rfind('];')
                post_text = full_content[obj_start:obj_end]
                slug_map[slug] = post_text
            else:
                print(f"  ❌ Could not find post '{slug}' in data.js")
                continue
        
        post_text = slug_map[slug]
        if not post_text:
            print(f"\n⚠️  Empty post text for '{slug}'")
            continue
        
        # Extract fields
        title = extract_field(post_text, 'title')
        excerpt = extract_field(post_text, 'excerpt')
        date = extract_field(post_text, 'date')
        tags_str = extract_field(post_text, 'tags')
        content = extract_content(post_text)
        
        print(f"\n{'='*60}")
        print(f"📝 Post: {slug}")
        print(f"   Title: {title[:80] if title else 'N/A'}...")
        print(f"   Content length: {len(content) if content else 0} chars")
        
        if not content or len(content) < 50:
            print("   ⚠️  Content too short or not extracted, trying raw extraction...")
            # Fallback: try to get content from post_text directly
            content_match = re.search(r'content:\s*`', post_text)
            if content_match:
                content_start = content_match.end()
                # Find the closing backtick
                end_match = re.search(r'`\s*,?\s*\}', post_text[content_start-1:])
                if end_match:
                    content = post_text[content_start-1:content_start-1+end_match.start()]
        
        if not content or len(content) < 50:
            print("   ❌ Could not extract content, skipping checks")
            continue
        
        results = run_checks(slug, title, excerpt, date, tags_str, content, post_text)
        
        # --- REPORT ---
        print(f"\n## Post: {slug}")
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        
        # TF-IDF
        r = results['tfidf']
        status = '✅' if r['pass'] else '❌'
        print(f"| TF-IDF: \"{r['keyword']}\" | {status} | {r['count']} occurrences |")
        
        # Entities
        r = results['entities']
        status = '✅' if r['pass'] else '❌'
        missing_str = ', '.join(r['missing']) if r['missing'] else 'None'
        found_str = []
        for k, v in r['found'].items():
            mark = '✅' if v else '❌'
            found_str.append(f"{mark} {k}")
        print(f"| Entities | {status} | Missing: {missing_str} |")
        print(f"|   └ Details | | {' | '.join(found_str)} |")
        if r['services_found']:
            print(f"|   └ Services | | {', '.join(r['services_found'][:5])} |")
        
        # Pillar
        r = results['pillar']
        status = '✅' if r['has_pillar_link'] else '❌'
        pillar_info = r['assigned_pillar'] or 'Not determined'
        has_link = r['has_pillar_link']
        print(f"| Pillar Link | {status} | Assigned: {pillar_info} |")
        print(f"|   └ Links to pillar? | {'✅' if has_link else '❌'} | Linked from content: {has_link} |")
        
        # AEO/GEO
        r = results['aeo']
        status = '✅' if r['pass'] else '❌'
        q_heads = r['question_headings']
        print(f"| AEO/GEO | {status} | {r['count']} question headings |")
        if q_heads:
            for q in q_heads[:5]:
                print(f"|   └ | | \"{q[:60]}\" |")
        
        # Internal Links
        r = results['internal_links']
        status = '✅' if r['pass'] else '❌'
        print(f"| Internal Links | {status} | {r['count']} total |")
        if r['links']:
            for link in sorted(r['links'])[:8]:
                print(f"|   └ | | {link} |")
        
        # Schema
        r = results['schema']
        status = '✅' if r['pass'] else '❌'
        print(f"| Schema Ready | {status} | Missing: {', '.join(r['missing']) if r['missing'] else 'All set'} |")
        
        # Fix instructions
        print(f"\n### Fix instructions:")
        fixes = []
        if not results['tfidf']['pass']:
            fixes.append(f"- 🔍 TF-IDF: Keyword \"{results['tfidf']['keyword']}\" appears only {results['tfidf']['count']}x. Add more semantic variations and repeat the core keyword phrase throughout the post (aim for ≥5).")
        if not results['entities']['pass']:
            fixes.append(f"- 🏷️ Entities: Missing {', '.join(results['entities']['missing'])}. Add location/industry mentions naturally in the content.")
        if not results['pillar']['has_pillar_link']:
            fixes.append(f"- 🔗 Pillar Link: No link found to pillar page \"{results['pillar']['assigned_pillar'] or 'unknown'}\". Add a contextual link to the pillar page.")
        if not results['aeo']['pass']:
            fixes.append(f"- ❓ AEO/GEO: Only {results['aeo']['count']} question heading(s). Add ≥2 question-based H2/H3 (How, What, Why, etc.) for voice/AI search optimization.")
        if not results['internal_links']['pass']:
            fixes.append(f"- 🔗 Internal Links: Only {results['internal_links']['count']} internal link(s). Add ≥3 links to other blog posts, services, or location pages.")
        if not results['schema']['pass']:
            missing = results['schema']['missing']
            if missing:
                fixes.append(f"- 📋 Schema: Missing {', '.join(missing)}. Ensure title, excerpt, date, and dateModified are set.")
        
        if not fixes:
            print("✅ All checks passed! No fixes needed.")
        else:
            for fix in fixes:
                print(fix)
        print()

if __name__ == '__main__':
    main()
