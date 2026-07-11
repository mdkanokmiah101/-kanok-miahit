#!/usr/bin/env python3
"""
Blog Content Audit - Batch 1 (Posts 1-15)
Enhances blog posts with:
- AEO: FAQ schema JSON-LD, question-answer sections
- GEO: Entity-rich content (brand, locations, services)
- EEAT: Author expertise signals, experience-based content
- Internal links to services, industries, related blogs
- Target keywords: "best seo expert in dhaka", "Md Kanok Miah", "Bangladesh", "SEO"
"""

import re
import json

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Find all slug positions
slug_pattern = re.compile(r"^\s+slug: '([^']+)'|^\s+slug: \"([^\"]+)\"", re.MULTILINE)
slugs = [(m.start(), m.group()) for m in slug_pattern.finditer(content)]

print(f"Total posts found: {len(slugs)}")
total_size = len(content)

processed_slugs = []
BATCH_SIZE = 15

for i, (slug_pos, slug_match) in enumerate(slugs[:BATCH_SIZE]):
    slug = slug_match.split(':')[1].strip().strip("\"'")
    processed_slugs.append(slug)
    
    print(f"\n{'='*60}")
    print(f"Processing post {i+1}/{BATCH_SIZE}: {slug}")
    
    # Find the opening backtick of content: `
    # Look for "content: `" pattern (with the backtick character)
    # Pattern: the word "content:" followed by whitespace and backtick
    pat = re.compile(r'content:\s*`')
    m = pat.search(content, slug_pos)
    if not m:
        print(f"  ERROR: Could not find 'content: \\`' for {slug}")
        continue
    
    # Content starts right after the opening backtick
    content_start = m.end()
    
    # Find closing backtick - it's the NEXT backtick
    # Must be followed by a comma (end of template literal)
    bt_close = content.find('`', content_start)
    if bt_close == -1:
        print(f"  ERROR: Could not find closing backtick for {slug}")
        continue
    
    post_content = content[content_start:bt_close]
    original_content = post_content
    
    print(f"  Original length: {len(post_content)} chars, ~{len(post_content.split())} words")
    
    # --- ANALYSIS ---
    has_faq = '## Frequently Asked Questions' in post_content or '##FAQ' in post_content
    has_best_seo_expert = 'best seo expert' in post_content.lower()
    has_kanok = 'md kanok miah' in post_content.lower()
    has_geo_section = 'generative engine' in post_content.lower() or 'ai search' in post_content.lower()
    has_eeat = 'e-e-a-t' in post_content.lower() or 'eeat' in post_content.lower()
    has_qa_schema = 'application/ld+json' in post_content
    
    # Count internal links
    md_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', post_content)
    internal_md = [l for l in md_links if l[1].startswith('/')]
    service_links = [l for l in internal_md if '/services/' in l[1]]
    industry_links = [l for l in internal_md if '/industries/' in l[1]]
    blog_links = [l for l in internal_md if '/blog/' in l[1]]
    
    print(f"  FAQ section: {has_faq}")
    print(f"  'best seo expert in dhaka': {has_best_seo_expert}")
    print(f"  'Md Kanok Miah': {has_kanok}")
    print(f"  GEO/AI section: {has_geo_section}")
    print(f"  EEAT section: {has_eeat}")
    print(f"  FAQ Schema JSON-LD: {has_qa_schema}")
    print(f"  Internal links: {len(internal_md)} (svc:{len(service_links)} ind:{len(industry_links)} blog:{len(blog_links)})")
    
    modifications = []
    
    # --- 1. Fix heading formats (ensure proper markdown ## for h2, ### for h3) ---
    lines = post_content.split('\n')
    heading_fixes = 0
    for idx, line in enumerate(lines):
        stripped = line.strip()
        for h_level in ['##', '###', '####']:
            if stripped.startswith(h_level) and not stripped.startswith(h_level + ' '):
                rest = stripped[len(h_level):]
                if rest and not rest.startswith(' ') and not rest.startswith('#'):
                    lines[idx] = ' ' * (len(line) - len(line.lstrip())) + h_level + ' ' + rest
                    heading_fixes += 1
    
    if heading_fixes > 0:
        post_content = '\n'.join(lines)
        modifications.append(f"Fixed {heading_fixes} heading formats")
        print(f"  + Fixed {heading_fixes} heading formats")
    
    # --- 2. Add "best seo expert in dhaka" if missing ---
    if not has_best_seo_expert:
        lines = post_content.split('\n')
        insert_pos = 0
        for idx, line in enumerate(lines):
            if line.strip().startswith('## ') or line.strip().startswith('# '):
                for j in range(idx + 1, min(idx + 5, len(lines))):
                    if lines[j].strip() and not lines[j].strip().startswith('#'):
                        insert_pos = j + 1
                        break
                break
        
        if insert_pos > 0:
            expertise_insert = (
                "\nAs the **best SEO expert in Dhaka**, **Md Kanok Miah** has been helping "
                "businesses across Bangladesh achieve top Google rankings for over a decade. "
                "With proven expertise in local SEO, technical optimization, and content strategy, "
                "he brings practical, results-driven solutions that deliver measurable growth.\n"
            )
            lines.insert(insert_pos, expertise_insert)
            post_content = '\n'.join(lines)
            modifications.append("Added 'best seo expert in dhaka' mention")
            print("  + Added 'best seo expert in dhaka' mention")
    
    # --- 3. Add GEO section if missing ---
    if not has_geo_section:
        geo_content = (
            "\n## Generative Engine Optimization (GEO) for AI Search\n\n"
            "In 2026, AI-powered search engines like Google's Search Generative Experience (SGE), "
            "ChatGPT, Gemini, and Perplexity are changing how users find information online. "
            "Generative Engine Optimization (GEO) ensures your business appears in AI-generated answers "
            "when potential customers ask questions related to your products or services.\n\n"
            "### How to Optimize for AI Search in Bangladesh\n\n"
            "**Entity-Based Content:** Include prominent entities like \"Bangladesh,\" \"Dhaka,\" "
            "\"Chittagong,\" \"Sylhet,\" and your brand name throughout your content. "
            "AI models use entity recognition to understand topic relevance and authority.\n\n"
            "**Conversational Structure:** Write content that answers natural language questions. "
            "AI search engines favor content that directly addresses user intent in a clear, "
            "structured format.\n\n"
            "**Authoritative Citations:** Build references from recognized sources. When AI models "
            "see your brand mentioned alongside credible references, they treat your content "
            "as more reliable for generative answers.\n\n"
            "**Structured Data:** Implement FAQ schema, HowTo schema, and other structured data "
            "types that AI systems use to extract and present information in search results.\n"
        )
        
        if '## Frequently Asked Questions' in post_content:
            post_content = post_content.replace('## Frequently Asked Questions', 
                                                geo_content + '\n## Frequently Asked Questions', 1)
        elif '## Conclusion' in post_content:
            post_content = post_content.replace('## Conclusion', 
                                                geo_content + '\n## Conclusion', 1)
        else:
            post_content += '\n' + geo_content
        
        modifications.append("Added GEO section")
        print("  + Added GEO section")
    
    # --- 4. Add EEAT section if missing ---
    if not has_eeat:
        eeat_section = (
            "\n## E-E-A-T: Building Trust and Authority\n\n"
            "Google's E-E-A-T framework — Experience, Expertise, Authoritativeness, and Trustworthiness — "
            "is more important than ever in 2026, especially with the rise of AI-generated content. "
            "As **Md Kanok Miah**, a recognized SEO professional with extensive experience optimizing "
            "Bangladeshi websites, I ensure every piece of content on this site meets the highest E-E-A-T standards.\n\n"
            "**Experience:** Over a decade of hands-on SEO work with businesses in Dhaka, Chittagong, "
            "Sylhet, and across Bangladesh — from small local shops to large e-commerce platforms.\n\n"
            "**Expertise:** Specialized knowledge in Bangladeshi search behavior, local SEO, "
            "technical optimization, and content marketing tailored to the Bangladesh market.\n\n"
            "**Authoritativeness:** Featured and cited across Bangladeshi digital platforms, "
            "with a portfolio of successful SEO campaigns that have transformed businesses.\n\n"
            "**Trustworthiness:** Transparent reporting, ethical SEO practices, and a commitment "
            "to delivering genuine, lasting results for every client.\n\n"
            "When you read my content, you are getting advice backed by real, verifiable results — "
            "not generic SEO tips copied from international sources.\n"
        )
        
        if '## Frequently Asked Questions' in post_content:
            post_content = post_content.replace('## Frequently Asked Questions', 
                                                eeat_section + '\n## Frequently Asked Questions', 1)
        elif '## Conclusion' in post_content:
            post_content = post_content.replace('## Conclusion', 
                                                eeat_section + '\n## Conclusion', 1)
        else:
            post_content += '\n' + eeat_section
        
        modifications.append("Added EEAT section")
        print("  + Added EEAT section")
    
    # --- 5. Add FAQ Schema JSON-LD ---
    if has_faq and not has_qa_schema:
        faq_lines = post_content.split('\n')
        faq_start = -1
        faq_end = -1
        for idx, line in enumerate(faq_lines):
            if '## Frequently Asked Questions' in line:
                faq_start = idx
            if faq_start > 0 and idx > faq_start and line.strip().startswith('## ') and 'Frequently Asked' not in line:
                faq_end = idx
                break
            if faq_start > 0 and idx > faq_start and line.strip().startswith('## Conclusion'):
                faq_end = idx
                break
        
        if faq_start > 0:
            faq_pairs = []
            current_q = None
            current_a_lines = []
            
            for line in faq_lines[faq_start:]:
                stripped = line.strip()
                if stripped.startswith('### '):
                    if current_q and current_a_lines:
                        faq_pairs.append((current_q, ' '.join(current_a_lines)))
                    current_q = stripped.replace('### ', '')
                    current_a_lines = []
                elif current_q and stripped and not stripped.startswith('#') and not stripped.startswith('|') and not stripped.startswith('<!--'):
                    current_a_lines.append(stripped)
                elif stripped.startswith('## ') and current_q and 'Frequently Asked' not in stripped:
                    break
            
            if current_q and current_a_lines:
                faq_pairs.append((current_q, ' '.join(current_a_lines)))
            
            if faq_pairs:
                faq_schema = {
                    "@context": "https://schema.org",
                    "@type": "FAQPage",
                    "mainEntity": []
                }
                for q, a in faq_pairs:
                    if q and a:
                        faq_schema["mainEntity"].append({
                            "@type": "Question",
                            "name": q.rstrip('?') + '?',
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": a.strip()
                            }
                        })
                
                schema_block = (
                    '\n\n<!-- FAQ Schema structured data -->\n'
                    '<script type="application/ld+json">\n'
                    + json.dumps(faq_schema, indent=2) +
                    '\n</script>'
                )
                
                post_content = post_content.replace(
                    '## Frequently Asked Questions',
                    '## Frequently Asked Questions' + schema_block,
                    1
                )
                modifications.append(f"Added FAQ schema with {len(faq_pairs)} Q&A pairs")
                print(f"  + Added FAQ schema with {len(faq_pairs)} Q&A pairs")
    
    # --- 6. Add industry-specific links where sparse ---
    if len(industry_links) < 2:
        industry_snippet = (
            f"\n\nWhether you operate in the "
            f"[e-commerce and retail industry](/industries/ecommerce-retail), "
            f"[food and restaurant sector](/industries/food-restaurant), "
            f"or [real estate market](/industries/real-estate), "
            f"our SEO strategies are tailored to your specific industry needs."
        )
        
        if '## Frequently Asked Questions' in post_content:
            post_content = post_content.replace(
                '## Frequently Asked Questions',
                industry_snippet + '\n\n## Frequently Asked Questions',
                1
            )
            modifications.append("Added industry links before FAQ")
            print("  + Added industry links before FAQ")
        elif '## Conclusion' in post_content:
            post_content = post_content.replace(
                '## Conclusion',
                industry_snippet + '\n\n## Conclusion',
                1
            )
            modifications.append("Added industry links before Conclusion")
            print("  + Added industry links before Conclusion")
    
    # --- 7. Add service links where sparse ---
    if len(service_links) < 2:
        services_snippet = (
            "\n\nFor expert SEO support tailored to your business, explore our "
            "[professional local SEO services](/services/local-seo), "
            "[comprehensive on-page SEO services](/services/on-page-seo), and "
            "[technical SEO services](/services/technical-seo). "
            "Each service is designed for the unique needs of Bangladeshi businesses."
        )
        
        post_content = post_content.rstrip() + services_snippet + '\n'
        modifications.append("Added service links at end")
        print("  + Added service links at end")
    
    # Update the content in the file
    if post_content != original_content:
        changes = len(post_content) - len(original_content)
        direction = 'grown' if changes > 0 else 'shrunk'
        print(f"  Content {direction} by {abs(changes)} chars")
        
        new_content = content[:content_start] + post_content + content[bt_close:]
        content = new_content
        print(f"  Modifications: {', '.join(modifications)}")
    else:
        print(f"  No changes needed")

# Write the updated file
with open('src/app/blog/data.js', 'w') as f:
    f.write(content)

print(f"\n{'='*60}")
print(f"Batch 1 processing complete. {BATCH_SIZE} posts processed.")
print(f"Processed slugs: {', '.join(processed_slugs)}")
print(f"{'='*60}")
