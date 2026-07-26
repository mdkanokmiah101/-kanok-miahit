import sys, re, urllib.request

url = sys.argv[1]
try:
    with urllib.request.urlopen(url, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
except Exception as e:
    print(f"ERROR fetching: {e}")
    sys.exit(1)

# Strip script and style blocks, then strip HTML tags
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()

dashes = len(re.findall(r'---', text))
stars = len(re.findall(r'\*\*', text))
brackets = len(re.findall(r'\[.*?\]\(.*?\)', text))
has_raw_heading = '## ' in text  or '# ' in text

print(f"Raw ---: {dashes}")
print(f"Raw **: {stars}")
print(f"Raw [text](url): {brackets}")
print(f"Raw headings: {'YES' if has_raw_heading else 'NO'}")
