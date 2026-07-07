#!/bin/bash
cd /root/kanok-miahit

# Replace footers in all pages
for f in src/app/about/page.js src/app/terms-of-service/page.js src/app/privacy-policy/page.js src/app/industries/[slug]/page.js src/app/industries/page.js; do
  sed -i "s/— SEO Agency in Bangladesh/— SEO Expert in Bangladesh/g" "$f"
  echo "Fixed: $f"
done

# Blog pages have slightly different structure
sed -i "s/— SEO Agency in Bangladesh/— SEO Expert in Bangladesh/g" src/app/blog/page.js
sed -i "s/— SEO Agency in Bangladesh/— SEO Expert in Bangladesh/g" src/app/blog/\[slug\]/page.js
echo "Fixed blog pages"

echo "Done!"
