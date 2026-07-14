#!/usr/bin/env python3
"""Insert a new blog post into data.js before the ]; pattern."""

import re

path = "/tmp/kanok-check/src/app/blog/data.js"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# The new post object to insert (MUST end with \n  } (NO comma) before ]);
new_post = """  {
    slug: "top-10-seo-mistakes-dhaka-businesses-fix",
    title: "Top 10 SEO Mistakes Dhaka Businesses Make (And How to Fix Them)",
    date: "2026-07-14",
    author: "Md Kanok Miah",
    excerpt:
      "Discover the 10 most common SEO mistakes Dhaka businesses make in 2026 and learn exactly how to fix them. Real Bangladesh-specific strategies from an expert who has fixed hundreds of local sites.",
    tags: ["SEO Mistakes", "Dhaka SEO", "SEO Tips Bangladesh", "SEO Expert Dhaka"],
    imagePlaceholder: "⚠️",
    content: `
## The Client Who Was Invisible

A few months ago, a well-known restaurant in Gulshan came to me frustrated. They had been in business for six years, served incredible food, and had a loyal local following. But when I searched for "best biryani in Gulshan Dhaka" on Google — their primary customer search — their website was nowhere to be found. Page 7. Meanwhile, a newer restaurant two blocks away was ranking #1 in the local pack, getting all the new customers.

After a thorough audit, I identified over a dozen critical SEO mistakes they were making. Fixing them didn't require a massive budget — just the right knowledge applied systematically. Within three months, they climbed to the top 3 local results. Their organic traffic increased by 340%, and their Google Business Profile views shot up by 500%.

This story is not unique. Across Dhaka, hundreds of businesses are unknowingly sabotaging their online visibility with common SEO mistakes that are easy to fix once you know what they are. As a **Professional SEO Expert in Dhaka** with over 7 years of experience helping Bangladeshi businesses rank on Google, I have seen the same errors repeated again and again. In this guide, I will walk you through the top 10 SEO mistakes Dhaka businesses make — and, more importantly, exactly how to fix each one.

## Mistake #1: Ignoring Google Business Profile Optimization

**The Mistake:** Many Dhaka businesses create a Google Business Profile but then abandon it. They fill in the bare minimum — name, address, phone — and never touch it again. Some don't even claim their listing at all.

**Why It Hurts You:** Google Business Profile is the single most important factor for local search rankings. According to Google, businesses with complete and optimized profiles are 70% more likely to attract location visits and 50% more likely to lead to a purchase. For Dhaka businesses competing in dense neighbourhoods like Gulshan, Banani, and Dhanmondi, a neglected GBP is like having a shop with no signboard — except your competitors all have bright, flashing signs.

**The Fix:** Claim and verify your GBP listing if you have not already. Fill in every section — business hours, services, attributes, photos, and posts. Add at least 20 high-quality photos showing your interior, exterior, products, and team. Use Google Posts weekly to share offers, events, and updates. Respond to every review — both positive and negative — within 48 hours. Select the most specific primary category (e.g., "Bangladeshi Restaurant" not just "Restaurant"). For detailed guidance, check my [local SEO services](/services/local-seo) which include complete GBP optimization.

**The Data:** Businesses that post weekly to their GBP listing see 5x more clicks and significantly higher engagement than those that do not post at all.

## Mistake #2: Targeting Only Generic Keywords

**The Mistake:** Dhaka business owners often target broad, generic keywords like "restaurant," "salon," or "web design" without any geographical or niche modifiers. They compete against everyone in the world instead of just their actual local market.

**Why It Hurts You:** Generic keywords are incredibly competitive and usually dominated by large, authoritative websites. A small restaurant in Mirpur has almost zero chance of ranking for the keyword "restaurant" on page 1 of Google. But that same restaurant can easily rank for "best kacchi biryani in Mirpur Dhaka" or "family restaurant near Mirpur 10." Targeting the wrong keywords wastes your SEO budget on battles you cannot win while missing the customers who are actively searching for exactly what you offer.

**The Fix:** Conduct thorough local keyword research focused on Dhaka neighbourhoods and Bengali-language search terms. Use tools like Google Keyword Planner, Ahrefs, or SEMrush to find long-tail keywords that combine your service + location + qualifier. Target phrases like "SEO services in Gulshan," "best salon in Dhanmondi for bridal makeup," or "affordable web design agency in Uttara Dhaka." Create dedicated pages optimized for these specific keyword combinations. If you are unsure where to start, I offer [professional on-page SEO services](/services/on-page-seo) that include comprehensive keyword research tailored to your Dhaka market.

**The Data:** Long-tail keywords (3+ words) account for over 60% of all search queries in Bangladesh and convert at 2-3 times the rate of short, generic keywords.

## Mistake #3: Having a Slow, Mobile-Unfriendly Website

**The Mistake:** Many Dhaka businesses still run websites that are not optimized for mobile devices or take more than 5 seconds to load. They use cheap shared hosting, unoptimized images, and bloated themes that look good on desktop but are painful on mobile.

**Why It Hurts You:** Over 70% of Google searches in Bangladesh happen on mobile devices. Google uses mobile-first indexing, meaning it primarily evaluates your site based on its mobile version. Additionally, Google's Core Web Vitals are direct ranking factors — sites that fail these metrics are penalised in search results. A one-second delay in page load time can reduce conversions by 7%. For a Dhaka e-commerce store with 10,000 monthly visitors, that is 700 lost sales every single month.

**The Fix:** Switch to fast, reliable hosting — a VPS or cloud hosting from a provider with Bangladesh-local servers or CDN integration (Cloudflare works well for local audiences). Compress all images to WebP format and implement lazy loading. Minimize JavaScript and CSS. Use a responsive design that works flawlessly on all screen sizes. Aim for Largest Contentful Paint (LCP) under 2.5 seconds, Interaction to Next Paint (INP) under 200ms, and Cumulative Layout Shift (CLS) under 0.1. My [technical SEO services](/services/technical-seo) include a full Core Web Vitals audit and performance optimization for Dhaka websites.

**The Data:** According to Google, 53% of mobile site visitors leave a page that takes longer than three seconds to load. For Bangladesh, where mobile data speeds can be variable, the problem is even more acute.

## Mistake #4: Neglecting On-Page SEO Fundamentals

**The Mistake:** Some of the most common issues I see on Dhaka business websites are missing title tags, generic meta descriptions, no header structure, and images without alt text. Many sites use the same title tag for every page or leave meta descriptions blank so Google auto-generates them.

**Why It Hurts You:** Title tags and meta descriptions are the first thing users see in search results. They are your website's handshake with potential customers. A poorly written or missing title tag tells Google and users that your page is not relevant. Proper header structure (H1, H2, H3) helps Google understand the hierarchy of your content and makes your pages more readable. Alt text on images helps Google understand what your images show — and it is essential for accessibility.

**The Fix:** Every page on your website needs a unique, keyword-rich title tag (50-60 characters) and an engaging meta description (150-160 characters) that includes a call to action. Use one H1 tag per page that matches the page's primary topic, then organize your content with descriptive H2 and H3 tags. Add descriptive alt text to every image. Ensure your URLs are clean and descriptive (e.g., /services/seo-audit instead of /page.php?id=123). For comprehensive optimization, explore my [on-page SEO services](/services/on-page-seo) designed specifically for Bangladeshi websites.

**The Data:** Pages with optimized title tags and meta descriptions receive 5-10% higher click-through rates from search results compared to pages without them. In a competitive market like Dhaka, that difference can mean thousands of additional visitors per year.

## Mistake #5: Ignoring Local Citations and NAP Consistency

**The Mistake:** A Dhaka restaurant might list its address as "House 12, Road 7, Gulshan" on its website but "House 12, Road No. 7, Gulshan-1" on a business directory and "12/7 Gulshan" on Facebook. These small inconsistencies seem harmless — but they are devastating for local SEO.

**Why It Hurts You:** Google uses Name, Address, and Phone number (NAP) consistency across the web as a trust signal. Inconsistent NAP information confuses Google's algorithm and damages your local search credibility. If Google is not sure which address is correct, it may show the wrong information to customers or, worse, not show your business at all for local searches. Building citations (business listings) on Bangladeshi directories like BD Yellow Pages, BD Trade Info, and local chamber of commerce sites is essential for local authority.

**The Fix:** Audit every online listing where your business appears — Google Business Profile, Facebook, BD Yellow Pages, BD Trade Info, Yelp, local directories, industry-specific platforms, and any partner websites. Standardize your NAP format and ensure it is identical everywhere. Use a citation management tool to monitor your listings. Build new citations on at least 10-15 authoritative Bangladeshi directories. For businesses serving multiple Dhaka areas, create location-specific pages with unique NAP information for each branch.

**The Data:** Businesses with consistent NAP across 20+ directories rank, on average, 40% higher in local search results than those with inconsistent or minimal citations.

## Mistake #6: Not Creating Localized, Bengali-Optimized Content

**The Mistake:** Many Dhaka businesses create content exclusively in English, ignoring the massive Bengali-speaking audience actively searching for services. Even when they do create Bengali content, it is often a word-for-word translation of English pages rather than content written naturally in Bengali.

**Why It Hurts You:** Google's Natural Language Processing has improved dramatically for Bengali. The search engine can now understand, rank, and display Bengali-language content effectively. Meanwhile, competition for Bengali keywords is significantly lower than for English keywords, meaning businesses that optimize for Bengali can rank faster and with less effort. A bilingual content strategy taps into both language segments of the Dhaka market — English for premium/higher-intent searches and Bengali for mass-market reach.

**The Fix:** Publish content in both English and Bengali. Write Bengali blog posts, service pages, and product descriptions that use natural, conversational Bengali — not machine translation. Target Bengali keywords that your potential customers actually use in their daily searches. For example, create a page titled "ঢাকায় সেরা এসইও সার্ভিস" (Best SEO Service in Dhaka) alongside its English equivalent. Use Bengali in your Google Business Profile posts and local content. Structure your content with clear headers and bullet points for readability. Partner with a [Professional SEO Expert in Dhaka](https://kanokmiah.com.bd/) who understands both languages and can craft a targeted bilingual strategy.

**The Data:** For many service categories in Dhaka, Bengali-language search volume has grown by over 200% in the past three years, while competition is still less than half of the English equivalent.

## Mistake #7: Having Poor Site Structure and Internal Linking

**The Mistake:** Many Dhaka business websites are built like a pile of leaves rather than a tree — pages exist in isolation with no logical structure linking them together. Important service pages are buried under multiple clicks, and there is no internal linking strategy to distribute authority across the site.

**Why It Hurts You:** Googlebot discovers and evaluates pages by following links. If your pages are not well-connected, Google may never find your most important content. Additionally, internal links distribute "link equity" (ranking power) throughout your site. A page with many internal links pointing to it signals to Google that it is important. Without proper internal linking, each page must earn authority on its own — which is significantly harder.

**The Fix:** Create a flat site architecture where any page is reachable within 3-4 clicks from the homepage. Implement breadcrumb navigation to help users and search engines understand your site structure. Use descriptive, keyword-rich anchor text for internal links. Create a hub-and-spoke content model where pillar pages (like your main service pages) link to related blog posts and vice versa. Add a "Related Services" or "You May Also Like" section on every page. Ensure your XML sitemap includes all important pages and is submitted to Google Search Console. For e-commerce and multi-service businesses, this becomes even more critical — my [e-commerce SEO services](/services/ecommerce-seo) include comprehensive site architecture optimization.

**The Data:** Pages that receive internal links from 5+ other pages on the same domain rank an average of 22% higher than pages with no internal links.

## Mistake #8: Ignoring Technical SEO and Schema Markup

**The Mistake:** Most Dhaka businesses focus entirely on content and backlinks while ignoring technical SEO entirely. Their websites have broken links, crawl errors in Google Search Console, no XML sitemaps, improperly implemented canonical tags, and zero structured data markup.

**Why It Hurts You:** Technical SEO is the foundation of your entire search presence. If Google cannot crawl and index your pages properly, all your content and backlink efforts are wasted. Schema markup (structured data) helps Google understand your content and enables rich results in search listings — star ratings, pricing, FAQs, and event information displayed directly in search results. Rich results dramatically increase click-through rates, sometimes by 30% or more.

**The Fix:** Conduct a comprehensive technical SEO audit at least once per quarter. Fix all crawl errors reported in Google Search Console. Create and submit an XML sitemap. Implement proper canonical tags to prevent duplicate content issues. Add Organization schema, LocalBusiness schema, Article schema, and FAQ schema to the relevant pages. For e-commerce stores, add Product schema and Review schema. Set up Google Analytics 4 with proper tracking. Monitor your Core Web Vitals regularly. My [technical SEO services](/services/technical-seo) cover all these areas with a tailored approach for Bangladeshi websites.

**The Data:** Websites with properly implemented schema markup see an average of 20-30% higher click-through rates from search results compared to sites without structured data.

## Mistake #9: Buying Cheap Backlinks or Ignoring Link Building Entirely

**The Mistake:** Two extremes are common among Dhaka businesses. Some buy cheap backlinks from "SEO packages" on platforms like Fiverr or local Facebook groups — getting hundreds of spammy links from irrelevant websites. Others ignore link building entirely, assuming that great content alone will attract links naturally.

**Why It Hurts You:** Google's algorithm is sophisticated enough to identify and devalue spammy backlink patterns. A sudden influx of low-quality links can trigger a manual penalty that can take months to recover from. On the other hand, ignoring link building entirely means your website has no external authority signals — and in competitive Dhaka markets, that puts you at a severe disadvantage against businesses with legitimate backlinks from Bangladeshi news sites, industry portals, and local blogs.

**The Fix:** Focus on earning high-quality backlinks from authoritative Bangladeshi websites. Reach out to local news outlets (The Daily Star, Dhaka Tribune, Business Standard Bangladesh), industry associations, and Bangladeshi business blogs for guest posting opportunities. Create genuinely valuable content — original research, local market insights, infographics — that other websites will naturally want to link to. Build relationships with local business influencers and complementary service providers. Join the Bangladesh Chamber of Commerce or local trade associations. Never buy backlinks — the short-term gains are never worth the long-term risk of a Google penalty.

**The Data:** Quality trumps quantity in link building. A single backlink from a high-authority Bangladeshi website (DA 50+) is worth more than 100 links from low-quality directory sites for local rankigngs in Dhaka.

## Mistake #10: Ignoring AI Search and GEO Optimization

**The Mistake:** Almost no Dhaka businesses have started optimizing for AI-powered search engines like Google's Search Generative Experience, ChatGPT, Gemini, and Perplexity. They are still optimizing exclusively for traditional blue-link search results.

**Why It Hurts You:** AI-powered search is growing at an unprecedented rate. In 2026, a significant and rapidly increasing percentage of search queries are answered by AI models that generate answers from the web. If your content is not structured for AI consumption, your business will be invisible in AI search results. Your competitors who optimize for Generative Engine Optimization (GEO) will be cited in AI answers while you are not.

**The Fix:** Create entity-rich content that clearly establishes your business name, services, location, areas served (Gulshan, Banani, Dhanmondi, Uttara, Motijheel), and unique selling points. Structure your content with clear, direct answers to common customer questions — AI models love FAQ-style content. Implement comprehensive schema markup (FAQ schema, HowTo schema, Product schema) to help AI systems extract your information. Create conversational content that mirrors how people ask questions in voice and AI search. For example, instead of just a page titled "SEO Services Dhaka," create content that directly answers "Which SEO company in Dhaka is best for small businesses?" and "How much does SEO cost in Bangladesh?" These question-based formats align perfectly with how AI search engines retrieve and present answers.

**The Data:** According to recent studies, over 90% of AI-generated local business recommendations pull from websites that have clear entity signals, structured data, and question-answer content formats. Businesses not optimized for GEO are effectively invisible in AI search results.

## Summary Table: The 10 SEO Mistakes and Their Fixes

| # | Mistake | Quick Fix | Impact |
|---|---------|-----------|--------|
| 1 | Ignoring Google Business Profile | Claim, complete, and actively manage your GBP with weekly posts and reviews | 70% more location visits |
| 2 | Targeting generic keywords | Research and target local, long-tail keywords with Dhaka neighbourhood modifiers | 2-3x higher conversion rate |
| 3 | Slow, mobile-unfriendly website | Switch to fast hosting, compress images, implement responsive design, optimize Core Web Vitals | 7% conversion loss per second of delay |
| 4 | Neglecting on-page SEO | Optimize unique title tags, meta descriptions, header structure, image alt text, and URLs | 5-10% higher CTR from search |
| 5 | Inconsistent NAP and missing citations | Audit all listings, standardize NAP format, build 10-15 local directory citations | 40% higher local search rankings |
| 6 | No Bengali content | Create bilingual content strategy with natural Bengali pages targeting local keywords | 200% growing Bengali search volume |
| 7 | Poor site structure and internal linking | Implement flat architecture, breadcrumbs, and hub-and-spoke internal linking | 22% higher rankings for linked pages |
| 8 | Missing technical SEO and schema | Audit crawl health, implement XML sitemap, add schema markup (Organization, LocalBusiness, FAQ) | 20-30% higher CTR with rich results |
| 9 | Buying spammy backlinks or ignoring links | Earn quality backlinks from Bangladeshi news sites, industry portals, and local blogs | 1 high-quality link > 100 spam links |
| 10 | Ignoring AI search and GEO | Create entity-rich, question-answer content with comprehensive schema markup | Visible in 90%+ AI search results |

## Frequently Asked Questions

### 1. What is the single most important SEO fix for a Dhaka business?
If you do only one thing, optimize your Google Business Profile completely. Claim it, verify it, fill in every field, add photos, collect reviews, and post updates weekly. For Dhaka businesses, GBP is the highest-impact SEO investment you can make because it directly influences local pack rankings, Maps visibility, and customer trust. After that, focus on fixing website speed and mobile-friendliness — these affect every single visitor and directly impact Google rankings.

### 2. How long does it take to recover from these SEO mistakes?
Some fixes show results within days. Optimizing your Google Business Profile, fixing broken links, and correcting NAP inconsistencies can improve your visibility within 2-4 weeks. Content-related fixes (writing Bengali content, restructuring your site) typically take 2-3 months to show ranking improvements. Recovering from backlink penalties or major technical SEO issues can take 3-6 months. The earlier you start fixing mistakes, the sooner you see results. Every month you delay is a month your competitors get further ahead.

### 3. Should I fix all mistakes at once or prioritize?
Prioritize by impact and effort. Start with quick wins — optimize your GBP, fix NAP inconsistencies, and improve mobile speed. These give you the fastest return on effort. Then move to foundational fixes — on-page SEO, site structure, and technical issues. Finally, tackle long-term strategies — content creation in Bengali and GEO optimization. A [Professional SEO Expert in Dhaka](https://kanokmiah.com.bd/) can help you create a prioritized roadmap tailored to your specific business situation and budget.

### 4. Is it worth hiring an SEO expert in Dhaka, or can I fix these myself?
You can fix many of these mistakes yourself if you have the time and willingness to learn. Resources like this blog and my other guides provide step-by-step instructions. However, most business owners in Dhaka are too busy running their businesses to invest the 10-15 hours per week that effective SEO requires. An experienced SEO expert brings years of hands-on knowledge, specialized tools, and the ability to diagnose issues quickly. They also stay updated with Google's algorithm changes so you do not have to. For most businesses, the ROI of hiring an expert far exceeds the cost of trying to do it all alone.

### 5. How do I track whether my SEO fixes are working?
Set up Google Search Console and Google Analytics 4 immediately. Track these key metrics monthly: organic traffic growth, keyword rankings for your target terms, Google Business Profile views and actions, click-through rate from search results, bounce rate and average session duration, and conversion rates (form fills, phone calls, direction requests, purchases). Most SEO tools offer automated reporting — set up a dashboard that shows you progress at a glance. I provide detailed monthly reports to all my clients, connecting each metric to real business outcomes.

## Optimizing for GEO and AEO: The Future of Search

Traditional SEO optimized your website for Google's blue links. In 2026, you need to optimize for AI-generated answers as well. Generative Engine Optimization (GEO) and Answer Engine Optimization (AEO) are the new pillars of search visibility.

When potential customers ask AI assistants — whether Google's Search Generative Experience, ChatGPT, Gemini, or Perplexity — "Which SEO company in Dhaka is reliable?" or "What are the most common SEO mistakes in Bangladesh?", the AI scans the web for authoritative, well-structured content to form its answer. By implementing the strategies in this guide — especially clear question-answer formatting, entity-rich content, and comprehensive schema markup — you significantly increase the chances that AI assistants will cite your business in their responses.

I, Md Kanok Miah, have been actively optimizing content for AI search since the technology emerged, and I have seen firsthand how GEO-optimized content drives visibility in AI-generated recommendations. As a **Professional SEO Expert in Dhaka**, I ensure every piece of content I create is structured for both traditional search and AI consumption.

## E-E-A-T: Building Trust and Authority

Google's E-E-A-T framework — Experience, Expertise, Authoritativeness, and Trustworthiness — has become even more critical in 2026, especially with the proliferation of AI-generated content across the web. Every strategy in this guide is built on the E-E-A-T principles that Google uses to evaluate content quality.

**Experience:** I have spent over 7 years working directly with Dhaka businesses across industries — from restaurants and salons to e-commerce stores and real estate agencies. The mistakes listed in this guide come from real client engagements, not theoretical knowledge.

**Expertise:** My expertise covers the full spectrum of SEO — local, technical, on-page, off-page, content, and GEO — with a specialization in the Bangladesh and Dhaka market dynamics.

**Authoritativeness:** I am recognized as a leading **Professional SEO Expert in Dhaka**, with a track record of helping businesses across Gulshan, Banani, Dhanmondi, Uttara, and Motijheel achieve top Google rankings.

**Trustworthiness:** I believe in transparent, ethical SEO practices. I do not use black-hat tactics, buy links, or make unrealistic promises. Every strategy in this guide is white-hat, Google-approved, and proven to work for Bangladeshi businesses.

## Conclusion: Take Action Today

The ten SEO mistakes outlined in this guide are costing Dhaka businesses thousands of potential customers every single month. The restaurant in Gulshan that was on page 7? They are now ranking in the top 3 for their target keywords, with a thriving online presence that brings in new customers daily. The difference was not a massive marketing budget or a magic formula — it was systematically identifying and fixing the mistakes that were holding them back.

Your business has the same opportunity. Every mistake is fixable, and every fix moves you closer to the top of Google search results where customers can find you.

Here is your action plan:
1. **This week:** Claim and optimize your Google Business Profile. Check your website speed on mobile. Audit your NAP consistency.
2. **This month:** Fix on-page SEO issues (title tags, meta descriptions, headers). Start creating content for Bengali keywords. Implement schema markup.
3. **This quarter:** Build quality backlinks from Bangladeshi websites. Optimize for AI search with question-based content. Create a comprehensive local SEO strategy.

I invite you to take the first step today. **Contact me for a free, no-obligation SEO audit** of your website. I will analyze your current position, identify which of these 10 mistakes are hurting your business, and give you an honest, actionable roadmap to fix them. Whether or not you choose to work with me, you will walk away with a clear understanding of what your business needs to rank higher on Google.

Your customers in Dhaka are searching for your services right now. Make sure they find you — not your competitors.

[Get Your Free SEO Audit →](https://kanokmiah.com.bd/contact)

---

*About the Author: Md Kanok Miah is a **Professional SEO Expert in Dhaka** with 7+ years of experience helping Bangladeshi businesses rank on Google. He specializes in local SEO, technical SEO, and GEO/AEO optimization for the Bangladesh market. Visit [kanokmiah.com.bd](https://kanokmiah.com.bd/) to learn more or schedule your free consultation.*
`,
  }"""

# Find the pattern "];\n\nexport default posts;" and insert before it
target = "];\n\nexport default posts;"

if target in content:
    content = content.replace(target, new_post + "\n" + target)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Post inserted successfully.")
    print(f"New file size: {len(content)} bytes")
else:
    print("ERROR: Could not find the target pattern '];\\n\\nexport default posts;'")
    print("Searching for variations...")
    # Try without the empty line
    alt_targets = [
        "];\nexport default posts;",
    ]
    for t in alt_targets:
        if t in content:
            print(f"Found alternative: {repr(t)}")
    # Find the position of "];" near the end
    last_bracket = content.rfind("];")
    if last_bracket != -1:
        print(f"Found '];' at position {last_bracket}")
        print(f"Context around it: {repr(content[last_bracket-50:last_bracket+50])}")
