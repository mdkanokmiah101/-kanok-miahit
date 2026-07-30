#!/usr/bin/env python3
"""Verify specific post content extractions."""
import re

with open('src/app/blog/data.js', 'r') as f:
    raw = f.read()

# Manual verification for specific posts
pairs = [
    ('locksmith-dundee-seo-case-study', 'Case Study'),
    ('hiring-seo-expert-dhaka-better-roi-than-paid-ads', 'SEO expert'),
    ('how-to-choose-best-seo-expert-dhaka-15-things', 'SEO expert'),
    ('watchzonebd-seo-case-study', 'Case Study'),
    ('stealth-windshield-repairs-seo-case-study', 'case study'),
    ('mir-cement-seo-case-study', 'case study'),
    ('smmsun-seo-case-study', 'case study'),
]

for slug, keyword in pairs:
    idx = raw.find(f'slug: "{slug}"')
    if idx == -1:
        idx = raw.find(f"slug: '{slug}'")
    if idx == -1:
        print(f"{slug}: NOT FOUND")
        continue
    
    # Find content field - look for backtick after "content:"
    ci = raw.find('content: `', idx)
    if ci == -1:
        ci = raw.find("content: '", idx)
    if ci == -1:
        ci = raw.find('content:\n    `', idx)
    if ci == -1:
        print(f"{slug}: NO content found")
        continue
    
    # Find opening backtick
    bt = raw.find('`', ci)
    if bt == -1:
        print(f"{slug}: NO backtick")
        continue
    
    # Extract content by finding the post boundaries first
    # Find the next slug to know where this post ends
    next_slug_idx = raw.find('slug:', bt)
    if next_slug_idx > 0:
        # Find the closing }, before next slug
        post_end_marker = raw.rfind('},', bt, next_slug_idx)
        if post_end_marker <= 0:
            post_end_marker = raw.rfind('};', bt, next_slug_idx)
    else:
        post_end_marker = raw.rfind('};', bt)
    
    # Find the closing backtick+comma before the post end
    if post_end_marker > 0:
        # Search backwards for the pattern that closes the content
        content_section = raw[bt:post_end_marker]
        # Find the last occurrence of a backtick followed by newline and }
        lines = content_section.split('\n')
        # The content is everything between first backtick and the last line that starts with backtick followed by comma
        content_parts = []
        in_content = False
        for line in lines:
            stripped = line.strip()
            if not in_content:
                if stripped == '':
                    continue
                # First real line after backtick
                if '`' in line and not in_content:
                    # Check if this is the opening line with just backtick
                    if stripped == '`':
                        in_content = True
                    elif stripped.endswith('`,'):
                        # One-liner content
                        content_line = stripped[1:-2]  # remove backtick and `,
                        content_parts.append(content_line)
                        break
                    else:
                        # Remove the leading backtick
                        bt_idx = line.find('`')
                        if bt_idx >= 0:
                            remainder = line[bt_idx+1:]
                            if remainder:
                                content_parts.append(remainder)
                        in_content = True
            else:
                if stripped.endswith('`,'):
                    # End of content
                    content_line = stripped[:-2]  # remove `,
                    if content_line:
                        content_parts.append(line[:line.rfind('`')].rstrip())
                    break
                elif stripped == '`':
                    # Backtick alone on a line
                    content_parts.append(line)
                elif stripped.count('`') >= 3:
                    # Code block
                    content_parts.append(line)
                else:
                    content_parts.append(line)
        
        content = '\n'.join(content_parts)
    else:
        content = raw[bt+1:bt+200]
    
    # Count keyword
    kw_count = content.lower().count(keyword.lower())
    
    # Question headings
    q_headings = re.findall(r'^#{2,4}\s+.+\?$', content, re.MULTILINE)
    
    # Internal links  
    internal_links = re.findall(r'\[([^\]]+)\]\((/[a-z][^\)]*)\)', content)
    internal_paths = [link for _, link in internal_links if not link.startswith('http') and not link.startswith('//')]
    
    print(f"\n=== {slug} ===")
    print(f"  Keyword \"{keyword}\": {kw_count} occurrences")
    print(f"  Question-based headings: {len(q_headings)} ({q_headings[:3]})")
    print(f"  Internal links: {len(internal_paths)}")
    print(f"  Content length: {len(content)} chars")
