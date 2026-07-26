import sys, re, subprocess

url = "https://kanokmiah.com.bd/blog/complete-seo-guide-bangladesh-businesses-2026"
result = subprocess.run(
    ['curl', '-sL', '--max-time', '15', '-A', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', url],
    capture_output=True, text=True, timeout=20
)
html = result.stdout

# Find the pipe table separator in HTML context
matches = re.findall(r'(<p[^>]*>[^<]*\|[-]{3,}[^<]*</p>)', html)
for m in matches:
    print('MATCH:', m[:200])
print('---')
# Also look for the full row
full_matches = re.findall(r'(<p[^>]*>[^<]*\|-{2,}\|.{0,80})', html)
for m in full_matches[:5]:
    print('FULL:', m[:200])
print('===')
# Count paragraphs containing pipe-dash
p_with_dash = len(re.findall(r'<p[^>]*>[^<]*\|-', html))
print(f"Paragraphs with pipe-dash: {p_with_dash}")
