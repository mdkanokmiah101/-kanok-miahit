import sys, re, subprocess

url = sys.argv[1]
try:
    result = subprocess.run(
        ['curl', '-sL', '--max-time', '15', '-A', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', url],
        capture_output=True, text=True, timeout=20
    )
    html = result.stdout
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

if not html:
    print("EMPTY response")
    sys.exit(1)

# Strip script and style blocks, then strip HTML tags
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()

dashes = len(re.findall(r'---', text))
stars = len(re.findall(r'\*\*', text))
brackets = len(re.findall(r'\[.*?\]\(.*?\)', text))
has_raw_heading = '## ' in text
has_single_hash_heading = False
# Check for # character at start of lines to avoid false positives from hashtags
for line in text.split('\n'):
    stripped = line.strip()
    if stripped.startswith('# ') or stripped.startswith('## ') or stripped.startswith('### '):
        has_single_hash_heading = True
        break

print(f"Raw ---: {dashes}")
print(f"Raw **: {stars}")
print(f"Raw [text](url): {brackets}")
print(f"Raw ## headings: {'YES' if has_raw_heading else 'NO'}")
print(f"Raw # headings at line start: {'YES' if has_single_hash_heading else 'NO'}")
