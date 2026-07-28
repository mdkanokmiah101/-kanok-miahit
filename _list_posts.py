import subprocess, re

# Extract ALL slugs modified across both commits
all_slugs = set()

for sha in ['c822841', '0cd493b']:
    result = subprocess.run(
        ['git', 'show', sha, '--', 'src/app/blog/data.js'],
        capture_output=True, text=True, cwd='/root/kanok-miahit'
    )
    diff = result.stdout
    
    # Find slug lines (context or added lines)
    for line in diff.split('\n'):
        m = re.search(r'slug:\s*"([^"]+)"', line)
        if m:
            all_slugs.add(m.group(1))

# Read data.js to map slugs to their positions
with open('src/app/blog/data.js') as f:
    data = f.read()

# For each slug, find its position and title
for slug in sorted(all_slugs):
    # Find slug in data.js
    idx = data.find(f'slug: "{slug}"')
    if idx >= 0:
        # Get surrounding context
        before = data[max(0,idx-200):idx]
        # Find the title
        after = data[idx:idx+500]
        title_match = re.search(r'title:\s*"([^"]+)"', after[:300])
        title = title_match.group(1) if title_match else 'UNKNOWN'
        print(f'{slug}')
        print(f'  Title: {title}')
        print()

print(f'\nTotal unique modified posts: {len(all_slugs)}')
