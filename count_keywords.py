import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

content_lines = lines[636:799]
content = ''.join(content_lines)

print("=== CHECK A: TF-IDF Coverage ===")
keyword_count = len(re.findall(r'SEO\s+[Aa]gency', content))
print(f"Occurrences of 'SEO Agency'/'SEO agency': {keyword_count}")

print("\n=== CHECK D: AEO/GEO: Question-based Headings ===")
headings = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are']
question_headings = []
for h in headings:
    for qw in question_words:
        if h.startswith(qw + ' '):
            question_headings.append(h)
            break
print(f"Question-based headings ({len(question_headings)}):")
for h in question_headings:
    print(f"  - {h}")

print("\n=== CHECK E: Internal Links ===")
blog_links = re.findall(r'\(/blog/[^)]+\)', content)
services_links = re.findall(r'\(/services[^)]*\)', content)
locations_links = re.findall(r'\(/locations/[^)]+\)', content)
industries_links = re.findall(r'\(/industries/[^)]+\)', content)
about_links = re.findall(r'\(/about[^)]*\)', content)
home_links = re.findall(r'\(/\)', content)
print(f"Blog links: {len(blog_links)}")
print(f"Services links: {len(services_links)}")
print(f"Location links: {len(locations_links)}")
print(f"Industries links: {len(industries_links)}")
print(f"About links: {len(about_links)}")
print(f"Home links: {len(home_links)}")
total = len(blog_links)+len(services_links)+len(locations_links)+len(industries_links)+len(about_links)+len(home_links)
print(f"Total internal links: {total}")

print("\n=== CHECK F: Schema Fields ===")
post_lines = lines[627:636]
post_text = ''.join(post_lines)
print(f"Slug set: {'YES' if 'how-to-choose-right-seo-agency-bangladesh' in post_text else 'NO'}")
print(f"Title set: {'YES' if 'How to Choose the Right SEO Agency in Bangladesh' in post_text else 'NO'}")
print(f"Date set: {'YES' if '2026-05-20' in post_text else 'NO'}")
print(f"Excerpt set: {'YES' if 'excerpt' in post_text else 'NO'}")

print("\n=== CHECK B: Semantic Entity Coverage ===")
dhaka = len(re.findall(r'Dhaka', content))
bangladesh = len(re.findall(r'Bangladesh', content))
service_type = len(re.findall(r'SEO\s+service|digital\s+marketing|SEO\s+consult', content, re.IGNORECASE))
industry = len(re.findall(r'digital\s+marketing|agency\s+selection|ecommerce|real\s+estate', content, re.IGNORECASE))
print(f"Dhaka mentions: {dhaka}")
print(f"Bangladesh mentions: {bangladesh}")
print(f"Service type mentions: {service_type}")
print(f"Industry mentions: {industry}")

print("\n=== CHECK C: Pillar-Cluster Alignment ===")
print(f"Links to /services/ (pillar): {len(services_links)}")
for l in services_links:
    print(f"  {l}")
