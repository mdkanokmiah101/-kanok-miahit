import re, sys

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Split into individual post blocks - each post starts with '{\n    slug:' and ends with backtick comma newline space space },
posts_raw = re.findall(r'\{\s*\n\s+slug: [^\n]+\n.*?(?=\n\s+\},\n\s+\{)', content, re.DOTALL)
# Add the last one
posts_raw2 = re.findall(r'\{\s*\n\s+slug: [^\n]+\n.*?`,\s*\n\s+\},', content, re.DOTALL)

if len(posts_raw2) > len(posts_raw):
    posts_raw = posts_raw2

print(f"Found {len(posts_raw)} posts total")

for i, block in enumerate(posts_raw):
    slug_m = re.search(r'slug: "([^"]+)"', block)
    title_m = re.search(r'title: "([^"]+)"', block)
    excerpt_m = re.search(r'excerpt:\s*"((?:[^"\\]|\\.)*)"', block, re.DOTALL)
    tags_m = re.search(r'tags:\s*\[(.*?)\]', block, re.DOTALL)
    date_m = re.search(r'date: "([^"]+)"', block)
    
    if not slug_m:
        continue
    
    slug = slug_m.group(1)
    title = title_m.group(1) if title_m else 'N/A'
    tags_str = tags_m.group(1).replace('\n', '') if tags_m else 'N/A'
    excerpt = excerpt_m.group(1).replace('\n', ' ').strip() if excerpt_m else 'N/A'
    
    # Get content - find the backtick block
    content_match = re.search(r'content: `(.*)`', block, re.DOTALL)
    content_text = content_match.group(1) if content_match else ''
    word_count = len(content_text.split()) if content_text else 0
    
    # Count headings
    h2_count = len(re.findall(r'^## ', content_text, re.MULTILINE))
    h3_count = len(re.findall(r'^### ', content_text, re.MULTILINE))
    
    # Internal links
    blog_links = len(re.findall(r'/blog/', content_text))
    service_links = len(re.findall(r'/services/', content_text))
    industry_links = len(re.findall(r'/industries/', content_text))
    total_internal = len(re.findall(r'/[a-z-]+/[a-z-]', content_text))
    
    # Brand mentions
    brand_kanok = len(re.findall(r'Md Kanok Miah', content_text))
    brand_expert = len(re.findall(r'best SEO expert in Dhaka', content_text))
    
    # Also check for Bengali brand variations
    brand_bn = len(re.findall(r'কনক মিঞা', content_text))
    
    # Check if first heading is H2
    first_h_match = re.search(r'^## (.+)', content_text, re.MULTILINE)
    first_h2 = first_h_match.group(1) if first_h_match else 'NONE'
    
    # Check if title has primary keywords
    has_seo = 'seo' in slug.lower() or 'এসইও' in title
    has_bangladesh = 'bangladesh' in slug.lower() or 'বাংলাদেশ' in title or 'ঢাকা' in title
    
    print(f'\n=== Post {i+1}: {slug} ===')
    print(f'Title: {title}')
    print(f'Tags: {tags_str}')
    print(f'Words: {word_count} | H2: {h2_count} | H3: {h3_count}')
    print(f'First H2: {first_h2}')
    print(f'Blog links: {blog_links} | Svc links: {service_links} | Ind links: {industry_links}')
    print(f'Brand "Md Kanok Miah": {brand_kanok} | "best SEO expert": {brand_expert} | Bengali brand: {brand_bn}')
    print(f'Excerpt (first 100): {excerpt[:100]}')
