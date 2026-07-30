#!/usr/bin/env python3
"""
Parse data.js post objects using a state machine.
Robust for multi-line strings and template literals.
Outputs JSON array of post objects to stdout.
"""
import re
import json
import sys

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"


def parse_posts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    posts = []

    # Find all slug positions
    slug_positions = [m.start() for m in re.finditer(r'^\s+slug:\s+"([^"]+)"', content, re.MULTILINE)]

    for i, pos in enumerate(slug_positions):
        # Find the start of this post object (the "  {" before slug)
        obj_start = content.rfind('{', 0, pos)
        line_start = content.rfind('\n', 0, obj_start) + 1

        # Find the end of this post object
        if i + 1 < len(slug_positions):
            next_slug_pos = slug_positions[i + 1]
            obj_end = content.rfind('},', 0, next_slug_pos)
            if obj_end == -1 or obj_end < pos:
                obj_end = next_slug_pos
            obj_end = content.find('\n', obj_end) + 1
        else:
            obj_end = content.rfind('];')

        raw = content[line_start:obj_end].strip()

        post = {}

        # slug
        m = re.search(r'slug:\s+"([^"]+)"', raw)
        if m:
            post['slug'] = m.group(1)

        # title
        m = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', raw)
        if m:
            post['title'] = m.group(1)

        # date
        m = re.search(r'date:\s+"([^"]*)"', raw)
        if m:
            post['date'] = m.group(1)

        # author
        m = re.search(r'author:\s+"([^"]*)"', raw)
        if m:
            post['author'] = m.group(1)

        # excerpt (can be multi-line)
        m = re.search(r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', raw)
        if m:
            post['excerpt'] = m.group(1)
        else:
            post['excerpt'] = ''

        # tags
        m = re.search(r'tags:\s*\[([^\]]*)\]', raw)
        if m:
            tags_str = m.group(1)
            post['tags'] = [t.strip().strip('"') for t in tags_str.split(',') if t.strip()]
        else:
            post['tags'] = []

        # dateModified (optional)
        m = re.search(r'dateModified:\s+"([^"]*)"', raw)
        post['dateModified'] = m.group(1) if m else ''

        # content - find the template literal
        m = re.search(r'content:\s*`\n', raw)
        if m:
            content_start = m.end()
            rest = raw[content_start:]
            end_idx = rest.find('`')
            post['content'] = rest[:end_idx] if end_idx >= 0 else ''
        else:
            post['content'] = ''

        posts.append(post)

    return posts


def main():
    posts = parse_posts(DATA_FILE)
    json.dump(posts, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
