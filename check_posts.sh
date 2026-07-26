#!/bin/bash

analyze_post() {
  local start=$1
  local end=$2
  local slug=$3
  local title_kw=$4
  local entity_check=$5  # "location:service:industry"
  
  echo "=== SLUG: $slug ==="
  
  # Extract content range
  local content=$(sed -n "${start},${end}p" /root/kanok-miahit/src/app/blog/data.js)
  
  # A. TF-IDF - count keyword
  local kw_count=$(echo "$content" | grep -oi "$title_kw" | wc -l)
  echo "TFIDF_COUNT:$kw_count"
  
  # B. Entities
  local has_bd=$(echo "$content" | grep -oi "বাংলাদেশ\|Bangladesh\|Dhaka\|ঢাকা" | wc -l)
  # Extract service from entity_check
  local service=$(echo "$entity_check" | cut -d: -f2)
  local industry=$(echo "$entity_check" | cut -d: -f3)
  local has_service=$(echo "$content" | grep -oi "$service" | wc -l)
  local has_industry=$(echo "$content" | grep -oi "$industry" | wc -l)
  echo "ENTITIES:bd:$has_bd:service:$service:$has_service:industry:$industry:$has_industry"
  
  # C. Tags from the post - extract tags array
  local tags=$(echo "$content" | grep -oP '"tags":\s*\[.*?\]' | head -1)
  echo "TAGS:$tags"
  
  # D. Pillar - count internal links to blog/services/locations
  local pillar_links=$(echo "$content" | grep -oP '/blog/|/services/|/locations/' | wc -l)
  echo "PILLAR_LINKS:$pillar_links"
  
  # E. AEO/GEO - count question headings
  local qheadings=$(echo "$content" | grep -cP '^### (কেন|কী|কখন|কোথায়|কীভাবে|কি|How|What|Why|When|Where|Can|Do|Is|Are)' 2>/dev/null)
  echo "QHEADINGS:$qheadings"
  
  # F. Internal Links - count ALL / links
  local all_links=$(echo "$content" | grep -oP '/[a-z][a-zA-Z0-9_/-]*' | sort -u | wc -l)
  echo "ALL_LINKS:$all_links"
  
  # G. Schema check
  local has_title=$(echo "$content" | grep -c '"title":')
  local has_excerpt=$(echo "$content" | grep -c '"excerpt":')
  local has_date=$(echo "$content" | grep -c '"date":')
  local has_datemod=$(echo "$content" | grep -c '"dateModified":')
  local has_metatitle=$(echo "$content" | grep -c '"metaTitle":')
  local has_metadesc=$(echo "$content" | grep -c '"metaDescription":')
  echo "SCHEMA:title:$has_title:excerpt:$has_excerpt:date:$has_date:dateModified:$has_datemod:metaTitle:$has_metatitle:metaDescription:$has_metadesc"
  
  echo "=== END:$slug ==="
}

# Post 1
analyze_post 15917 16227 "seo-google-penalty-recovery-bd" "গুগল পেনাল্টি" "বাংলাদেশ:পেনাল্টি রিকভারি:ওয়েবসাইট"

# Post 2  
analyze_post 16229 16463 "seo-https-ssl-impact-bangladesh" "HTTPS" "বাংলাদেশ:HTTPS:SSL"

# Post 3
analyze_post 16465 16797 "seo-redirects-guide-bangladesh" "রিডাইরেক্ট" "বাংলাদেশ:রিডাইরেক্ট:SEO"

# Post 4
analyze_post 16799 17093 "seo-canonical-url-guide-bd" "ক্যানোনিকাল" "বাংলাদেশ:ক্যানোনিকাল:SEO"

# Post 5
analyze_post 17095 17445 "seo-robots-txt-guide-bangladesh" "robots.txt" "বাংলাদেশ:robots.txt:SEO"

# Post 6
analyze_post 17447 17774 "seo-xml-sitemap-guide-bd" "সাইটম্যাপ" "বাংলাদেশ:সাইটম্যাপ:SEO"

# Post 7
analyze_post 17776 18061 "seo-hreflang-guide-bangladesh" "hreflang" "বাংলাদেশ:hreflang:SEO"

# Post 8
analyze_post 18063 18389 "seo-structured-data-guide-bd" "স্ট্রাকচারড ডাটা" "বাংলাদেশ:স্ট্রাকচারড ডাটা:Schema"

# Post 9
analyze_post 18391 18750 "seo-json-ld-schema-bangladesh" "JSON-LD" "বাংলাদেশ:JSON-LD:Schema"

# Post 10
analyze_post 18752 19028 "seo-breadcrumb-schema-bd" "ব্রেডক্রাম্ব" "বাংলাদেশ:ব্রেডক্রাম্ব:Schema"

# Post 11
analyze_post 19030 19371 "seo-faq-schema-bangladesh" "FAQ স্কিমা" "বাংলাদেশ:FAQ:Schema"

# Post 12
analyze_post 19373 19732 "seo-howto-schema-bangladesh" "HowTo স্কিমা" "বাংলাদেশ:HowTo:Schema"

# Post 13
analyze_post 19734 19902 "seo-for-startups-bangladesh" "startup" "Bangladesh:SEO:startup"

# Post 14
analyze_post 19904 20110 "b2b-lead-generation-seo-bangladesh" "B2B" "Bangladesh:SEO:B2B"

# Post 15
analyze_post 20112 20347 "seo-for-law-firms-bangladesh" "law firm" "Bangladesh:SEO:law"

# Post 16
analyze_post 20349 20571 "seo-for-fitness-gyms-bangladesh" "fitness" "Bangladesh:SEO:fitness"

# Post 17
analyze_post 24703 25101 "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh" "SEO expert" "Dhaka:SEO:Bangladesh"
