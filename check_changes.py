import re, subprocess, sys

# Get old version
result = subprocess.run(['git', 'show', '9a56389:src/app/blog/data.js'], capture_output=True, text=True)
old_content = result.stdout

# Get current version
with open('src/app/blog/data.js', 'r') as f:
    curr_content = f.read()

def get_posts_simple(content):
    posts = {}
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.search(r'slug: "([^"]+)"', line)
        if m:
            slug = m.group(1)
            post_lines = [line]
            i += 1
            while i < len(lines):
                if re.search(r'slug: "([^"]+)"', lines[i]):
                    break
                if lines[i].strip() == '];':
                    break
                post_lines.append(lines[i])
                i += 1
            posts[slug] = '\n'.join(post_lines)
        else:
            i += 1
    return posts

old_posts = get_posts_simple(old_content)
curr_posts = get_posts_simple(curr_content)

print(f"Old posts: {len(old_posts)}")
print(f"Curr posts: {len(curr_posts)}")

common = set(old_posts.keys()) & set(curr_posts.keys())
modified = []
for slug in sorted(common):
    if old_posts[slug] != curr_posts[slug]:
        modified.append(slug)

print(f"Modified existing posts within 48h: {len(modified)}")
for m in modified:
    print(f"  MODIFIED: {m}")

new_slugs = set(curr_posts.keys()) - set(old_posts.keys())
print(f"\nNew posts within 48h: {len(new_slugs)}")
for n in sorted(new_slugs):
    print(f"  NEW: {n}")
