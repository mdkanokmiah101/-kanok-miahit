#!/bin/bash
FILE="/root/kanok-miahit/src/app/blog/data.js"

echo "============================================"
echo " CHECK A: PRIMARY KEYWORD COUNTS "
echo "============================================"

echo "P1: complete-seo-guide"
sed -n '14,158p' "$FILE" | grep -coi 'SEO guide\|Bangladesh.*SEO\|Bangladesh.*business.*SEO'

echo "P2: local-seo-tips"
sed -n '169,320p' "$FILE" | grep -coi 'local seo\|local.*SEO\|Google Maps\|Dominate Google'

echo "P3: why-ecommerce"
sed -n '331,463p' "$FILE" | grep -coi 'ecommerce.*seo\|e-commerce.*SEO\|SEO for\|Daraz.*SEO\|Shopify.*SEO'

echo "P4: technical-seo"
sed -n '474,626p' "$FILE" | grep -coi 'technical seo\|Technical SEO\|Core Web Vitals\|site structure\|crawlability'

echo "P5: how-to-choose-agency"
sed -n '637,803p' "$FILE" | grep -coi 'SEO agency\|agency.*SEO\|choose.*agency\|red flag'

echo "P6: link-building"
sed -n '814,1022p' "$FILE" | grep -coi 'link building\|backlink\|Link Building\|guest post'

echo "P7: geo-optimization"
sed -n '1033,1205p' "$FILE" | grep -coi 'GEO\|Generative Engine\|AI search\|AI-powered'

echo "P8: garments-textile"
sed -n '1216,1453p' "$FILE" | grep -coi 'garment.*SEO\|textile.*SEO\|RMG\|B2B.*lead\|export.*SEO'

echo "P9: google-business-profile"
sed -n '1464,1718p' "$FILE" | grep -coi 'Google Business Profile\|GBP\|local pack\|Google Maps.*optim'

echo "P10: seo-vs-ads"
sed -n '1729,2002p' "$FILE" | grep -coi 'SEO vs\|Google Ads\|PPC\|paid.*advertising\|cost.*SEO.*Ads'

echo "P11: real-estate"
sed -n '2013,2261p' "$FILE" | grep -coi 'real estate.*SEO\|property.*SEO\|developer.*lead\|property search.*SEO'

echo "P12: mobile-seo"
sed -n '2272,2481p' "$FILE" | grep -coi 'mobile seo\|mobile.*optimiz\|mobile-first\|voice search\|smartphone.*SEO'

echo "P13: content-marketing"
sed -n '2492,2663p' "$FILE" | grep -coi 'content marketing\|content.*strategy\|blog.*SEO\|storytelling.*SEO'

echo "P14: international-seo"
sed -n '2674,2828p' "$FILE" | grep -coi 'international seo\|global.*SEO\|hreflang\|multilingual\|export.*SEO\|buyer.*SEO'

echo ""
echo "============================================"
echo " CHECK B: ENTITY CHECK (Dhaka/Bangladesh) "
echo "============================================"
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
  case $i in
    1) L1=14; L2=158 ;; 2) L1=169; L2=320 ;; 3) L1=331; L2=463 ;; 4) L1=474; L2=626 ;;
    5) L1=637; L2=803 ;; 6) L1=814; L2=1022 ;; 7) L1=1033; L2=1205 ;; 8) L1=1216; L2=1453 ;;
    9) L1=1464; L2=1718 ;; 10) L1=1729; L2=2002 ;; 11) L1=2013; L2=2261 ;; 12) L1=2272; L2=2481 ;;
    13) L1=2492; L2=2663 ;; 14) L1=2674; L2=2828 ;;
  esac
  DH=$(sed -n "${L1},${L2}p" "$FILE" | grep -co 'Dhaka')
  BD=$(sed -n "${L1},${L2}p" "$FILE" | grep -co 'Bangladesh\|Bangladeshi')
  echo "P${i}: Dhaka=${DH}, BD=${BD}"
done

echo ""
echo "============================================"
echo " CHECK C: INTERNAL LINKS "
echo "============================================"
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
  case $i in
    1) L1=14; L2=158 ;; 2) L1=169; L2=320 ;; 3) L1=331; L2=463 ;; 4) L1=474; L2=626 ;;
    5) L1=637; L2=803 ;; 6) L1=814; L2=1022 ;; 7) L1=1033; L2=1205 ;; 8) L1=1216; L2=1453 ;;
    9) L1=1464; L2=1718 ;; 10) L1=1729; L2=2002 ;; 11) L1=2013; L2=2261 ;; 12) L1=2272; L2=2481 ;;
    13) L1=2492; L2=2663 ;; 14) L1=2674; L2=2828 ;;
  esac
  BLOG=$(sed -n "${L1},${L2}p" "$FILE" | grep -co '/blog/')
  SVC=$(sed -n "${L1},${L2}p" "$FILE" | grep -co '/services/')
  echo "P${i}: /blog/=${BLOG}, /services/=${SVC}"
done

echo ""
echo "============================================"
echo " CHECK D: QUESTION MARKS IN HEADINGS "
echo "============================================"
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
  case $i in
    1) L1=14; L2=158 ;; 2) L1=169; L2=320 ;; 3) L1=331; L2=463 ;; 4) L1=474; L2=626 ;;
    5) L1=637; L2=803 ;; 6) L1=814; L2=1022 ;; 7) L1=1033; L2=1205 ;; 8) L1=1216; L2=1453 ;;
    9) L1=1464; L2=1718 ;; 10) L1=1729; L2=2002 ;; 11) L1=2013; L2=2261 ;; 12) L1=2272; L2=2481 ;;
    13) L1=2492; L2=2663 ;; 14) L1=2674; L2=2828 ;;
  esac
  Q=$(sed -n "${L1},${L2}p" "$FILE" | grep -c '##.*?')
  echo "P${i}: headings_with_?=${Q}"
done

echo ""
echo "============================================"
echo " CHECK E: MARKDOWN LINK COUNT [/ "
echo "============================================"
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
  case $i in
    1) L1=14; L2=158 ;; 2) L1=169; L2=320 ;; 3) L1=331; L2=463 ;; 4) L1=474; L2=626 ;;
    5) L1=637; L2=803 ;; 6) L1=814; L2=1022 ;; 7) L1=1033; L2=1205 ;; 8) L1=1216; L2=1453 ;;
    9) L1=1464; L2=1718 ;; 10) L1=1729; L2=2002 ;; 11) L1=2013; L2=2261 ;; 12) L1=2272; L2=2481 ;;
    13) L1=2492; L2=2663 ;; 14) L1=2674; L2=2828 ;;
  esac
  L=$(sed -n "${L1},${L2}p" "$FILE" | grep -co '\[')
  echo "P${i}: [ links = ${L}"
done

echo ""
echo "============================================"
echo " CHECK F: METADATA SET "
echo "============================================"
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
  case $i in
    1) L1=2; L2=12 ;; 2) L1=160; L2=168 ;; 3) L1=322; L2=330 ;; 4) L1=465; L2=473 ;;
    5) L1=628; L2=636 ;; 6) L1=805; L2=813 ;; 7) L1=1024; L2=1032 ;; 8) L1=1207; L2=1215 ;;
    9) L1=1455; L2=1463 ;; 10) L1=1720; L2=1728 ;; 11) L1=2004; L2=2012 ;; 12) L1=2263; L2=2271 ;;
    13) L1=2483; L2=2491 ;; 14) L1=2665; L2=2673 ;;
  esac
  TITLE=$(sed -n "${L1},${L2}p" "$FILE" | grep -c 'title:')
  D=$(sed -n "${L1},${L2}p" "$FILE" | grep -c 'date:')
  A=$(sed -n "${L1},${L2}p" "$FILE" | grep -c 'author:')
  E=$(sed -n "${L1},${L2}p" "$FILE" | grep -c 'excerpt:')
  echo "P${i}: title=${TITLE} date=${D} author=${A} excerpt=${E}"
done
