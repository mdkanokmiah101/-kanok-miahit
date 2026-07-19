#!/usr/bin/awk -f
# Extract blog posts by slug from data.js
# Tracks backtick-delimited content fields to correctly handle closing braces

BEGIN {
    printing = 0
    in_backtick = 0
    post_count = 0
}

{
    # If we're printing, always output the line (after processing)
    
    # Check if this line opens a backtick content field
    if (printing) {
        # Track backtick state: count backticks on this line
        # A content field starts with ` after content: and ends with `, on its own line
        if ($0 ~ /^    content: `$/) {
            in_backtick = 1
        }
    }
    
    # Check for start condition
    if ($0 ~ /^\{$/) {
        # Look ahead at next line to check slug
        # We can't peek in awk easily, so we check the line AFTER seeing the slug
        # Actually let's handle it differently - start on the slug line and backfill
    }
}

# Check for target slug lines
/^    slug: "seo-for-fitness-gyms-bangladesh",$/ {
    printing = 1
    in_backtick = 0
    print "{"
    print $0
    next
}

/^    slug: "seo-for-law-firms-bangladesh",$/ {
    printing = 1
    in_backtick = 0
    print "{"
    print $0
    next
}

/^    slug: "seo-for-startups-bangladesh",$/ {
    printing = 1
    in_backtick = 0
    print "{"
    print $0
    next
}

# If we're printing
printing == 1 {
    # Track backtick state
    if ($0 ~ /^    content: `$/) {
        in_backtick = 1
    }
    
    # Check for closing backtick (`,` on its own line after content)
    if (in_backtick && $0 ~ /^`,$/) {
        in_backtick = 0
    }
    
    # Check for post closing `  },` - only when NOT in a backtick
    if (!in_backtick && $0 ~ /^  },$/) {
        printing = 0
        print $0
        print ""  # blank line separator
        post_count++
        next
    }
    
    print $0
}

END {
    if (post_count != 3) {
        print "WARNING: Extracted " post_count " posts (expected 3)" > "/dev/stderr"
    }
}
