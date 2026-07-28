#!/bin/bash
cd /root/kanok-miahit
git diff c822841~1..c822841 -- src/app/blog/data.js 2>/dev/null || git show c822841 -- src/app/blog/data.js 2>/dev/null | head -3000
