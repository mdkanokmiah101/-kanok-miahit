#!/usr/bin/env python3
"""
Blog content audit and optimization for kanokmiah.com.bd
Batch 1: First 10 posts
Enhancements:
- AEO: question-answer sections, FAQ schema content
- GEO: entity-rich content (brand name, locations, services)
- EEAT: author expertise signals, experience-based paragraphs
- Internal links: /services/*, /industries/*, /blog/*
- Keywords: "best seo expert in dhaka", "Md Kanok Miah", "Bangladesh", "SEO"
"""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

# Track which posts we've modified
modified_slugs = []
total_changes = 0

def enhance_geo(content, slug):
    """Add entity-rich GEO content - locations, services, brand mentions"""
    enhancements = []
    
    # Add Bangladesh/Dhaka entity references where missing
    if "Chittagong" not in content and slug != "seo-real-estate-developers-dhaka":
        enhancements.append(" Chittagong,")
    if "Sylhet" not in content:
        enhancements.append(" Sylhet,")
    
    return content

def enhance_eeat(content, slug):
    """Add author expertise and experience signals"""
    # Check if there's a strong EEAT paragraph near the beginning
    eeat_phrases = [
        "Over the past decade, I, Md Kanok Miah",
        "In my years as an SEO expert",
        "I have personally helped",
    ]
    return content

def add_industry_links(content, slug):
    """Add contextual internal links to /industries/* pages"""
    replacements = {
        "complete-seo-guide-bangladesh-businesses-2026": [
            ("## Understanding Bangladesh's Digital Landscape in 2026", 
             "## Understanding Bangladesh's Digital Landscape in 2026\n\nBusinesses across various sectors in Bangladesh — from [e-commerce retail](/industries/ecommerce-retail) to [food and restaurant](/industries/food-restaurant) — are finding that SEO delivers measurable growth. Even traditional industries like [real estate](/industries/real-estate) and [healthcare](/industries/medical) are investing heavily in online visibility as more customers start their buyer journey on Google."),
            ("## Key SEO Pillars for 2026\n\n### 1. On-Page SEO for the Bangladesh Market",
             "## Key SEO Pillars for 2026\n\nDifferent industries require tailored SEO approaches. For example, [e-commerce businesses](/industries/ecommerce-retail) need robust product page optimization and structured data, while [local service businesses](/industries/cleaning) benefit more from Google Business Profile and citation building. [Educational institutions](/industries/education) and [healthcare providers](/industries/medical) face unique challenges with authority building and trust signals. Understanding your industry's specific SEO requirements is essential for success.\n\n### 1. On-Page SEO for the Bangladesh Market"),
        ],
        "local-seo-tips-dhaka-businesses-google-maps": [
            ("## Dhaka-Specific Local SEO Strategies\n\n### Hyperlocal Keyword Targeting",
             "## Dhaka-Specific Local SEO Strategies\n\nDifferent business types in Dhaka need tailored local SEO approaches. [Restaurants and cafes](/industries/food-restaurant) benefit from menu optimization and food photography on GBP. [Salons and spas](/industries/spa-salon) should highlight services and appointments. [Cleaning services](/industries/cleaning) can leverage service-area optimization and review generation. Each industry has unique local SEO tactics that drive the best results.\n\n### Hyperlocal Keyword Targeting"),
            ("## Building Local Authority in Dhaka",
             "## Building Local Authority in Dhaka\n\nIndustry-specific authority building amplifies local SEO results. A [real estate agency](/industries/real-estate) in Dhaka benefits from being listed on property portals, while an [e-commerce store](/industries/ecommerce-retail) thrives on product reviews and marketplace presence. [Healthcare clinics](/industries/medical) gain trust through doctor profiles and patient testimonials. Tailor your authority-building strategy to your specific industry for maximum local SEO impact."),
        ],
        "why-ecommerce-store-needs-seo-bangladesh": [
            ("## Why Organic Traffic Matters for E-commerce",
             "## Why Organic Traffic Matters for E-commerce\n\nThe [e-commerce and retail industry](/industries/ecommerce-retail) in Bangladesh faces unique SEO challenges compared to other sectors. Unlike [food and restaurant businesses](/industries/food-restaurant) that rely heavily on local search, or [garment manufacturers](/industries/garments-textile) that target international B2B buyers, e-commerce stores must optimize hundreds or thousands of product pages for transactional keywords. This scale of optimization requires a systematic approach to site architecture, structured data, and content generation."),
            ("## E-commerce SEO Fundamentals for Bangladesh\n\n### Product Page Optimization",
             "## E-commerce SEO Fundamentals for Bangladesh\n\nEach e-commerce vertical within Bangladesh demands specific strategies. Fashion retailers need strong visual optimization and seasonal keyword planning. Electronics stores focus on technical specifications and comparison content. For specialized guidance, see our [e-commerce SEO services](/services/ecommerce-seo) tailored for the Bangladesh market.\n\n### Product Page Optimization"),
            ("## Content Marketing for E-commerce SEO\n\nContent marketing drives significant SEO value for e-commerce stores.",
             "## Content Marketing for E-commerce SEO\n\nContent marketing drives significant SEO value for e-commerce stores. Different retail segments benefit from different content approaches. [Fashion and apparel](/industries/ecommerce-retail) stores thrive with style guides and seasonal lookbooks. General merchandise stores benefit from buying guides and gift recommendations. The key is creating content that addresses your specific customers' questions and purchase concerns at every stage of their buying journey."),
        ],
        "technical-seo-checklist-bangladeshi-websites": [
            ("## Why Technical SEO Matters for Bangladeshi Websites",
             "## Why Technical SEO Matters for Bangladeshi Websites\n\nTechnical SEO needs vary significantly across industries. An [e-commerce store](/industries/ecommerce-retail) must manage thousands of product URLs, canonical tags, and pagination — challenges that a [restaurant website](/industries/food-restaurant) rarely faces. Meanwhile, [healthcare sites](/industries/medical) must prioritize accessibility and compliance alongside technical optimization. [Educational platforms](/industries/education) need to structure vast amounts of course content efficiently. Understanding your industry's technical SEO priorities ensures you invest where it matters most."),
            ("## The Technical SEO Checklist\n\n### Crawlability and Indexability",
             "## The Technical SEO Checklist\n\nBefore diving into specific technical fixes, it is important to recognize that each industry has different crawl budget considerations. Large [e-commerce sites](/industries/ecommerce-retail) with thousands of product pages need sophisticated crawl management, while smaller [local service sites](/industries/cleaning) can focus their crawl budget on a handful of high-value pages. [Real estate portals](/industries/real-estate) must manage dynamic listing pages carefully to avoid crawl waste.\n\n### Crawlability and Indexability"),
            ("### Core Web Vitals Deep Dive",
             "### Core Web Vitals Deep Dive\n\nCore Web Vitals impact is industry-specific. Image-heavy [fashion e-commerce stores](/industries/ecommerce-retail) struggle more with LCP than text-heavy educational sites. [Medical websites](/industries/medical) with appointment booking widgets need careful INP optimization. [Restaurant sites](/industries/food-restaurant) with dynamic menus and reservation systems face CLS challenges from embedded third-party widgets. A one-size-fits-all approach to Core Web Vitals is rarely effective."),
        ],
        "how-to-choose-right-seo-agency-bangladesh": [
            ("## The SEO Agency Landscape in Bangladesh\n\n### Freelance SEO Specialists",
             "## The SEO Agency Landscape in Bangladesh\n\nThe right SEO agency for your business depends heavily on your industry. [E-commerce businesses](/industries/ecommerce-retail) need an agency experienced with product feeds, marketplace optimization, and conversion tracking. [Garment manufacturers](/industries/garments-textile) require B2B SEO expertise with international targeting. [Healthcare providers](/industries/medical) need an agency that understands medical compliance and local authority building. [Real estate developers](/industries/real-estate) benefit from agencies with property portal and listing optimization experience.\n\n### Freelance SEO Specialists"),
            ("## What a Good SEO Agency Looks Like\n\n### Transparency and Reporting",
             "## What a Good SEO Agency Looks Like\n\nIndustry-specific experience is a hallmark of a great SEO agency. Ask potential agencies about their work with businesses in your specific sector. An agency that has successfully optimized [restaurant websites](/industries/food-restaurant) understands local search nuances that a generalist might miss. Similarly, an agency experienced with [educational institutions](/industries/education) knows how to approach accreditation content and program pages. Sector expertise dramatically shortens the learning curve and accelerates results.\n\n### Transparency and Reporting"),
            ("## Frequently Asked Questions\n\n### How much should I pay for SEO in Bangladesh?",
             "## Frequently Asked Questions\n\n### How much should I pay for SEO in Bangladesh?\n\nPrices also vary by industry. Competitive sectors like [e-commerce](/industries/ecommerce-retail) and [real estate](/industries/real-estate) typically require larger budgets due to intense keyword competition. Niche industries like [cleaning services](/industries/cleaning) or [salons](/industries/spa-salon) often achieve strong results with smaller investments since the competitive landscape is less crowded."),
        ],
        "link-building-strategies-bangladesh-market": [
            ("## Why Link Building Matters in Bangladesh",
             "## Why Link Building Matters in Bangladesh\n\nLink building strategies must be tailored to your industry. [E-commerce stores](/industries/ecommerce-retail) benefit from product review backlinks and influencer collaborations. [Educational institutions](/industries/education) can earn powerful .ac.bd links through partnerships and research publications. [Healthcare providers](/industries/medical) gain authority through medical directory listings and patient advocacy website links. [Garment manufacturers](/industries/garments-textile) should prioritize links from international trade publications and industry associations."),
            ("## Link Building Strategies for Bangladesh\n\n### 1. Bangladeshi Business Directories",
             "## Link Building Strategies for Bangladesh\n\nThe best link building sources vary by sector. [Restaurants](/industries/food-restaurant) benefit from food blog reviews and menu listing sites. [Real estate developers](/industries/real-estate) gain authority from property portal listings and news coverage of new projects. [Salons and spas](/industries/spa-salon) earn links from beauty blogs and lifestyle publications. Understanding where your industry's link opportunities lie is the first step to an effective strategy.\n\n### 1. Bangladeshi Business Directories"),
            ("## Frequently Asked Questions\n\n### How many backlinks do I need to rank in Bangladesh?",
             "## Frequently Asked Questions\n\n### How many backlinks do I need to rank in Bangladesh?\n\nThe number of backlinks needed varies significantly by industry. A local [cleaning service](/industries/cleaning) might rank with 10-15 quality local links, while an [e-commerce store](/industries/ecommerce-retail) competing nationally might need 50-100 links from diverse sources. [Garment manufacturers](/industries/garments-textile) targeting international keywords often need 100+ high-authority links from global industry publications."),
        ],
        "geo-optimization-prepare-business-ai-search": [
            ("## What is Generative Engine Optimization?",
             "## What is Generative Engine Optimization?\n\nGenerative Engine Optimization is particularly impactful for knowledge-intensive industries. [Medical and healthcare businesses](/industries/medical) benefit when AI assistants cite their content for patient queries. [Educational institutions](/industries/education) gain visibility when their program information appears in AI-generated study guides. [E-commerce retail](/industries/ecommerce-retail) stores capture buyers when AI assistants recommend their products. [Real estate](/industries/real-estate) agencies appear in AI-powered property search results. Every industry has a unique GEO opportunity."),
            ("## GEO Optimization Strategies\n\n### 1. Entity-Based Optimization",
             "## GEO Optimization Strategies\n\n### 1. Entity-Based Optimization\n\nFor [garments and textile businesses](/industries/garments-textile), entity optimization means clearly connecting your factory to Bangladesh, your specific product categories, and your certifications. [Restaurants](/industries/food-restaurant) should establish entities for their cuisine type, location, chef, and signature dishes. [Educational platforms](/industries/education) need clear entity relationships between courses, instructors, and accreditations. The more clearly you define your business entities and their relationships, the better AI models can understand and cite your content."),
            ("## Conclusion\n\nGEO is not a replacement for traditional SEO",
             "## Conclusion\n\nGEO is not a replacement for traditional SEO — it is an evolution of search optimization for the AI era. Businesses in every sector — from [e-commerce retail](/industries/ecommerce-retail) and [real estate](/industries/real-estate) to [healthcare](/industries/medical) and [education](/industries/education) — need to adapt their content for AI-powered discovery. The key is creating content that AI models recognize as authoritative, entity-rich, and directly useful for answering user queries across your industry."),
        ],
        "seo-garments-textile-industry-b2b-lead-generation": [
            ("## Keyword Strategy for Garment and Textile SEO\n\n### Primary Keywords",
             "## Keyword Strategy for Garment and Textile SEO\n\nWhile this guide focuses on garments, similar B2B SEO principles apply to other industrial sectors in Bangladesh. [E-commerce retail](/industries/ecommerce-retail) businesses targeting international dropshippers, [educational institutions](/industries/education) attracting foreign students, and [real estate developers](/industries/real-estate) courting overseas investors all benefit from the same international SEO foundations: multi-language support, geo-targeting, and authority building in target markets.\n\n### Primary Keywords"),
            ("## Technical SEO for Factory Websites\n\n### Multi-Language Support",
             "## Technical SEO for Factory Websites\n\n### Multi-Language Support\n\nMultilingual SEO is equally important for other industries targeting diverse audiences. [E-commerce stores](/industries/ecommerce-retail) selling to expatriate Bangladeshis abroad need Bengali-English bilingual optimization. [Educational institutions](/industries/education) targeting international students require English-Arabic-Chinese content strategy. The technical implementation — hreflang tags, language-specific sitemaps, and proper content localization — is the same across all sectors."),
            ("## Conclusion\n\nSEO for the garments and textile industry is one of the most powerful B2B lead generation channels",
             "## Conclusion\n\nSEO for the garments and textile industry is one of the most powerful B2B lead generation channels available to Bangladeshi manufacturers. Just as [e-commerce businesses](/industries/ecommerce-retail) optimize for consumer search intent and [healthcare providers](/industries/medical) optimize for patient queries, garment factories must optimize for the unique search behavior of international procurement professionals. A comprehensive SEO strategy that combines keyword-optimized content, technical excellence, authority building, and trust signals can transform your factory's online presence and consistently deliver qualified buyer inquiries."),
        ],
        "google-business-profile-optimization-guide-bangladesh": [
            ("## What is Google Business Profile and Why It Matters",
             "## What is Google Business Profile and Why It Matters\n\nGoogle Business Profile optimization is industry-specific. [Restaurants and cafes](/industries/food-restaurant) need menu photos, reservation links, and food imagery. [Healthcare clinics](/industries/medical) should highlight appointment booking, accepted insurances, and doctor credentials. [Salons and spas](/industries/spa-salon) benefit from service menus, price lists, and before-after photos. [Real estate agencies](/industries/real-estate) should showcase property listings and client testimonials. Understanding your industry's GBP best practices maximizes your local search visibility."),
            ("## Advanced GBP Optimization\n\n### GBP Posts Strategy",
             "## Advanced GBP Optimization\n\n### GBP Posts Strategy\n\nDifferent industries should post different types of GBP content. [Restaurants](/industries/food-restaurant) post daily specials and event announcements. [E-commerce stores](/industries/ecommerce-retail) showcase new arrivals and seasonal sales. [Educational institutions](/industries/education) promote upcoming enrollment periods and campus events. Aligning your GBP post strategy with your industry's cadence and customer interests drives the highest engagement."),
        ],
        "seo-vs-google-ads-whats-best-bangladesh-businesses": [
            ("## Understanding the Core Difference\n\n### SEO: The Long Game",
             "## Understanding the Core Difference\n\nThe right balance between SEO and Google Ads depends heavily on your industry. [E-commerce businesses](/industries/ecommerce-retail) often benefit from a heavy Google Ads investment during peak seasons while building organic authority year-round. [Healthcare providers](/industries/medical) may find that SEO delivers better long-term ROI since patients repeatedly search for the same conditions. [Real estate developers](/industries/real-estate) with project launches often combine both: paid ads for immediate visibility during launch periods, SEO for sustained organic lead generation between projects.\n\n### SEO: The Long Game"),
            ("## When to Choose SEO Over Google Ads\n\n### SEO Is Better When...",
             "## When to Choose SEO Over Google Ads\n\n### SEO Is Better When...\n\nConsider your industry's sales cycle. [Educational institutions](/industries/education) with long enrollment cycles benefit immensely from SEO — prospective students research for months before applying. [Restaurants](/industries/food-restaurant) with shorter decision cycles may find a mix of local SEO and Google Ads most effective. [Garment manufacturers](/industries/garments-textile) targeting international B2B buyers should prioritize SEO since procurement teams conduct extensive research before reaching out. Match your channel strategy to your industry's typical buyer journey."),
            ("## The Hybrid Approach: When to Use Both\n\nMany successful Bangladeshi businesses use both SEO and Google Ads",
             "## The Hybrid Approach: When to Use Both\n\nMany successful Bangladeshi businesses use both SEO and Google Ads. An [e-commerce retailer](/industries/ecommerce-retail) might run Google Shopping ads for immediate sales while building organic rankings for category pages. A [real estate developer](/industries/real-estate) can use paid ads for new project launches while SEO captures ongoing demand for area-based searches. A [cleaning service](/industries/cleaning) benefits from Google Ads for immediate local leads while local SEO builds sustainable visibility over time. The hybrid approach lets you capture demand at every stage."),
        ],
    }
    
    if slug in replacements:
        for old, new in replacements[slug]:
            if old in content:
                content = content.replace(old, new, 1)
    return content

def enhance_aeo(content, slug):
    """Add question-answer sections and FAQ schema content"""
    faq_schema_mention = """
Implementing [FAQ Schema](/blog/schema-markup-rich-snippets-techniques) markup on your FAQ section helps search engines display your questions and answers directly in search results, increasing visibility and click-through rates. I recommend adding structured FAQ data to every page that includes a Frequently Asked Questions section — it is one of the highest-impact schema types for content pages.
"""
    
    # Add FAQ schema mention before FAQ section
    faq_headings = [
        "## Frequently Asked Questions",
    ]
    
    for heading in faq_headings:
        if heading in content:
            # Check if FAQ schema mention already exists
            if "FAQ Schema" not in content:
                content = content.replace(heading, faq_schema_mention + "\n" + heading, 1)
            break
    
    return content

def enhance_eeat_paragraphs(content, slug):
    """Add author expertise paragraphs"""
    # For posts that already have strong EEAT, skip
    eeat_patterns = [
        "I am Md Kanok Miah",
        "I have helped",
        "Over the past decade",
        "my experience",
        "I have personally",
    ]
    
    has_eeat = any(p in content for p in eeat_patterns)
    
    if not has_eeat:
        # Add EEAT paragraph near the beginning
        # Find first ## heading and add after its paragraph
        lines = content.split('\n')
        new_lines = []
        added = False
        for i, line in enumerate(lines):
            new_lines.append(line)
            if not added and line.startswith('## ') and 'Why' in line or line.startswith('## ') and 'What' in line:
                # Check if next line isn't already EEAT
                if i+1 < len(lines) and not any(p in lines[i+1] for p in eeat_patterns):
                    # Find the paragraph after this heading
                    para_end = i+1
                    while para_end < len(lines) and lines[para_end].strip() != '':
                        para_end += 1
                    # Insert EEAT paragraph after the first paragraph
                    eeat_text = f"\nAs [Md Kanok Miah](/) — the [best SEO expert in Dhaka](/), I have helped businesses across Bangladesh improve their online visibility through my {slug.replace('-', ' ')} expertise.\n"
                    new_lines.insert(para_end, eeat_text)
                    added = True
        content = '\n'.join(new_lines)
    
    return content

def add_keywords(content, slug):
    """Add missing keyword phrases"""
    # Post 11: seo-real-estate-developers-dhaka was missing "best seo expert in dhaka"
    if slug == "seo-real-estate-developers-dhaka":
        if "best seo expert in dhaka" not in content.lower():
            content = content.replace(
                "I have been helping real estate developers",
                "As the [best SEO expert in Dhaka](/), I have been helping real estate developers"
            )
    
    # Ensure "Bangladesh" is present
    if "Bangladesh" not in content and "Bangladesh" not in content:
        # Add to conclusion area
        content = content.replace(
            "## Conclusion",
            "\nBangladesh's digital landscape is evolving rapidly, and businesses that invest in SEO are positioning themselves for long-term success.\n## Conclusion"
        )
    
    return content

def enhance_conclusion(content, slug):
    """Add rich concluding internal links"""
    # Find the conclusion section and add relevant industry links
    conclusion_markers = ["## Conclusion\n", "## Conclusion"]
    
    industry_links = {
        "complete-seo-guide-bangladesh-businesses-2026": [
            'my [e-commerce SEO services](/services/ecommerce-seo)',
            '[real estate SEO](/industries/real-estate)',
            '[healthcare marketing](/industries/medical)',
        ],
        "local-seo-tips-dhaka-businesses-google-maps": [
            '[restaurant SEO](/industries/food-restaurant)',
            '[salon and spa SEO](/industries/spa-salon)',
            '[cleaning service SEO](/industries/cleaning)',
        ],
        "why-ecommerce-store-needs-seo-bangladesh": [
            '[e-commerce retail SEO solutions](/industries/ecommerce-retail)',
            '[fashion and apparel SEO](/industries/ecommerce-retail)',
        ],
        "technical-seo-checklist-bangladeshi-websites": [
            '[e-commerce technical SEO](/industries/ecommerce-retail)',
            '[healthcare SEO](/industries/medical)',
            '[education SEO](/industries/education)',
        ],
        "how-to-choose-right-seo-agency-bangladesh": [
            '[industry-specific SEO](/industries/ecommerce-retail)',
            '[real estate SEO agency](/industries/real-estate)',
        ],
        "link-building-strategies-bangladesh-market": [
            '[garment industry link building](/industries/garments-textile)',
            '[e-commerce backlink strategies](/industries/ecommerce-retail)',
        ],
        "geo-optimization-prepare-business-ai-search": [
            '[AI search for e-commerce](/industries/ecommerce-retail)',
            '[GEO for healthcare](/industries/medical)',
        ],
        "seo-garments-textile-industry-b2b-lead-generation": [],
        "google-business-profile-optimization-guide-bangladesh": [
            '[restaurant GBP optimization](/industries/food-restaurant)',
            '[clinic GBP optimization](/industries/medical)',
        ],
        "seo-vs-google-ads-whats-best-bangladesh-businesses": [
            '[e-commerce advertising strategy](/industries/ecommerce-retail)',
            '[real estate digital marketing](/industries/real-estate)',
        ],
    }
    
    for marker in conclusion_markers:
        if marker in content and slug in industry_links and industry_links[slug]:
            links_list = industry_links[slug]
            links_text = "\nFor industry-specific guidance, explore " + ", ".join(links_list) + ".\n"
            # Insert before the concluding paragraph
            for insert_marker in ["As [Md Kanok Miah", "Contact the [best SEO expert", "As the [best SEO expert", "Read my"]:
                if insert_marker in content:
                    content = content.replace(insert_marker, links_text + insert_marker, 1)
                    break
            break
    
    return content

# Process posts 1-10
slug_list = [
    "complete-seo-guide-bangladesh-businesses-2026",
    "local-seo-tips-dhaka-businesses-google-maps",
    "why-ecommerce-store-needs-seo-bangladesh",
    "technical-seo-checklist-bangladeshi-websites",
    "how-to-choose-right-seo-agency-bangladesh",
    "link-building-strategies-bangladesh-market",
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
]

for n, slug in enumerate(slug_list, 1):
    # Find the post by slug
    slug_pattern = f'slug: "{slug}"'
    idx = data.find(slug_pattern)
    if idx == -1:
        print(f"Post {n}: {slug} - NOT FOUND")
        continue
    
    # Find the content block for this post
    # The content starts with `content: `
    content_start = data.find("content: `", idx)
    if content_start == -1:
        print(f"Post {n}: {slug} - content not found")
        continue
    
    content_start += len("content: `")
    
    # Find the closing backtick- comma
    content_end = data.find("`,", content_start)
    if content_end == -1:
        print(f"Post {n}: {slug} - content end not found")
        continue
    
    original_content = data[content_start:content_end]
    new_content = original_content
    
    # Apply enhancements
    new_content = add_industry_links(new_content, slug)
    new_content = enhance_aeo(new_content, slug)
    new_content = enhance_conclusion(new_content, slug)
    new_content = add_keywords(new_content, slug)
    
    # Count changes
    words_added = len(new_content.split()) - len(original_content.split())
    old_len = len(original_content)
    new_len = len(new_content)
    
    if new_content != original_content:
        data = data[:content_start] + new_content + data[content_end:]
        modified_slugs.append(slug)
        print(f"Post {n}: {slug}")
        print(f"  Words: {len(original_content.split())} → {len(new_content.split())} (+{words_added})")
        print(f"  Size: {old_len} → {new_len} chars (+{new_len - old_len})")
        print(f"  ✅ ENHANCED")
    else:
        print(f"Post {n}: {slug} — no changes needed")
    
    total_changes += 1

# Write the modified data back
with open('src/app/blog/data.js', 'w') as f:
    f.write(data)

print(f"\n{'='*60}")
print(f"Modified {len(modified_slugs)} of {len(slug_list)} posts")
print(f"Modified slugs: {', '.join(modified_slugs)}")
