#!/bin/bash

BASE_URL="https://kanokmiah.com.bd/blog"

declare -a SLUGS=(
  "complete-seo-guide-bangladesh-businesses-2026"
  "local-seo-tips-dhaka-businesses-google-maps"
  "why-ecommerce-store-needs-seo-bangladesh"
  "technical-seo-checklist-bangladeshi-websites"
  "how-to-choose-right-seo-agency-bangladesh"
)

echo "+------------------------------------------------+------+-----------+------+-----------+--------------+"
echo "| Post                                            | **   | [text](  |  ---  | Raw ##    | FAQ raw txt  |"
echo "+------------------------------------------------+------+-----------+------+-----------+--------------+"

for slug in "${SLUGS[@]}"; do
  URL="$BASE_URL/$slug"
  
  # Fetch page, follow redirects, capture both body and HTTP code
  RESPONSE=$(curl -sL -o /tmp/page_check.html -w "%{http_code}" "$URL" --max-time 15)
  HTTP_CODE="$RESPONSE"
  
  if [ "$HTTP_CODE" != "200" ]; then
    printf "| %-46s | %-4s | %-9s | %-4s | %-9s | %-12s |\n" "$slug" "ERR" "ERR" "ERR" "ERR" "ERR"
    continue
  fi
  
  HTML=$(cat /tmp/page_check.html)
  
  # 1. Count raw **bold** markers - look for ** that aren't inside <script>/<style>
  # Count occurrences of ** in the visible text
  BOLD_COUNT=$(echo "$HTML" | grep -oP '\*\*' | wc -l)
  
  # 2. Count raw [text](url) markdown links
  LINK_COUNT=$(echo "$HTML" | grep -oP '\[.*?\]\(' | wc -l)
  
  # 3. Count raw --- (horizontal rules not rendered)
  # Look for three dashes on their own line or in paragraph text
  HR_COUNT=$(echo "$HTML" | grep -oP '(?<![>-])---(?![>-])' | wc -l)
  
  # 4. Check headings for raw ## or ###
  HEADING_RAW=$(echo "$HTML" | grep -oP '(?:^|>)(#{1,6}\s)' | wc -l)
  
  # 5. Check FAQ section for raw schema.org or ld+json visible as text
  # Check if ld+json exists properly in script tags vs visible as raw text
  # Look for schema.org text outside of <script> context
  FAQ_RAW=$(echo "$HTML" | grep -oP 'schema\.org|ld\+json|application/ld\+json' | wc -l)
  
  # Count how many of those occurrences are inside proper <script> tags vs visible text
  # Let's also specifically look for raw FAQ content
  FAQ_VISIBLE=$(echo "$HTML" | grep -oP '(?i)faq|frequently asked|accordion' | wc -l)
  
  # Better: extract visible text (roughly) and check for schema text
  # Remove script and style blocks then check
  VISIBLE_TEXT=$(echo "$HTML" | sed 's/<script[^>]*>.*<\/script>//g' | sed 's/<style[^>]*>.*<\/style>//g' | sed 's/<[^>]*>//g' | tr -s ' \n' ' ')
  SCHEMA_IN_VISIBLE=$(echo "$VISIBLE_TEXT" | grep -oP 'schema\.org|ld\+json|application/ld\+json' | wc -l)
  
  printf "| %-46s | %-4s | %-9s | %-4s | %-9s | %-12s |\n" "$slug" "$BOLD_COUNT" "$LINK_COUNT" "$HR_COUNT" "$HEADING_RAW" "$SCHEMA_IN_VISIBLE"
done

echo "+------------------------------------------------+------+-----------+------+-----------+--------------+"
