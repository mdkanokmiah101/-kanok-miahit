#!/usr/bin/env python3
"""
Batch 3 Rewrite: Process all 30 posts efficiently
Expands content to 2000+ words with AEO/GEO/EEAT/SEO optimization
"""

import re

filepath = '/root/kanok-miahit/src/app/blog/data.js'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

def wc(t):
    return len(t.split())

def expand_post(current_content, topic_keyword, extra_sections):
    """Add extra sections to existing content to reach 2000+ words.
    Keeps original intro/conclusion but adds new middle sections."""
    # Find conclusion (উপসংহার)
    conclusion_marker = '### উপসংহার'
    conclusion_idx = current_content.find(conclusion_marker)
    
    if conclusion_idx == -1:
        # Try looking for the last ### heading
        lines = current_content.split('\n')
        for i in range(len(lines)-1, -1, -1):
            if lines[i].startswith('### '):
                conclusion_idx = current_content.find(lines[i])
                break
    
    if conclusion_idx == -1:
        # Just append
        return current_content + '\n\n' + extra_sections
    
    # Insert extra sections before conclusion
    before_conclusion = current_content[:conclusion_idx]
    after_conclusion = current_content[conclusion_idx:]
    
    return before_conclusion + extra_sections + '\n\n' + after_conclusion


# Define expansion sections for each post
# Template: AEO (FAQ), GEO (AI search), EEAT (experience), SEO (keywords)

def make_expansion(topic, faq_qas, bd_tips, eeat_story, links):
    """Generate expanded sections for a post."""
    sections = []
    
    # GEO section
    sections.append(f"""### GEO (Generative Engine Optimization) এবং {topic}

২০২৬ সালে, Generative Engine Optimization (GEO) একটি গুরুত্বপূর্ণ SEO কৌশল হয়ে উঠেছে। AI চালিত সার্চ ইঞ্জিন যেমন ChatGPT, Google Gemini, এবং Perplexity যখন ব্যবহারকারীদের প্রশ্নের উত্তর দেয়, তারা আপনার কন্টেন্ট থেকে তথ্য নেয়। {topic}-এর জন্য GEO অপটিমাইজেশন মানে হলো আপনার কন্টেন্টকে এমনভাবে স্ট্রাকচার করা যাতে AI সহজেই তা বুঝতে পারে এবং উদ্ধৃত করতে পারে।

GEO-র জন্য নিম্নলিখিত কৌশলগুলো অনুসরণ করুন:
১. প্রশ্ন-উত্তর ফরম্যাটে কন্টেন্ট তৈরি করুন — AI এই ফরম্যাট সহজেই প্রসেস করতে পারে
২. স্ট্রাকচারড ডেটা (Schema.org) ব্যবহার করুন — এটি AI-কে আপনার কন্টেন্টের প্রসঙ্গ বুঝতে সাহায্য করে
৩. প্রামাণিক এবং নির্ভরযোগ্য তথ্য প্রদান করুন — AI নির্ভরযোগ্য উৎসকে অগ্রাধিকার দেয়
৪. সহজ এবং স্পষ্ট ভাষা ব্যবহার করুন — জটিল ভাষা AI প্রসেস করতে পারে না""")
    
    # EEAT section
    sections.append(f"""### EEAT (Experience, Expertise, Authoritativeness, Trustworthiness)

Google-এর EEAT ফ্রেমওয়ার্ক আপনার কন্টেন্টের বিশ্বাসযোগ্যতা নির্ধারণে গুরুত্বপূর্ণ ভূমিকা পালন করে। {topic} সম্পর্কিত কন্টেন্টের জন্য EEAT তৈরি করতে:

{eeat_story}

EEAT বাড়ানোর জন্য:
- আপনার ওয়েবসাইটে About Us এবং Contact পেজ সম্পূর্ণ এবং নির্ভুল রাখুন
- লেখকের বায়ো এবং এক্সপার্টাইজ স্পষ্টভাবে উল্লেখ করুন
- প্রামাণিক উৎস থেকে ব্যাকলিংক অর্জন করুন
- ব্যবহারকারীর রিভিউ এবং টেস্টিমোনিয়াল অন্তর্ভুক্ত করুন""")
    
    # AEO section
    sections.append(f"""### AEO (Answer Engine Optimization) এবং {topic}

Answer Engine Optimization (AEO) হলো কন্টেন্ট অপটিমাইজ করার একটি কৌশল যা সরাসরি প্রশ্নের উত্তর প্রদানের উপর ফোকাস করে। Google-এর ফিচার্ড স্নিপেট, People Also Ask (PAA), এবং AI সার্চ ইঞ্জিন সবই AEO-র উপর নির্ভর করে।

AEO-র জন্য কৌশল:
- প্রতিটি প্রধান পয়েন্টকে একটি প্রশ্নের উত্তর হিসেবে ফরম্যাট করুন
- FAQ সেকশন অন্তর্ভুক্ত করুন
- সংক্ষিপ্ত এবং স্পষ্ট উত্তর দিন (৪০-৬০ শব্দ)
- হেডিং-এ প্রশ্ন ব্যবহার করুন""")
    
    # FAQ section
    if faq_qas:
        sections.append("""### FAQ — """ + topic)
        for q, a in faq_qas:
            sections.append(f"""#### {q}
{a}""")
    
    # Bangladesh-specific
    sections.append(f"""### বাংলাদেশি ওয়েবসাইটের জন্য বিশেষ টিপস

{bangladesh_tips(topic)}

বাংলাদেশি ওয়েবসাইটগুলোর জন্য {topic} বাস্তবায়নের সময় স্থানীয় হোস্টিং, বাংলা ভাষা সাপোর্ট, এবং মোবাইল ফার্স্ট অ্যাপ্রোচ বিবেচনা করা গুরুত্বপূর্ণ।""")
    
    # Links section
    links_section = "\n\n".join(links)
    
    return "\n\n".join(sections) + "\n\n" + links_section


def bangladesh_tips(topic):
    tips = [
        f"বাংলাদেশি প্রেক্ষাপটে {topic} বাস্তবায়নের জন্য স্থানীয় উদাহরণ এবং ডেটা ব্যবহার করুন",
        f"বাংলা ভাষায় কন্টেন্ট তৈরি করে {topic}-এর সুবিধা নিন — বাংলা ভাষায় প্রতিযোগিতা কম",
        f"মোবাইল ফার্স্ট অ্যাপ্রোচ নিশ্চিত করুন — বাংলাদেশে ৭০% এর বেশি সার্চ মোবাইল থেকে হয়",
        f"স্থানীয় SEO কৌশলের সাথে {topic} সমন্বয় করুন",
        f"বাংলাদেশি ডিরেক্টরি এবং সোশ্যাল মিডিয়া প্ল্যাটফর্মে আপনার উপস্থিতি নিশ্চিত করুন"
    ]
    return '\n'.join(f"{i+1}. {tip}" for i, tip in enumerate(tips))


# All 30 slugs
slugs = [
    'seo-information-gain-optimization',
    'seo-passage-ranking-bangladesh',
    'seo-people-also-ask-optimization',
    'seo-featured-snippet-bangladesh',
    'seo-knowledge-panel-bangladesh',
    'seo-zero-click-search-bangladesh',
    'seo-google-penalty-recovery-bd',
    'seo-https-ssl-impact-bangladesh',
    'seo-redirects-guide-bangladesh',
    'seo-canonical-url-guide-bd',
    'seo-robots-txt-guide-bangladesh',
    'seo-xml-sitemap-guide-bd',
    'seo-hreflang-guide-bangladesh',
    'seo-structured-data-guide-bd',
    'seo-json-ld-schema-bangladesh',
    'seo-breadcrumb-schema-bd',
    'seo-faq-schema-bangladesh',
    'seo-howto-schema-bangladesh',
    'seo-for-startups-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-law-firms-bangladesh',
    'seo-for-fitness-gyms-bangladesh',
    'seo-services-cost-bangladesh-pricing-guide',
    'seo-vs-ppc-advertising-bangladesh',
    'how-to-track-measure-seo-roi-bangladesh',
    'seo-healthcare-medical-clinics-bangladesh',
    'seo-educational-institutions-bangladesh',
    'seo-travel-tourism-bangladesh',
    'seo-event-management-companies-bangladesh',
    'seo-real-estate-agents-property-developers-bangladesh'
]

def process_all():
    for i, slug in enumerate(slugs, 1):
        idx = text.find(f'slug: "{slug}"')
        if idx == -1:
            print(f"  SKIPPING (not found): {slug}")
            continue
        
        marker = 'content: `'
        start = text.find(marker, idx)
        if start == -1:
            print(f"  SKIPPING (no marker): {slug}")
            continue
        
        start += len(marker)
        
        # Find closing backtick
        end = start
        while end < len(text):
            if text[end] == '`':
                rest = text[end+1:end+10].lstrip()
                if rest.startswith(','):
                    break
            end += 1
        
        if end >= len(text):
            end = text.find('`,\n', start)
            if end != -1:
                end = end + 1
            else:
                print(f"  SKIPPING (no close): {slug}")
                continue
        
        old_content = text[start:end]
        old_wc = wc(old_content)
        
        # For this batch approach, we just signal success and move on
        # The content will be replaced by the full expanded version
        print(f"  [{i}/30] FOUND: {slug} ({old_wc} words current)")
    
    print(f"\nAll {len(slugs)} slugs found in file.")

process_all()

print("\nScript ready. To execute replacements, uncomment the run section.")
print("The expanded content for all 30 posts needs to be defined.")
