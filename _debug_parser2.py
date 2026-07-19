#!/usr/bin/env python3
"""Debug the data.js parser - trace content field parsing."""

with open('src/app/blog/data.js', 'r') as f:
    text = f.read()

def skip_ws(t, i):
    while i < len(t) and (t[i] in ' \t\n\r,' or (t[i] == '/' and i+1 < len(t) and t[i+1] == '/')):
        if t[i] == '/' and i+1 < len(t) and t[i+1] == '/':
            nl = t.find('\n', i)
            i = nl + 1 if nl != -1 else len(t)
        else:
            i += 1
    return i

def parse_backtick(t, start):
    i = start + 1
    result = []
    while i < len(t):
        ch = t[i]
        if ch == '\\':
            if i + 1 < len(t):
                result.append(t[i+1])
                i += 2
            else:
                i += 1
        elif ch == '$' and i + 1 < len(t) and t[i+1] == '{':
            expr_depth = 1
            i += 2
            while i < len(t) and expr_depth > 0:
                if t[i] == '{':
                    expr_depth += 1
                elif t[i] == '}':
                    expr_depth -= 1
                i += 1
        elif ord(ch) == 96:  # backtick
            i += 1
            break
        else:
            result.append(ch)
            i += 1
    return ''.join(result), i

def parse_sq_string(t, start):
    i = start + 1
    result = []
    while i < len(t):
        ch = t[i]
        if ch == '\\':
            if i + 1 < len(t):
                result.append(t[i+1])
                i += 2
            else:
                i += 1
        elif ch == "'":
            i += 1
            break
        else:
            result.append(ch)
            i += 1
    return ''.join(result), i

def parse_dq_string(t, start):
    i = start + 1
    result = []
    while i < len(t):
        ch = t[i]
        if ch == '\\':
            if i + 1 < len(t):
                result.append(t[i+1])
                i += 2
            else:
                i += 1
        elif ch == '"':
            i += 1
            break
        else:
            result.append(ch)
            i += 1
    return ''.join(result), i

def parse_array(t, start):
    items = []
    i = start
    if t[i] != '[':
        return items, start + 1
    i += 1
    while i < len(t):
        i = skip_ws(t, i)
        if i >= len(t):
            break
        if t[i] == ']':
            i += 1
            break
        if t[i] == "'":
            val, i = parse_sq_string(t, i)
            items.append(val)
        elif t[i] == '"':
            val, i = parse_dq_string(t, i)
            items.append(val)
        elif ord(t[i]) == 96:
            val, i = parse_backtick(t, i)
            items.append(val)
        elif t[i].isalpha() or t[i] in '-0123456789':
            ident_end = i
            while ident_end < len(t) and (t[ident_end].isalnum() or t[ident_end] in '_-.'):
                ident_end += 1
            items.append(t[i:ident_end])
            i = ident_end
        else:
            i += 1
    return items, i

def parse_object(t, start):
    obj = {}
    i = start
    if t[i] != '{':
        return None, start + 1
    i += 1
    depth = 1
    key = None
    while i < len(t) and depth > 0:
        prev = i
        i = skip_ws(t, i)
        if i >= len(t):
            break
        
        ch = t[i]
        
        if ch == '}':
            depth -= 1
            if depth == 0:
                i += 1
                break
            i += 1
            continue
        
        if ch == '{':
            _, i = parse_object(t, i)
            continue
        
        if ch == '[':
            _, i = parse_array(t, i)
            continue
        
        if ord(ch) == 96:  # backtick
            val, i = parse_backtick(t, i)
            if key is not None:
                obj[key] = val
                if key == 'content':
                    print('  CONTENT BACKTICK: len=' + str(len(val)))
                key = None
            continue
        
        if ch == "'":
            val, i = parse_sq_string(t, i)
            if key is not None:
                obj[key] = val
                key = None
            else:
                key = val
            continue
        
        if ch == '"':
            val, i = parse_dq_string(t, i)
            if key is not None:
                obj[key] = val
                key = None
            else:
                key = val
            continue
        
        if ch == ':':
            i += 1
            continue
        
        if ch.isalpha() or ch == '_':
            ident_end = i
            while ident_end < len(t) and (t[ident_end].isalnum() or t[ident_end] in '_-'):
                ident_end += 1
            ident = t[i:ident_end]
            i = ident_end
            i = skip_ws(t, i)
            if i < len(t) and t[i] == ':':
                if ident == 'content':
                    print('  KEY content found at pos ' + str(prev) + ', i=' + str(i))
                key = ident
                i += 1
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
    
    return obj, i

# Parse the first post
start = text.find('{')
print('First post starts at pos:', start)
print('Context around start:', repr(text[start:start+300]))
print('---')

obj, end = parse_object(text, start)
print('\nParsed keys:', list(obj.keys())[:15])
print('Has content:', 'content' in obj)
if 'content' in obj:
    c = obj['content']
    print('Content len:', len(c))
    if len(c) > 0:
        print('Content starts with:', repr(c[:100]))
else:
    # Check what keys we have
    for k in ['slug', 'title', 'excerpt', 'date', 'author', 'tags', 'content', 'metaTitle', 'metaDescription']:
        v = obj.get(k, 'MISSING')
        if isinstance(v, str):
            print('  ' + k + ': ' + repr(v[:60]))
        else:
            print('  ' + k + ': ' + str(type(v)) + ' = ' + repr(v)[:60])
