#!/usr/bin/env python3
"""
Internal Linking Audit & Fix Script for KanokMiah Blog
Fixed version - handles double-quoted slugs and backtick content
"""

import re
import sys
from collections import defaultdict
from datetime import datetime

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

def load_data():
    with open(DATA_FILE, 'r') as f:
        return f.read()

def save_data(content):
    with open(DATA_FILE, 'w') as f:
        f.write(content)

def parse_posts(content):
    """Parse all blog posts from data.js"""
    posts = []
    # Pattern: slug: "slug-value"\n    title: "...\n    content: `...`,\n    },
    # Find each content block by locating "content: `" and matching backtick pairs
    pattern = re.compile(r'slug:\s*"([^"]+)"[\s\S]*?content:\s*`([\s\S]*?)`,\s*\n\s*\},?\n')
    for m in pattern.finditer(content):
        posts.append({
            'slug': m.group(1),
            'body': m.group(2),
            'start': m.start(2),
            'end': m.end(2),
        })
    return posts

def extract_links(text):
    """Extract markdown internal links from text"""
    links = []
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
        url = m.group(2)
        anchor = m.group(1)
        # Only internal links
        if url.startswith('/') or 'kanokmiah.com.bd' in url or 'kanokmiah-site' in url:
            if 'kanokmiah.com.bd' in url:
                url = '/' + url.split('kanokmiah.com.bd', 1)[-1].lstrip('/')
            elif 'kanokmiah-site' in url:
                url = '/' + url.split('.vercel.app', 1)[-1].lstrip('/') if '.vercel.app' in url else url
            links.append({
                'url': url,
                'anchor': anchor,
                'full': m.group(0),
                'start': m.start(),
                'end': m.end(),
            })
    return links

def remove_duplicate_links(body):
    """Remove duplicate links - keep only first occurrence of each URL"""
    seen_urls = set()
    changes = 0
    
    links_found = list(re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', body))
    
    # Process in reverse to maintain offsets
    for m in reversed(links_found):
        url = m.group(2)
        # Normalize URL
        if url.startswith('/') or 'kanokmiah' in url:
            if 'kanokmiah.com.bd' in url:
                url_norm = '/' + url.split('kanokmiah.com.bd', 1)[-1].lstrip('/')
            elif 'kanokmiah-site' in url:
                url_norm = '/' + url.split('.vercel.app', 1)[-1].lstrip('/') if '.vercel.app' in url else url
            else:
                url_norm = url
            
            if url_norm in seen_urls:
                # Remove link markup, keep anchor text
                anchor = m.group(1)
                body = body[:m.start()] + anchor + body[m.end():]
                changes += 1
            else:
                seen_urls.add(url_norm)
    
    return body, changes

def add_missing_home_link(body, slug):
    """Add contextual homepage link if missing"""
    # Check if / link already exists
    if re.search(r'\(/\)|\(/[\'"]?\)', body):
        return body, False
    
    # Find good insertion point - after first paragraph or at end
    # Check content type
    is_english = any(kw in body.lower()[:500] for kw in ['the', 'is', 'are', 'for', 'and'])
    is_bengali = not is_english
    
    # Skip very short content
    if len(body) < 200:
        return body, False
    
    if is_bengali:
        anchors = [
            "[কানক মিয়া](/)-কে",
            "[কানক মিয়া](/),",
            "[সেরা SEO বিশেষজ্ঞ](/)-এর",
        ]
    else:
        anchors = [
            "[Kanok Miah](/).",
            "[best SEO expert in Bangladesh](/).",
            "[SEO expert in Dhaka](/).",
            "[professional SEO services](/).",
            "[SEO consultant](/),",
        ]
    
    anchor = anchors[hash(slug) % len(anchors)]
    
    # Add at end of content before last newline
    body = body.rstrip() + f"\n\nLooking for the {anchor}"
    return body, True

def add_location_link(body):
    """Add /locations/dhaka link if Dhaka/Bangladesh content and no location link"""
    if '/locations/' in body:
        return body, False
    
    has_loc = any(kw in body.lower()[:1000] for kw in ['dhaka', 'bangladesh', 'mirpur', 'gulshan', 'banani'])
    if not has_loc:
        return body, False
    
    body = body.rstrip() + f"\n\n**[SEO services in Dhaka neighborhoods](/locations/dhaka)**."
    return body, True

def main():
    content = load_data()
    posts = parse_posts(content)
    
    print(f"📊 Found {len(posts)} blog posts\n")
    
    total_duplicates = 0
    total_home_added = 0
    total_location_added = 0
    updated_slugs = []
    stats = {'home_before': 0, 'home_after': 0, 'loc_before': 0, 'loc_after': 0}
    
    for i, post in enumerate(posts):
        slug = post['slug']
        print(f"  [{i+1}/{len(posts)}] {slug[:50]:50s} ", end='', flush=True)
        
        body = post['body']
        links_before = extract_links(body)
        has_home_before = any(l['url'] in ['/', ''] for l in links_before)
        has_loc_before = any('/locations/' in l['url'] for l in links_before)
        
        if has_home_before:
            stats['home_before'] += 1
        if has_loc_before:
            stats['loc_before'] += 1
        
        # Fix: Remove duplicate links
        new_body, dup_count = remove_duplicate_links(body)
        
        # Fix: Add homepage link
        new_body, home_added = add_missing_home_link(new_body, slug)
        
        # Fix: Add location link
        new_body, loc_added = add_location_link(new_body)
        
        if dup_count > 0 or home_added or loc_added:
            # Update the post
            old_key = f"content: `{body}`"
            new_key = f"content: `{new_body}`"
            
            if old_key in content:
                content = content.replace(old_key, new_key, 1)
                total_duplicates += dup_count
                total_home_added += 1 if home_added else 0
                total_location_added += 1 if loc_added else 0
                updated_slugs.append(slug)
                print(f"✅ dup:{dup_count} home:{int(home_added)} loc:{int(loc_added)}")
            else:
                print(f"❌ REPLACE FAILED (body not found)")
        else:
            print(f"✅ clean ({len(links_before)} links)")
    
    # Save if changes made
    if updated_slugs:
        save_data(content)
    
    # Report
    print(f"\n{'='*60}")
    print(f"📋 INTERNAL LINKING AUDIT REPORT")
    print(f"{'='*60}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📊 Total blogs audited: {len(posts)}")
    print(f"🔗 Duplicate links removed: {total_duplicates}")
    print(f"🏠 Homepage links added: {total_home_added}")
    print(f"📍 Location links added: {total_location_added}")
    print(f"📝 Blogs updated: {len(updated_slugs)}")
    print(f"✅ Homepage links BEFORE: {stats['home_before']} | AFTER: {stats['home_before'] + total_home_added}")
    print(f"✅ Location links BEFORE: {stats['loc_before']} | AFTER: {stats['loc_before'] + total_location_added}")
    print(f"{'='*60}")
    
    return len(updated_slugs)

if __name__ == '__main__':
    main()
