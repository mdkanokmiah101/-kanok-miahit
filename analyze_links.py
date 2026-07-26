#!/usr/bin/env python3
"""
Analyze Internal Linking & Technical SEO for all blog posts in data.js
"""
import re
import json

# Read the file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Known blog slugs for broken link checking
known_slugs = [
    "complete-seo-guide-bangladesh-businesses-2026",
    "local-seo-tips-dhaka-businesses-google-maps",
    "why-ecommerce-store-needs-seo-bangladesh",
    "technical-seo-checklist-bangladeshi-websites",
    "how-to-choose-right-seo-agency-bangladesh",
    "link-building-strategies-bangladesh-market",
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "seo-real-estate-developers-dhaka",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "international-seo-bangladesh-exporters-global-buyers",
    "seo-bangla-beginners-guide-google-ranking",
    "local-seo-dhaka-google-maps-ranking",
    "seo-trends-2026-ai-geo-future",
    "technical-seo-core-web-vitals-optimization",
    "ecommerce-seo-daraz-shopify-guide",
    "link-building-bangladesh-strategies",
    "keyword-research-bangladesh-market",
    "content-marketing-seo-friendly-content-writing",
    "google-search-console-performance-guide",
    "mobile-seo-bangladesh-ranking-strategy",
    "schema-markup-rich-snippets-techniques",
    "youtube-seo-bangladesh-ranking-tips",
    "seo-vs-google-ads-bangladesh-business",
    "seo-bangla-blog-content-writing",
    "seo-tips-for-business-owners-bd",
    "long-tail-keywords-bangladesh",
    "seo-for-facebook-marketplace",
    "seo-for-youtube-channel-bangla",
    "seo-google-updates-2026",
    "seo-semantic-search-bangla",
    "seo-for-hotel-resort-bangladesh",
    "seo-google-business-profile-posts",
    "seo-local-citations-bangladesh",
    "seo-for-ngo-bangladesh",
    "seo-career-guide-bangladesh-2026",
    "seo-consultant-dhaka-bangladesh",
    "google-my-business-optimization-bangladesh",
    "seo-for-new-website-bangladesh",
    "website-speed-optimization-bangladesh",
    "seo-audit-checklist-bangladesh",
    "affiliate-seo-bangladesh",
    "voice-search-seo-bangladesh",
    "seo-legal-compliance-bangladesh",
    "seo-for-restaurants-cafe-dhaka",
    "seo-for-cleaning-services-bangladesh",
    "seo-dashboard-tools-bangladesh",
    "seo-mistakes-to-avoid-bangladesh",
    "seo-website-migration-guide-bd",
    "google-tag-manager-seo-bd",
    "seo-google-analytics-4-bangladesh",
    "seo-keyword-clustering-bangladesh",
    "seo-competitor-analysis-bangladesh",
    "seo-landing-page-optimization-bd",
    "seo-for-mobile-apps-bangladesh",
    "google-discover-seo-bangladesh",
    "seo-for-podcast-bangladesh",
    "seo-pillar-content-strategy-bd",
    "seo-skyscraper-technique-bangladesh",
    "seo-content-repurposing-bangladesh",
    "seo-hubspot-vs-wordpress-bd",
    "seo-domain-authority-bangladesh",
    "seo-page-authority-bangladesh",
    "seo-referral-traffic-bangladesh",
    "seo-direct-traffic-bangladesh",
    "seo-branded-vs-non-branded-bd",
    "seo-search-intent-optimization",
    "seo-information-gain-optimization",
    "seo-passage-ranking-bangladesh",
    "seo-people-also-ask-optimization",
    "seo-featured-snippet-bangladesh",
    "seo-knowledge-panel-bangladesh",
    "seo-zero-click-search-bangladesh",
    "seo-google-penalty-recovery-bd",
    "seo-https-ssl-impact-bangladesh",
    "seo-redirects-guide-bangladesh",
    "seo-canonical-url-guide-bd",
    "seo-robots-txt-guide-bangladesh",
    "seo-xml-sitemap-guide-bd",
    "seo-hreflang-guide-bangladesh",
    "seo-structured-data-guide-bd",
    "seo-json-ld-schema-bangladesh",
    "seo-breadcrumb-schema-bd",
    "seo-faq-schema-bangladesh",
    "seo-howto-schema-bangladesh",
    "seo-for-startups-bangladesh",
    "voice-search-seo-bengali-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "locksmith-dundee-seo-case-study",
    "landlord-certificates-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "watchzonebd-seo-case-study",
]

known_slug_set = set(known_slugs)

# Parse posts from the JS file
# Strategy: Find each post object by looking for "slug:" patterns, then extract the content between braces
# We need to handle backtick template strings properly

def parse_posts_js(text):
    """Parse posts array from JavaScript file."""
    posts = []
    
    # Find all slug occurrences with their positions
    slug_pattern = re.compile(r'^\s{4}slug:\s*"([^"]+)"', re.MULTILINE)
    slug_matches = list(slug_pattern.finditer(text))
    
    print(f"Found {len(slug_matches)} slug entries")
    
    for i, match in enumerate(slug_matches):
        slug = match.group(1)
        start_pos = match.start()
        
        # Find the start of this post object (the opening '{')
        # Go backwards from slug to find '{'
        brace_start = text.rfind('{', 0, start_pos)
        
        # Find the end of this post object
        # We need to balance braces AND handle backtick template strings
        if i + 1 < len(slug_matches):
            next_start = slug_matches[i + 1].start()
            # Find the preceding '{' of the next post
            brace_end = text.rfind('{', 0, next_start)
            # The current post ends just before the next post starts
            # Go back from next_start to find the closing '}' of current post
            # Actually, we need to find the '},' or '}' that closes this post
            # The next post starts with '  {', so current post ends at '  },' before it
            end_pos = text.rfind('\n  }', brace_start, next_start)
            if end_pos == -1:
                end_pos = text.rfind('}', brace_start, next_start)
            if end_pos != -1:
                end_pos += 3  # include '  }'
        else:
            # Last post - find '];' at end
            end_pos = text.find('\n];', start_pos)
        
        if brace_start >= 0 and end_pos > brace_start:
            post_text = text[brace_start:end_pos]
            posts.append({
                'slug': slug,
                'text': post_text,
                'start': brace_start,
                'end': end_pos,
            })
    
    return posts


def extract_content_from_post_text(post_text):
    """Extract the content template string from a post object text."""
    # Find content: `
    content_start = post_text.find('content: `')
    if content_start == -1:
        return ""
    
    content_start += len('content: `')
    
    # Find the closing backtick - it's the last backtick before the end of the post
    # The content ends with `,
    # Look for `, (backtick followed by comma and possibly newline)
    # But first let's find the last backtick in the post text
    content_end = post_text.rfind('`')
    if content_end <= content_start:
        return ""
    
    return post_text[content_start:content_end]


def count_links(content, slug):
    """Count internal and external links in content."""
    # Find all markdown links: [text](url) and plain URLs (http://...)
    
    # Internal links: [text](/path...) or just /path
    # We look for markdown link patterns [text](url) where url starts with /
    internal_links = []
    external_links = []
    all_links = []
    
    # Find markdown links [text](url)
    md_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    for text, url in md_links:
        url = url.strip()
        if url.startswith('/'):
            internal_links.append(url)
            all_links.append(url)
        elif url.startswith('http://') or url.startswith('https://'):
            # Check if it's a same-domain link (kanokmiah.com)
            if 'kanokmiah' in url.lower() or 'kanok-miah' in url.lower():
                # Extract the path from the URL
                path_match = re.match(r'https?://[^/]+(/.*)', url)
                if path_match:
                    internal_links.append(path_match.group(1))
            else:
                external_links.append(url)
            all_links.append(url)
    
    # Also find bare URLs that might not be in markdown format
    bare_urls = re.findall(r'(?<!\]\()(https?://[^\s\)\"\']+)', content)
    for url in bare_urls:
        # Skip URLs already counted (inside markdown)
        if url not in external_links:
            if 'kanokmiah' in url.lower() or 'kanok-miah' in url.lower():
                path_match = re.match(r'https?://[^/]+(/.*)', url)
                if path_match:
                    internal_links.append(path_match.group(1))
            else:
                external_links.append(url)
            all_links.append(url)
    
    # Categorize internal links
    categorized = {
        '/blog/*': [],
        '/services/*': [],
        '/industries/*': [],
        '/locations/*': [],
        '/about': [],
        '/contact': [],
        '/': [],
        'other': [],
    }
    
    blog_internal_links = []
    for link in internal_links:
        if link.startswith('/blog/'):
            categorized['/blog/*'].append(link)
            blog_internal_links.append(link)
        elif link.startswith('/services/'):
            categorized['/services/*'].append(link)
        elif link.startswith('/industries/'):
            categorized['/industries/*'].append(link)
        elif link.startswith('/locations/'):
            categorized['/locations/*'].append(link)
        elif link == '/about':
            categorized['/about'].append(link)
        elif link == '/contact':
            categorized['/contact'].append(link)
        elif link == '/':
            categorized['/'].append(link)
        else:
            categorized['other'].append(link)
    
    # Count broken blog links (links starting with /blog/ that don't point to valid slugs)
    broken_blog_links = []
    for link in blog_internal_links:
        # Extract slug from /blog/slug-name
        path = link
        if path.startswith('/blog/'):
            link_slug = path[len('/blog/'):]
            # Remove trailing slash if any
            link_slug = link_slug.rstrip('/')
            if link_slug not in known_slug_set:
                broken_blog_links.append(link)
    
    # Count missing blog prefix links
    # Links that look like blog post slugs (match known slugs) but don't have /blog/ prefix
    missing_blog_prefix = []
    for link in internal_links:
        link_path = link.rstrip('/')
        # Check if the path (possibly with leading /) matches a known slug directly
        if link_path.startswith('/'):
            candidate = link_path[1:]  # remove leading /
        else:
            candidate = link_path
        if candidate in known_slug_set and not link.startswith('/blog/'):
            missing_blog_prefix.append(link)
    
    # Count words in content for link density
    # Strip markdown syntax for word count
    clean_text = re.sub(r'[#*_\[\]()>|`\-]', ' ', content)
    words = clean_text.split()
    word_count = len(words)
    
    total_links = len(internal_links) + len(external_links)
    link_density = round(total_links / word_count * 100, 2) if word_count > 0 else 0
    
    return {
        'internal_links': internal_links,
        'external_links': external_links,
        'internal_count': len(internal_links),
        'external_count': len(external_links),
        'categorized': categorized,
        'broken_blog_links': broken_blog_links,
        'broken_blog_count': len(broken_blog_links),
        'missing_blog_prefix': missing_blog_prefix,
        'missing_blog_prefix_count': len(missing_blog_prefix),
        'total_links': total_links,
        'word_count': word_count,
        'link_density': link_density,
    }


# Parse the posts
posts = parse_posts_js(content)
print(f"Parsed {len(posts)} posts")

# Process each post
results = []
for post in posts:
    slug = post['slug']
    post_text = post['text']
    content_str = extract_content_from_post_text(post_text)
    
    if not content_str:
        print(f"WARNING: No content found for {slug}")
        continue
    
    analysis = count_links(content_str, slug)
    
    is_linking_gap = analysis['internal_count'] <= 1
    
    results.append({
        'slug': slug,
        'internal_count': analysis['internal_count'],
        'external_count': analysis['external_count'],
        'categorized': analysis['categorized'],
        'broken_blog_count': analysis['broken_blog_count'],
        'broken_blog_links': analysis['broken_blog_links'],
        'link_density': analysis['link_density'],
        'total_links': analysis['total_links'],
        'word_count': analysis['word_count'],
        'is_linking_gap': is_linking_gap,
        'missing_blog_prefix_count': analysis['missing_blog_prefix_count'],
        'missing_blog_prefix': analysis['missing_blog_prefix'],
        'internal_links': analysis['internal_links'],
        'external_links': analysis['external_links'],
    })

# Output results
print("\n" + "="*120)
print("ANALYSIS RESULTS")
print("="*120)

# Header
print(f"{'slug':<60}|{'int_links':<10}|{'ext_links':<10}|{'broken':<8}|{'link_density':<12}|{'gap_0or1':<10}|{'missing_prefix':<15}")
print("-"*120)

posts_with_gaps = []
posts_with_missing_prefix = []
all_broken_links = []

for r in results:
    gap_flag = 'YES' if r['is_linking_gap'] else ''
    print(f"{r['slug']:<60}|{r['internal_count']:<10}|{r['external_count']:<10}|{r['broken_blog_count']:<8}|{r['link_density']:<12}|{gap_flag:<10}|{r['missing_blog_prefix_count']:<15}")
    
    if r['is_linking_gap']:
        posts_with_gaps.append(r['slug'])
    if r['missing_blog_prefix_count'] > 0:
        posts_with_missing_prefix.append(r['slug'])
    for bl in r['broken_blog_links']:
        all_broken_links.append((r['slug'], bl))

print("\n" + "="*120)
print("ALL KNOWN BLOG SLUGS (106)")
print("="*120)
for s in known_slugs:
    print(s)

print("\n" + "="*120)
print("POSTS WITH 0 OR 1 INTERNAL LINKS (LINKING GAPS)")
print("="*120)
for s in posts_with_gaps:
    print(s)
print(f"Total: {len(posts_with_gaps)}")

print("\n" + "="*120)
print("POSTS WITH MISSING BLOG PREFIX LINKS")
print("="*120)
for r in results:
    if r['missing_blog_prefix_count'] > 0:
        print(f"{r['slug']}: {r['missing_blog_prefix']}")
print(f"Total posts with missing prefix: {len(posts_with_missing_prefix)}")

print("\n" + "="*120)
print("BROKEN BLOG LINKS")
print("="*120)
for source, link in all_broken_links:
    print(f"  {source} -> {link}")
if not all_broken_links:
    print("  None found!")
print(f"Total broken links: {len(all_broken_links)}")

print("\n" + "="*120)
print("SUMMARY STATISTICS")
print("="*120)
total_posts = len(results)
total_internal = sum(r['internal_count'] for r in results)
total_external = sum(r['external_count'] for r in results)
total_broken = sum(r['broken_blog_count'] for r in results)
total_missing_prefix = sum(r['missing_blog_prefix_count'] for r in results)
avg_link_density = sum(r['link_density'] for r in results) / total_posts if total_posts > 0 else 0

print(f"Total posts analyzed: {total_posts}")
print(f"Total internal links: {total_internal}")
print(f"Total external links: {total_external}")
print(f"Total broken blog links: {total_broken}")
print(f"Total missing blog prefix: {total_missing_prefix}")
print(f"Average link density: {avg_link_density:.2f} links per 100 words")
print(f"Posts with 0 or 1 internal links (gaps): {len(posts_with_gaps)}")
print(f"Posts with missing blog prefix: {len(posts_with_missing_prefix)}")

# Category breakdown
cat_totals = {}
for r in results:
    for cat, links in r['categorized'].items():
        cat_totals[cat] = cat_totals.get(cat, 0) + len(links)
print(f"\nInternal link category breakdown:")
for cat, count in sorted(cat_totals.items()):
    print(f"  {cat}: {count}")

# Also output a JSON file for reference
with open('/root/kanok-miahit/link_analysis_results.json', 'w') as f:
    json.dump({
        'posts': results,
        'summary': {
            'total_posts': total_posts,
            'total_internal': total_internal,
            'total_external': total_external,
            'total_broken': total_broken,
            'total_missing_prefix': total_missing_prefix,
            'avg_link_density': avg_link_density,
            'posts_with_gaps': posts_with_gaps,
            'posts_with_missing_prefix': posts_with_missing_prefix,
            'gap_count': len(posts_with_gaps),
            'missing_prefix_count': len(posts_with_missing_prefix),
        },
        'known_slugs': known_slugs,
    }, f, indent=2)

print("\n\nDetailed results saved to link_analysis_results.json")
