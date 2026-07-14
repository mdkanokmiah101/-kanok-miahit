#!/usr/bin/env python3
"""Technical SEO & Content Audit for kanokmiah.com"""
import requests
import re
import json
import sys
from collections import OrderedDict
from html.parser import HTMLParser
from urllib.parse import urlparse

BASE_URL = "https://kanokmiah.com"
API_BASE = f"{BASE_URL}/wp-json/wp/v2"
AUTH = ("KM856W2s", "f44#%W@$%ffefr4dS")

# ----- H1 extraction -----
class H1Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1s = []
        self.in_h1 = False
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'h1':
            self.in_h1 = True
            self._text = []
    def handle_endtag(self, tag):
        if tag.lower() == 'h1' and self.in_h1:
            self.in_h1 = False
            self.h1s.append(''.join(self._text).strip())
    def handle_data(self, data):
        if self.in_h1:
            self._text.append(data)

def extract_h1(html_content):
    parser = H1Extractor()
    parser.feed(html_content)
    return parser.h1s

def extract_meta_description(html_content):
    """Try to find meta description in rendered content or excerpt."""
    # Check for yoast/rankmath meta tags in raw content
    m = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)', html_content)
    if m:
        return m.group(1)
    # Check for description in the excerpt
    return None

def strip_html(html):
    clean = re.sub(r'<[^>]+>', ' ', html)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def word_count(text):
    return len(text.split())

def fetch_all(endpoint, per_page=100):
    """Fetch all items from a paginated WP REST API endpoint."""
    items = []
    page = 1
    while True:
        url = f"{API_BASE}/{endpoint}?per_page={per_page}&page={page}&_fields=id,slug,link,title,content,excerpt,meta,type,status,date,modified"
        resp = requests.get(url, auth=AUTH, timeout=30)
        if resp.status_code != 200:
            print(f"  ERROR: {url} returned {resp.status_code}", file=sys.stderr)
            break
        data = resp.json()
        if not data:
            break
        items.extend(data)
        # Check if there are more pages
        total_pages = resp.headers.get('X-WP-TotalPages')
        if total_pages and int(total_pages) <= page:
            break
        page += 1
        if page > 20:  # safety limit
            break
    return items

def check_elementor(content):
    """Check if Elementor is used in the page."""
    return 'elementor' in content.lower() or 'data-elementor-type' in content

def check_page_for_meta(html_content):
    """Extract meta description from rendered content."""
    # Yoast/RankMath sometimes embed it
    m = re.search(r'class=".*?yoast.*?".*?content="([^"]+)"', html_content)
    if m:
        return m.group(1)
    return None

def main():
    print("=" * 80)
    print("TECHNICAL SEO & CONTENT AUDIT REPORT - kanokmiah.com")
    print("=" * 80)
    
    # 1. Check homepage redirects
    print("\n--- 1. HOMEPAGE REDIRECT CHECK ---")
    for proto in ['https://', 'http://']:
        for domain in ['kanokmiah.com', 'www.kanokmiah.com']:
            url = f"{proto}{domain}"
            try:
                resp = requests.get(url, auth=AUTH, allow_redirects=True, timeout=15)
                print(f"  {url}")
                print(f"    Status: {resp.status_code}")
                print(f"    Final URL: {resp.url}")
                print(f"    Redirect chain: ", end="")
                if resp.history:
                    for i, r in enumerate(resp.history):
                        print(f"{r.status_code} -> {r.url} ", end="")
                    print(f"-> {resp.url}")
                else:
                    print("None (direct)")
            except Exception as e:
                print(f"  {url} - ERROR: {e}")
    
    # 2. Fetch all pages
    print("\n--- 2. FETCHING ALL PAGES ---")
    pages = fetch_all('pages')
    print(f"  Found {len(pages)} pages")
    
    # 3. Fetch all posts
    print("\n--- 3. FETCHING ALL POSTS ---")
    posts = fetch_all('posts')
    print(f"  Found {len(posts)} posts")
    
    # 4. Analyze each page
    print("\n--- 4. PAGE-BY-PAGE AUDIT ---")
    
    all_items = []
    
    print("\n  --- PAGES ---")
    for p in pages:
        title = p['title']['rendered']
        slug = p['slug']
        link = p['link']
        content_html = p['content']['rendered']
        excerpt_html = p['excerpt']['rendered']
        
        h1s = extract_h1(content_html)
        has_h1 = len(h1s) > 0
        h1_text = h1s[0] if has_h1 else "MISSING"
        
        content_text = strip_html(content_html)
        excerpt_text = strip_html(excerpt_html)
        full_text = content_text + " " + excerpt_text
        wc = word_count(full_text)
        
        uses_elementor = check_elementor(content_html)
        
        meta_desc = None
        # Try to find meta description in the excerpt
        if excerpt_text and len(excerpt_text) > 20:
            meta_desc = excerpt_text[:200]
        
        all_items.append({
            'type': 'page',
            'title': title,
            'slug': slug,
            'link': link,
            'h1_count': len(h1s),
            'h1_text': h1_text,
            'has_h1': has_h1,
            'word_count': wc,
            'meta_desc_preview': (meta_desc[:150] + '...') if meta_desc and len(meta_desc) > 150 else (meta_desc or ''),
            'uses_elementor': uses_elementor,
        })
        
        h1_status = "✅" if has_h1 else "❌ MISSING H1"
        ele_status = "Elementor" if uses_elementor else "Classic"
        print(f"  [{ele_status}] {title}")
        print(f"    URL: {link}")
        print(f"    H1 ({len(h1s)}): {h1_text}")
        print(f"    Words: {wc}")
        print(f"    {h1_status}")
        if meta_desc:
            print(f"    Meta desc: {meta_desc[:120]}...")
        print()
    
    print("\n  --- POSTS ---")
    for p in posts:
        title = p['title']['rendered']
        slug = p['slug']
        link = p['link']
        content_html = p['content']['rendered']
        excerpt_html = p['excerpt']['rendered']
        
        h1s = extract_h1(content_html)
        has_h1 = len(h1s) > 0
        h1_text = h1s[0] if has_h1 else "MISSING"
        
        content_text = strip_html(content_html)
        excerpt_text = strip_html(excerpt_html)
        full_text = content_text + " " + excerpt_text
        wc = word_count(full_text)
        
        uses_elementor = check_elementor(content_html)
        
        meta_desc = None
        if excerpt_text and len(excerpt_text) > 20:
            meta_desc = excerpt_text[:200]
        
        all_items.append({
            'type': 'post',
            'title': title,
            'slug': slug,
            'link': link,
            'h1_count': len(h1s),
            'h1_text': h1_text,
            'has_h1': has_h1,
            'word_count': wc,
            'meta_desc_preview': (meta_desc[:150] + '...') if meta_desc and len(meta_desc) > 150 else (meta_desc or ''),
            'uses_elementor': uses_elementor,
        })
        
        h1_status = "✅" if has_h1 else "❌ MISSING H1"
        ele_status = "Elementor" if uses_elementor else "Classic"
        print(f"  [{ele_status}] {title}")
        print(f"    URL: {link}")
        print(f"    H1 ({len(h1s)}): {h1_text}")
        print(f"    Words: {wc}")
        print(f"    {h1_status}")
        if meta_desc:
            print(f"    Meta desc: {meta_desc[:120]}...")
        print()
    
    # 5. Summary: Missing H1s
    print("\n--- 5. PAGES MISSING H1 TAG ---")
    missing_h1 = [i for i in all_items if not i['has_h1']]
    if missing_h1:
        for item in missing_h1:
            print(f"  ❌ [{item['type'].upper()}] \"{item['title']}\"")
            print(f"     {item['link']}")
    else:
        print("  ✅ All pages/posts have H1 tags.")
    
    # 6. Summary: Elementor usage
    print("\n--- 6. ELEMENTOR USAGE ---")
    ele_items = [i for i in all_items if i['uses_elementor']]
    non_ele_items = [i for i in all_items if not i['uses_elementor']]
    print(f"  Elementor pages: {len(ele_items)}")
    print(f"  Classic pages:   {len(non_ele_items)}")
    if non_ele_items:
        print("  Non-Elementor items:")
        for item in non_ele_items:
            print(f"    - {item['title']} ({item['link']})")
    
    # 7. Content gaps for ranking keywords
    print("\n--- 7. CONTENT GAP ANALYSIS ---")
    target_keywords = [
        "best digital marketing expert in Bangladesh",
        "digital marketing expert Bangladesh",
        "SEO expert Bangladesh",
        "best SEO company in Bangladesh",
        "digital marketing agency Bangladesh",
        "top digital marketer in Bangladesh",
        "affordable SEO services Bangladesh",
        "Facebook ads expert Bangladesh",
        "Google Ads expert Bangladesh",
        "content marketing Bangladesh",
        "social media marketing Bangladesh",
    ]
    
    # Collect all text content
    all_text = ""
    for item in all_items:
        all_text += item['title'] + " " + item['h1_text'] + " "
    all_text_lower = all_text.lower()
    
    print("  Keyword presence in page titles and H1s:\n")
    for kw in target_keywords:
        kw_lower = kw.lower()
        # Check exact phrase in all text
        found = kw_lower in all_text_lower
        # Find which items mention it
        mentioning_items = []
        for item in all_items:
            combined = (item['title'] + " " + item['h1_text']).lower()
            if kw_lower in combined:
                mentioning_items.append(item['title'])
        
        status = "✅ FOUND" if found else "❌ NOT FOUND"
        print(f"  {status}: \"{kw}\"")
        if mentioning_items:
            for t in mentioning_items:
                print(f"         - {t}")
        else:
            # Check if any partial mention exists
            partial = False
            for word in kw_lower.split():
                if word in all_text_lower and len(word) > 3:
                    partial = True
            if not partial:
                print(f"         ⚠️ No partial mention either - content gap!")
        print()
    
    # 8. Summary stats
    print("\n--- 8. OVERALL STATISTICS ---")
    print(f"  Total pages: {len(pages)}")
    print(f"  Total posts: {len(posts)}")
    print(f"  Total items: {len(all_items)}")
    print(f"  Items with H1: {sum(1 for i in all_items if i['has_h1'])}")
    print(f"  Items missing H1: {sum(1 for i in all_items if not i['has_h1'])}")
    print(f"  Elementor pages: {len(ele_items)}")
    print(f"  Average word count: {sum(i['word_count'] for i in all_items) // len(all_items) if all_items else 0}")
    
    # 9. Recommendations
    print("\n--- 9. SEO & CONTENT RECOMMENDATIONS ---")
    print("""
  PRIORITY RECOMMENDATIONS:

  1. Missing H1 Tags:
  """)
    if missing_h1:
        for item in missing_h1:
            print(f"     - Add H1 tag to \"{item['title']}\" at {item['link']}")
    else:
        print("     None - all pages have H1 tags. ✅")
    
    print("""
  2. Content for Target Keywords:
  
     The following pages/posts should be created or optimized to target
     high-value keywords:
  """)
    
    # Based on what we found, suggest content
    print("""
     a) Create dedicated page: "Best Digital Marketing Expert in Bangladesh"
        - Optimize for "best digital marketing expert in Bangladesh"
        - Include schema markup (Person, LocalBusiness)
        - Target 1500-2500 words with case study references
        
     b) Create dedicated service page: "SEO Services Bangladesh"
        - Target "SEO expert Bangladesh", "best SEO company in Bangladesh"
        - List specific SEO packages with pricing
        - Include client testimonials
        
     c) Create dedicated page: "Facebook Ads Agency Bangladesh"
        - Target "Facebook ads expert Bangladesh"
        - Reference Fixzoo, Dohar Malabis, Iqra Cadet Madrasha case studies
        
     d) Create dedicated page: "Google Ads Management Bangladesh"
        - Target "Google Ads expert Bangladesh"
        - Reference SMMJobz, SMMRX, CloudMatrix case studies
        
     e) Add comparison content:
        - "Best Digital Marketing Agencies in Bangladesh" (listicle/comparison)
        - "Affordable SEO Packages in Bangladesh" (pricing page)
        
     f) Add FAQ schema content across all service pages targeting
        question-based queries about digital marketing in Bangladesh.
    
  3. Technical Improvements:
     - Ensure all pages have unique meta descriptions
     - Add internal links between case studies and service pages
     - Consider adding a blog category for "Bangladesh Digital Marketing"
     - Add Location-specific pages for Dhaka, Chittagong etc.
  """)
    
    print("=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
