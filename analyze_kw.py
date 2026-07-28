#!/usr/bin/env python3
import re

s = """## The Challenge: Starting from Absolute Zero
Dhaka Apparels started from absolute zero — a completely new domain with no authority, no indexed pages, no backlinks, no Google Business Profile, and no local search presence. They were competing against established garments suppliers with 5+ years of SEO history, hundreds of indexed pages, and strong backlink profiles.

In Bangladesh $50+ billion RMG (Ready-Made Garments) sector, Dhaka Apparels was entering a market where every competitor had years of head start in online visibility.

## The Solution: Five-Phase Structured Plan

### Phase 1: Foundation

A lead-generation website was built with under 200ms server response time and under 2 seconds mobile load speed. The design was mobile-first with click-to-call functionality, SEO-optimized URL structure, and logical internal linking architecture.

### Phase 2: Content That Converts

Instead of generic descriptions, we addressed real B2B buyer objections: MOQ (Minimum Order Quantity), export documentation, and quality grading. Dedicated pages were created for each service category with depth over volume — preferring comprehensive, authoritative content over thin, keyword-stuffed pages.

### Phase 3: Technical SEO and AI Readiness

Schema markup (Organization and Product) was implemented alongside Core Web Vitals optimization achieving all Good scores. Structured FAQ blocks were designed specifically for AI-generated search summaries — anticipating how Google Search Generative Experience would display content.

### Phase 4: Local SEO

The Google Business Profile was fully optimized with real photos of the facility and products. NAP consistency was ensured across all platforms. Location-targeted keywords were integrated throughout the content.

### Phase 5: Authority Building

Selective, contextual backlinks were earned from trade directories and B2B platforms only. Quality was prioritized over quantity, with every backlink adding genuine value to the site's authority profile.

## The Results

The impact was achieved in just 90 days:

- **Top Keyword Ranking**: #1 for "best stock garments supplier in bd"
- **Impressions (90 days)**: 14,700
- **AI Search Appearances**: Featured in Google AI-generated search summaries
- **Domain Authority**: 0 (started as brand new domain)
- **Timeline**: 90 days from zero to #1
- **Ad Spend**: $0

## Key Takeaways for New Domains

This case study proves that new domains can compete and win against established competitors. The key is a strategic, phased approach that prioritizes technical excellence, conversion-focused content, and AI-readiness from day one.

As the **best SEO expert in Dhaka**, I specialize in helping Bangladeshi garment manufacturers and B2B businesses achieve rapid SEO results on new domains. Visit [kanokmiah.com.bd](https://kanokmiah.com.bd/) to learn how we can take your business from zero to #1 in your market.

- [B2B SEO](/blog/b2b-lead-generation-seo-bangladesh) — B2B Lead Generation SEO
- Garments & Textile industry — Garments & Textile SEO
- [Mir Cement case study](/blog/mir-cement-seo-case-study) — Mir Cement Case Study

## Conclusion

Dhaka Apparels achievement of #1 ranking in 90 days on a brand new domain demonstrates that with the right strategy, new entrants can dominate even competitive B2B markets. Technical excellence, buyer-focused content, and AI readiness are the keys to rapid SEO success.
    
আপনার সাইটের জন্য [গার্মেন্টস ও টেক্সটাইল শিল্পের জন্য SEO পৃষ্ঠা](/industries/garments-textile)-এর মাধ্যমে আরও উন্নত SEO ফলাফল পেতে পারেন। গার্মেন্টস শিল্পের জন্য শিল্প-নির্দিষ্ট SEO কৌশল সম্পর্কে বিস্তারিত জানতে আমাদের ইন্ডাস্ট্রি পৃষ্ঠা দেখুন।

Looking for the professional SEO services.

**[SEO services in Dhaka neighborhoods](/locations/dhaka)**.
Looking for the best SEO expert in Bangladesh.

Looking for the [SEO expert in Dhaka](/).
"""

print("=== Keyword: 'case study' (all forms) ===")
pattern1 = re.compile(r"[Cc]ase\s+[Ss]tud[\w]*")
matches1 = pattern1.findall(s)
for m in matches1:
    print(f"  '{m}'")
print(f"Total: {len(matches1)}")

print()
print("=== Keyword: 'SEO' (case insensitive) ===")
pattern2 = re.compile(r"[Ss][Ee][Oo]")
matches2 = pattern2.findall(s)
print(f"Total occurrences: {len(matches2)}")

print()
print("=== 'SEO' adjacent to 'case study' ===")
# Check if SEO appears near case study
pattern3 = re.compile(r"[Cc]ase\s+[Ss]tud[\w]*")
for m in pattern1.finditer(s):
    start = max(0, m.start() - 50)
    end = min(len(s), m.end() + 50)
    context = s[start:end].replace('\n', ' ')
    print(f"  Context: ...{context}...")

print()
print("=== Headings (H2/H3) ===")
for line in s.split('\n'):
    if line.startswith('## ') or line.startswith('### '):
        print(f"  {line.strip()}")
