=== DATA QUALITY SCAN REPORT ===
File: /root/kanok-miahit/src/app/blog/data.js
Size: 27,527 lines / 3.2 MB
Total posts: 128 (all verified by slug count)

============================================================
CHECK 1: Raw HTML Comments (<!--)
RESULT: ALL CLEAN — 0 occurrences found
============================================================

CHECK 2: Raw <script> Tags in Content
RESULT: ALL CLEAN
- 8 occurrences of <script found, ALL inside code blocks
  (```html or ```json fenced blocks showing JSON-LD schema examples)
- 3 additional occurrences are inline text references (escaped as \`<script>\`)
- No raw, unescaped <script> tags that would execute
============================================================

CHECK 3: Stray Markdown Artifacts
RESULT: All within content (as expected)
- ** (bold markers): 3,821 lines — legitimate markdown in content
- ]( (markdown links): 1,312 lines — legitimate markdown in content
- ## headings: 3,483 lines — all inside content template literals ✓
============================================================

CHECK 4: Post Structure Validation
RESULT: ALL POSTS VALID ✓
- 128/128 posts have all 5 required fields: slug, title, date, author, tags
- 0 posts with missing required fields
- 0 duplicate slugs ✓
- 0 duplicate titles ✓
- All slugs use lowercase-kebab-case format ✓
- All dates in YYYY-MM-DD format ✓
- 0 empty tag arrays ✓
- 0 console.log/debugger statements ✓
- No BOM character ✓

============================================================
CHECK 5: Additional Issues Found

ISSUE 5a: Inline comment on content closing (1 occurrence)
- Line 156: content ends with `, // EEAT Optimized: 2026-07-15
  (Backtick+comma followed by inline // comment)
  This is the only line with this pattern; all other 127 content
  closing lines end cleanly with `<backtick>,`

ISSUE 5b: Trailing whitespace in content (~19 lines)
- 5 content paragraph lines end with a single space:
  lines 315, 458, 622, 796, 19907
- 1 intentional markdown line-break double-space: line 1264
- ~13 blank separator lines inside content have 4 spaces of
  indentation (lines 17119, 17439, 17725, 18041, 18389, 18663,
  18990, 19522, 19734, 19964, 20190, 20455, 20691, 20953)

ISSUE 5c: Long content lines (281 lines exceed 500 chars)
- These are content lines within markdown template literals.
  Very long lines can indicate paragraphs that weren't wrapped.
- Example: Line 16 (644 chars), Line 38 (778 chars)
  This is a readability/maintainability concern, not a functional bug.

ISSUE 5d: metaDescription > 160 chars (5 posts)
- Line 12: 197 chars
- Line 7476: 188 chars (Bengali)
- Line 7781: 201 chars (Bengali)
- Line 8089: 195 chars (Bengali)
- Line 8381: 198 chars (Bengali)
  (160 chars is the recommended Google display limit)
  Bengali descriptions being longer is somewhat expected.

============================================================
SUMMARY
============================================================
CRITICAL ISSUES: 0
MODERATE ISSUES: 0
MINOR ISSUES: 4
  - 1 inline comment on content closing (line 156)
  - ~19 lines with trailing whitespace
  - 281 very long content lines (>500 chars)
  - 5 metaDescriptions over 160 char limit

ALL STRUCTURAL CHECKS PASSED: Post structure, slug uniqueness,
date format, required fields, and content boundaries are all clean.
