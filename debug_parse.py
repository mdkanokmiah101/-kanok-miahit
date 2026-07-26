#!/usr/bin/env python3
"""Debug parsing issues with seo-structured-data-guide-bd"""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Find this specific post
slug = "seo-structured-data-guide-bd"
pattern = re.compile(r'^\s{4}slug:\s*"([^"]+)"', re.MULTILINE)
match = None
for m in pattern.finditer(text):
    if m.group(1) == slug:
        match = m
        break

if match:
    start_pos = match.start()
    brace_start = text.rfind('{', 0, start_pos)
    
    # Find next slug after this one
    next_match = None
    for m in pattern.finditer(text):
        if m.start() > start_pos:
            next_match = m
            break
    
    if next_match:
        next_start = next_match.start()
        end_search_start = brace_start
        end_search_end = next_start
        
        # Find '  },' 
        end_pos = text.find('\n  },', brace_start, next_start)
        if end_pos == -1:
            end_pos = text.find('\n  }', brace_start, next_start)
        if end_pos != -1:
            end_pos += 5
        else:
            end_pos = text.rfind('}', brace_start, next_start)
            if end_pos != -1:
                end_pos += 1
    else:
        end_pos = text.find('\n];', start_pos)
        if end_pos != -1:
            end_pos += 3
    
    post_text = text[brace_start:end_pos]
    print(f"Post text length: {len(post_text)}")
    print(f"Post text starts at line {text[:brace_start].count(chr(10))+1}")
    print(f"First 200 chars: {post_text[:200]}")
    print(f"Last 200 chars: {post_text[-200:]}")
    
    # Find content
    cs = post_text.find('content: `')
    print(f"\ncontent: position: {cs}")
    
    if cs != -1:
        cs += len('content: `')
        print(f"After 'content: `', position: {cs}")
        print(f"Content starts with: {post_text[cs:cs+100]}")
        
        # Find closing backtick
        # Look for `,\n
        ce1 = post_text.rfind('`,\n')
        print(f"rfind('`,\\n'): {ce1}")
        
        # Look for `,
        ce2 = post_text.rfind('`,')
        print(f"rfind('`,'): {ce2}")
        
        # Look for just backtick
        ce3 = post_text.rfind('`')
        print(f"rfind('`'): {ce3}")
        
        # How many backticks in the content?
        content_section = post_text[cs:]
        backtick_count = content_section.count('`')
        print(f"\nBacktick count in content section: {backtick_count}")
        
        # Check for escaped backticks \`
        escaped_count = content_section.count('\\`')
        print(f"Escaped backtick (\\`) count: {escaped_count}")
        
        # Check for triple backticks \`\`\`
        triple_count = content_section.count('\\`\\`\\`')
        print(f"Triple backtick (\\`\\`\\`) count: {triple_count}")
        
        # The actual number of real closing backtick candidates
        # Real backtick count = total - escaped
        real_backticks = backtick_count - escaped_count
        print(f"Real (unescaped) backtick count: {real_backticks}")
        
        # Show positions of all backtick-comma occurrences
        print("\nAll `, occurrences:")
        for i, c in enumerate(content_section):
            if c == '`' and i+1 < len(content_section) and content_section[i+1] == ',':
                context = content_section[max(0,i-20):i+20]
                print(f"  Position {i}: ...{repr(context)}...")
        
        # Let's try a different approach: iterate through chars
        # to find the real closing backtick
        depth = 0
        i = 0
        while i < len(content_section):
            if content_section[i] == '\\' and i+1 < len(content_section) and content_section[i+1] == '`':
                i += 2
                continue
            if content_section[i] == '`':
                # This is the closing backtick
                if i+1 >= len(content_section) or content_section[i+1] == ',' or content_section[i+1] == '\n':
                    print(f"\nFound closing backtick at content offset {i}")
                    print(f"Context: ...{repr(content_section[max(0,i-10):i+30])}...")
                    if ce1 != -1:
                        actual_end = ce1 - cs  # relative to content_section start
                        print(f"rfind `,\\n gave offset {actual_end}")
                    break
            i += 1
        
        # Check the content section before the first backtick-comma
        first_comma_pos = content_section.find('`,\n')
        print(f"\nFirst `,\\n at content offset: {first_comma_pos}")
        if first_comma_pos > 0:
            print(f"Context: ...{repr(content_section[first_comma_pos-30:first_comma_pos+30])}...")
        
        # And check what's at the very end
        print(f"\nLast 50 chars of content section: {repr(content_section[-50:])}")
        print(f"Last 50 chars of post_text: {repr(post_text[-50:])}")
