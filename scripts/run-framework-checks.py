#!/usr/bin/env python3
"""Framework check runner for modified blog posts."""

import re
import sys

# Modified post slugs and their line ranges (from git diff analysis)
MODIFIED_POSTS = {
    "mobile-seo-optimization-bangladesh-mobile-first-era": 2250,
    "local-seo-dhaka-google-maps-ranking": 3079,
    "seo-career-guide-bangladesh-2026": 8580,
    "affiliate-seo-bangladesh": 10224,
    "seo-knowledge-panel-bangladesh": 15027,
    "seo-canonical-url-guide-bd": 16321,
    "b2b-lead-generation-seo-bangladesh": 19341,
    "seo-for-fitness-gyms-bangladesh": 19776,
    "seo-healthcare-medical-clinics-bangladesh": 20755,
    "seo-educational-institutions-bangladesh": 21062,
    "seo-travel-tourism-bangladesh": 21391,
    "recovering-google-penalties-bangladesh-guide": 23530,
}

def find_all_slugs():
    """Build a dict of slug -> line number for all posts."""
    slug_map = {}
    with open("src/app/blog/data.js", "r") as f:
        for i, line in enumerate(f, 1):
            m = re.search(r'slug: "([^"]+)"', line)
            if m:
                slug_map[m.group(1)] = i
    return slug_map

def extract_post(slug, slug_map):
    """Extract post metadata and content."""
    start_line = slug_map[slug]
    with open("src/app/blog/data.js", "r") as f:
        lines = f.readlines()

    # Find the next slug to know boundaries
    slugs_sorted = sorted(slug_map.items(), key=lambda x: x[1])
    idx = None
    for i, (s, ln) in enumerate(slugs_sorted):
        if s == slug:
            idx = i
            break
    
    if idx is None:
        return None
    
    if idx + 1 < len(slugs_sorted):
        end_line = slugs_sorted[idx + 1][1]
    else:
        end_line = len(lines) + 1  # last post

    # Extract post lines
    post_lines = lines[start_line - 1 : end_line - 1]
    post_text = "".join(post_lines)

    # Parse metadata
    meta = {}
    for key in ["slug", "title", "date", "author", "excerpt", "tags", "readTime", "imagePlaceholder", "metaTitle", "metaDescription", "dateModified"]:
        m = re.search(rf'{key}:\s*(".*?")(?:,|\s*$)', post_text, re.DOTALL)
        if m:
            val = m.group(1)
            # Handle multi-line excerpts
            if key == "excerpt" and not val.endswith('"'):
                # Find closing quote
                rest = post_text[m.end():]
                m2 = re.search(r'^([^"]*"[^"]*")', rest, re.DOTALL)
                if m2:
                    val = '""'  # complex, skip
            meta[key] = val

    # Extract content (template literal)
    content_match = re.search(r'content:\s*`\n(.*?)`\s*,?\s*\}', post_text, re.DOTALL)
    if not content_match:
        # Try alternative pattern
        content_match = re.search(r'content:\s*`\n(.*?)`\s*\n\s*\}', post_text, re.DOTALL)
    if not content_match:
        content_match = re.search(r'content:\s*`\n(.*?)`', post_text, re.DOTALL)
    
    content = content_match.group(1) if content_match else ""
    
    return meta, content, post_text

def check_tfidf(title, content):
    """Check TF-IDF coverage - count keyword occurrences in content."""
    # Extract primary keyword from title (first meaningful noun phrase)
    title_lower = title.lower()
    
    # Remove common prefixes
    for prefix in ["complete ", "comprehensive ", "ultimate ", "definitive ", "a "]:
        if title_lower.startswith(prefix):
            title_lower = title_lower[len(prefix):]
    
    # Split by colon, take first part
    if ":" in title_lower:
        title_lower = title_lower.split(":")[0].strip()
    
    # Remove trailing filler
    for suffix in [" guide", " strategy", " tips", " techniques", " optimization", " for bangladesh"]:
        if title_lower.endswith(suffix):
            title_lower = title_lower[:-len(suffix)]
    
    # Get the main noun phrase
    words = title_lower.split()
    
    # Try to extract the core keyword
    keywords = set()
    
    # Common patterns: "SEO for X" -> "SEO", "X SEO" -> "SEO", "X for Y" -> "X"
    if "seo" in words:
        keywords.add("seo")
    
    # Add first 2-3 significant words
    stopwords = {"a", "an", "the", "for", "with", "in", "on", "at", "to", "of", "and", "or", "is", "are", "how", "what", "why", "when", "where", "can", "do", "does", "bangladesh", "bangladeshi", "your", "you", "our", "through", "guide", "complete", "comprehensive", "ultimate", "best", "top", "tips", "guide"}
    sig_words = [w for w in words if w not in stopwords and len(w) > 2]
    
    if sig_words:
        # Take first 1-2 as primary keyword
        keyword = " ".join(sig_words[:2])
        keywords.add(keyword)
    
    # For Bangla titles
    if not keywords:
        # Use first non-stopword
        for w in words:
            if len(w) > 1:
                keywords.add(w)
                break
    
    if not keywords:
        keywords.add(words[0] if words else title_lower)
    
    primary_keyword = list(keywords)[0]
    
    # Count occurrences
    content_lower = content.lower()
    count = content_lower.count(primary_keyword)
    
    # For short keywords like "seo", be careful - count in whole words
    if len(primary_keyword) <= 4:
        # Count as whole word only
        count = len(re.findall(r'\b' + re.escape(primary_keyword) + r'\b', content_lower))
    
    return primary_keyword, count, count >= 5

def check_entities(title, content, slug):
    """Check semantic entity coverage."""
    entities_needed = {
        "location": ["dhaka", "bangladesh", "chittagong", "sylhet"],
        "service": ["seo", "local seo", "technical seo", "on-page seo", "google business profile", "content marketing", "link building"],
    }
    
    content_lower = content.lower()
    title_lower = title.lower()
    
    # Always expect Dhaka/Bangladesh
    expected = {
        "dhaka": "location: Dhaka",
        "bangladesh": "location: Bangladesh",
        "seo_mention": "service: SEO",
    }
    
    missing = []
    for key, label in expected.items():
        if key == "dhaka":
            if "dhaka" not in content_lower and "dhaka" not in title_lower:
                missing.append(label)
        elif key == "bangladesh":
            if "bangladesh" not in content_lower and "bangladesh" not in title_lower and "bangladeshi" not in content_lower:
                missing.append(label)
        elif key == "seo_mention":
            if "seo" not in content_lower:
                missing.append(label)
    
    # Post-specific entity checks
    if "healthcare" in slug or "medical" in slug or "clinic" in slug:
        if "patient" not in content_lower:
            missing.append("entity: patient")
        if "doctor" not in content_lower and "clinic" not in content_lower:
            missing.append("entity: doctor/clinic")
    elif "fitness" in slug or "gym" in slug:
        if "gym" not in content_lower and "fitness" not in content_lower:
            missing.append("entity: gym/fitness")
        if "member" not in content_lower:
            missing.append("entity: member")
    elif "education" in slug:
        if "student" not in content_lower:
            missing.append("entity: student")
        if "university" not in content_lower and "college" not in content_lower and "school" not in content_lower:
            missing.append("entity: school/college")
    elif "travel" in slug or "tourism" in slug:
        if "travel" not in content_lower and "tourism" not in content_lower:
            missing.append("entity: travel/tourism")
        if "tourist" not in content_lower and "traveler" not in content_lower:
            missing.append("entity: traveler")
    elif "b2b" in slug or "lead" in slug:
        if "lead" not in content_lower and "b2b" not in content_lower:
            missing.append("entity: B2B/lead")
    elif "penalty" in slug:
        if "penalty" not in content_lower:
            missing.append("entity: penalty")
        if "google" not in content_lower:
            missing.append("entity: Google")
    elif "canonical" in slug:
        if "canonical" not in content_lower:
            missing.append("entity: canonical URL")
        if "duplicate" not in content_lower:
            missing.append("entity: duplicate content")
    elif "affiliate" in slug:
        if "affiliate" not in content_lower:
            missing.append("entity: affiliate")
        if "commission" not in content_lower:
            missing.append("entity: commission")
    elif "career" in slug:
        if "career" not in content_lower and "ক্যারিয়ার" not in content:
            missing.append("entity: career")
        if "salary" not in content_lower and "বেতন" not in content and "আয়" not in content:
            missing.append("entity: salary/income")
    elif "knowledge" in slug or "panel" in slug:
        if "knowledge graph" not in content_lower and "নলেজ" not in content:
            missing.append("entity: knowledge graph")
        if "panel" not in content_lower and "প্যানেল" not in content:
            missing.append("entity: panel")
    
    return missing

def check_pillar_links(tags, content, slug):
    """Check pillar-cluster alignment."""
    # Map tags to pillar topics
    pillar_map = {
        "seo guide": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "bangladesh seo": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "local seo": "/blog/local-seo-tips-dhaka-businesses-google-maps",
        "google maps": "/blog/local-seo-tips-dhaka-businesses-google-maps",
        "technical seo": "/blog/technical-seo-checklist-bangladeshi-websites",
        "mobile seo": "/blog/mobile-seo-optimization-bangladesh-mobile-first-era",
        "mobile optimization": "/blog/mobile-seo-optimization-bangladesh-mobile-first-era",
        "on page seo": "/services/on-page-seo",
        "link building": "/blog/link-building-strategies-bangladesh-market",
        "seo career": "/blog/seo-career-guide-bangladesh-2026",
        "affiliate": "/blog/affiliate-seo-bangladesh",
        "healthcare seo": "/blog/seo-healthcare-medical-clinics-bangladesh",
        "education seo": "/blog/seo-educational-institutions-bangladesh",
        "travel seo": "/blog/seo-travel-tourism-bangladesh",
        "fitness seo": "/blog/seo-for-fitness-gyms-bangladesh",
        "b2b seo": "/blog/b2b-lead-generation-seo-bangladesh",
        "google penalty": "/blog/recovering-google-penalties-bangladesh-guide",
    }
    
    tags_lower = [t.lower() for t in tags]
    pillar_urls = []
    
    for tag, url in pillar_map.items():
        for t in tags_lower:
            if tag in t or t in tag:
                if url not in pillar_urls:
                    pillar_urls.append(url)
    
    # Check if post links to pillar pages
    content_lower = content.lower()
    found_links = []
    missing_links = []
    
    for url in pillar_urls:
        if url.lower() in content_lower:
            found_links.append(url)
        else:
            missing_links.append(url)
    
    return found_links, missing_links

def check_aeo_geo(content):
    """Count question-based headings (How, What, Why, When, Where, Can, Do, Is, Are)."""
    questions = re.findall(r'^##+\s+(How|What|Why|When|Where|Can|Do|Does|Is|Are)\b', content, re.MULTILINE)
    # Also check for question mark headings
    question_headings = re.findall(r'^##+\s+.*\?', content, re.MULTILINE)
    all_questions = set(questions) | set(question_headings)
    return len(all_questions), list(all_questions)

def check_internal_links(content):
    """Count internal links to other posts, services, locations."""
    internal_links = re.findall(r'\[([^\]]+)\]\(((?:/blog/|/services/|/locations/|/about|/contact)[^)]*)\)', content)
    return len(internal_links), internal_links

def check_schema_ready(meta):
    """Check if post has title, excerpt, date set."""
    missing_schema = []
    
    if not meta.get('title') or meta['title'] == '""':
        missing_schema.append("title")
    if not meta.get('excerpt') or meta['excerpt'] == '""':
        missing_schema.append("excerpt")
    if not meta.get('date'):
        missing_schema.append("date")
    
    # Check for metaTitle and metaDescription
    if 'metaTitle' not in meta:
        missing_schema.append("metaTitle (optional but recommended)")
    if 'metaDescription' not in meta:
        missing_schema.append("metaDescription (optional but recommended)")
    
    return missing_schema

def main():
    slug_map = find_all_slugs()
    
    for slug, start_line in sorted(MODIFIED_POSTS.items(), key=lambda x: x[1]):
        print(f"\n{'='*70}")
        print(f"## Post: {slug}")
        print(f"{'='*70}")
        
        result = extract_post(slug, slug_map)
        if result is None:
            print(f"  ERROR: Could not extract post {slug}")
            continue
        
        meta, content, raw = result
        
        # Parse title, tags, etc.
        title_match = re.search(r'title:\s*"([^"]*)"', raw)
        title = title_match.group(1) if title_match else "Unknown"
        
        tags_match = re.search(r'tags:\s*\[(.*?)\]', raw, re.DOTALL)
        tags = []
        if tags_match:
            tags = re.findall(r'"([^"]*)"', tags_match.group(1))
        
        date_match = re.search(r'date:\s*"([^"]*)"', raw)
        date = date_match.group(1) if date_match else "Unknown"
        
        excerpt_match = re.search(r'excerpt:\s*\n?\s*"([^"]*)"', raw, re.DOTALL)
        excerpt = excerpt_match.group(1) if excerpt_match else "Unknown"
        
        print(f"  Title: {title}")
        print(f"  Date: {date}")
        print(f"  Tags: {tags}")
        print(f"  Content length: {len(content)} chars")
        print()
        
        # A. TF-IDF Coverage
        keyword, count, tfidf_ok = check_tfidf(title, content)
        print(f"| TF-IDF: `{keyword}` | {'✅' if tfidf_ok else '❌'} | {count} occurrences |")
        
        # B. Semantic Entity Coverage
        missing_entities = check_entities(title, content, slug)
        if missing_entities:
            print(f"| Entities | ❌ | Missing: {', '.join(missing_entities)} |")
        else:
            print(f"| Entities | ✅ | All expected entities found |")
        
        # C. Pillar-Cluster Alignment
        found_links, missing_links = check_pillar_links(tags, content, slug)
        if missing_links:
            # Check if there's any link to the site root or about page at least
            has_any_pillar = bool(found_links)
            if has_any_pillar:
                print(f"| Pillar Link | ✅ | Links to: {', '.join(found_links)} |")
            else:
                print(f"| Pillar Link | ❌ | No pillar page link found |")
        else:
            print(f"| Pillar Link | ✅ | No missing pillar links |")
        
        # D. AEO/GEO Check
        q_count, q_list = check_aeo_geo(content)
        if q_count < 2:
            print(f"| AEO/GEO | ❌ | {q_count} question heading(s) — need ≥2 |")
        else:
            print(f"| AEO/GEO | ✅ | {q_count} question heading(s) |")
            for q in q_list:
                print(f"    - {q.strip()}")
        
        # E. Internal Linking
        link_count, links = check_internal_links(content)
        if link_count < 3:
            print(f"| Internal Links | ❌ | {link_count} internal link(s) — need ≥3 |")
        else:
            print(f"| Internal Links | ✅ | {link_count} internal link(s) |")
            for text, url in links[:5]:
                print(f"    - [{text}]({url})")
            if len(links) > 5:
                print(f"    ... and {len(links)-5} more")
        
        # F. Schema Ready
        missing_schema = check_schema_ready(meta)
        if missing_schema:
            print(f"| Schema Ready | ❌ | Missing: {', '.join(missing_schema)} |")
        else:
            print(f"| Schema Ready | ✅ | All fields set |")
        
        # Print fix instructions
        print(f"\n### Fix instructions:")
        fixes = []
        
        if not tfidf_ok:
            fixes.append(f"- **TF-IDF**: Add more occurrences of `{keyword}` in the content (currently {count}, need ≥5)")
        
        if missing_entities:
            fixes.append(f"- **Entities**: Add mentions of: {', '.join(missing_entities)}")
        
        if missing_links:
            fixes.append(f"- **Pillar Link**: Add a link to pillar page(s): {', '.join(missing_links)}")
        
        if q_count < 2:
            fixes.append(f"- **AEO/GEO**: Add at least {2 - q_count} more question-based headings (starting with How/What/Why/When/Where/Can/Do/Is/Are)")
        
        if link_count < 3:
            fixes.append(f"- **Internal Links**: Add at least {3 - link_count} more internal links to other blog posts, services, or location pages")
        
        if missing_schema:
            fixes.append(f"- **Schema**: Ensure these fields are set: {', '.join(missing_schema)}")
        
        if not fixes:
            print("  ✅ All checks passed! No fixes needed.")
        else:
            for fix in fixes:
                print(fix)

if __name__ == "__main__":
    main()
