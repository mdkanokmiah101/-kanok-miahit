import sys, re, subprocess

url = "https://kanokmiah.com.bd/blog/complete-seo-guide-bangladesh-businesses-2026"
result = subprocess.run(
    ['curl', '-sL', '--max-time', '15', '-A', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', url],
    capture_output=True, text=True, timeout=20
)
html = result.stdout

# Check --- inside table
table_match = re.findall(r'<table[^>]*>.*?</table>', html, re.DOTALL)
table_html = table_match[0] if table_match else ''
table_dashes = len(re.findall(r'---', table_html))

# Total --- in visible text
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
total_dashes = len(re.findall(r'---', text))

print(f"Dashes inside table: {table_dashes}")
print(f"Total dashes in visible text: {total_dashes}")
print(f"All dashes from table: {'YES' if total_dashes == table_dashes else 'NO - some elsewhere'}")
print(f"Table found: {'YES' if table_match else 'NO'}")
