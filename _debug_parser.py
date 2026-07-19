#!/usr/bin/env python3
"""Debug the data.js parser - trace content field parsing."""
from _cron_framework_check import parse_object, skip_ws, parse_array, parse_backtick, parse_sq_string, parse_dq_string

with open('src/app/blog/data.js', 'r') as f:
    text = f.read()

# Find the start of the first post object
start = text.find('{')
if start > 0:
    i = start
    obj = {}
    depth = 1
    key = None
    step = 0
    content_seen = False
    
    while i < len(text) and depth > 0:
        prev_i = i
        i = skip_ws(text, i)
        
        ch = text[i]
        
        if ch == '}':
            depth -= 1
            if depth == 0:
                i += 1
                break
            i += 1
            continue
        
        if ch == '{':
            _, i = parse_object(text, i)
            continue
        
        if ch == '[':
            _, i = parse_array(text, i)
            continue
        
        if ord(ch) == 96:  # backtick
            val, i = parse_backtick(text, i)
            if key is not None:
                obj[key] = val
                if key == 'content':
                    content_seen = True
                    print(f'Set "content" = backtick(len={len(val)})')
                key = None
            else:
                print(f'WARN: backtick with no key at pos {i}')
            continue
        
        if ch == "'":
            val, i = parse_sq_string(text, i)
            if step < 20:
                print(f"  sq_string val: {repr(val[:40])}, key={key}")
            if key is not None:
                obj[key] = val
                if step < 15:
                    print(f'Set key "{key}" = {repr(val[:40])}')
                key = None
            else:
                key = val
            step += 1
            continue
        
        if ch == '"':
            val, i = parse_dq_string(text, i)
            if key is not None:
                obj[key] = val
            else:
                key = val
            continue
        
        if ch == ':':
            i += 1
            continue
        
        if ch.isalpha() or ch == '_':
            ident_end = i
            while ident_end < len(text) and (text[ident_end].isalnum() or text[ident_end] in '_-'):
                ident_end += 1
            ident = text[i:ident_end]
            i = ident_end
            i = skip_ws(text, i)
            if i < len(text) and text[i] == ':':
                key = ident
                i += 1
                if step < 15:
                    print(f'Found key: "{ident}"')
                    step += 1
            else:
                if ident in ('true', 'false'):
                    obj[key] = ident == 'true'
                elif ident == 'null':
                    obj[key] = None
                elif ident.isdigit():
                    obj[key] = int(ident)
                else:
                    obj[key] = ident
                key = None
            continue
        
        i += 1
    
    print(f'\nParsed {len(obj)} keys')
    print(f'Has content: {"content" in obj}')
    if 'content' in obj:
        print(f'Content len: {len(obj["content"])}')
        print(f'Content preview: {obj["content"][:100]}')
    else:
        print('Keys:', list(obj.keys()))
