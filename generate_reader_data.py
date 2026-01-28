#!/usr/bin/env python3
"""Generate reader data files (manifest.json and page JSONs) from extracted text files."""

import json
import os
import re
import html

PAGES_DIR = "/Users/adrian/personal/clrs/clrs_pages"
OUTPUT_DATA_DIR = "/Users/adrian/personal/clrs/reader/data"
OUTPUT_PAGES_DIR = os.path.join(OUTPUT_DATA_DIR, "pages")
TOTAL_PAGES = 1313

def extract_title_from_text(text, page_num):
    """Extract a meaningful title from the page text."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]

    # Try to find chapter headers, section titles, etc.
    for line in lines[:10]:  # Check first 10 non-empty lines
        # Skip very short lines or page numbers
        if len(line) < 3 or line.isdigit():
            continue
        # Skip lines that are just numbers or symbols
        if re.match(r'^[\d\.\s]+$', line):
            continue
        # Return first meaningful line as title (truncate if too long)
        title = line[:80]
        if len(line) > 80:
            title += "..."
        return title

    return f"Page {page_num}"

def escape_html_content(text):
    """Convert plain text to HTML-safe content with basic formatting."""
    # Escape HTML special characters
    text = html.escape(text)
    # Convert newlines to <br> or wrap in paragraphs
    paragraphs = text.split('\n\n')
    formatted = []
    for p in paragraphs:
        p = p.strip()
        if p:
            # Keep single newlines within paragraphs
            p = p.replace('\n', '<br>')
            formatted.append(f'<p>{p}</p>')
    return '\n'.join(formatted)

def generate_page_json(page_num, text):
    """Generate JSON data for a single page."""
    title = extract_title_from_text(text, page_num)
    content_html = f'''<div class="article-header">
    <div class="section-label">Page {page_num}</div>
    <h2>{html.escape(title)}</h2>
</div>
<div class="original-content">
    <pre class="page-text">{html.escape(text)}</pre>
</div>'''

    return {
        "page": page_num,
        "title": title,
        "content": content_html
    }

def main():
    # Create output directories
    os.makedirs(OUTPUT_PAGES_DIR, exist_ok=True)

    manifest = {
        "title": "Introduction to Algorithms, Third Edition",
        "authors": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "totalPages": TOTAL_PAGES,
        "pages": []
    }

    for page_num in range(1, TOTAL_PAGES + 1):
        txt_file = os.path.join(PAGES_DIR, f"page-{page_num:04d}.txt")

        # Read text content
        if os.path.exists(txt_file):
            with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
        else:
            text = f"Page {page_num} content not available."

        # Generate page JSON
        page_data = generate_page_json(page_num, text)

        # Save page JSON
        page_json_file = os.path.join(OUTPUT_PAGES_DIR, f"page-{page_num:04d}.json")
        with open(page_json_file, 'w', encoding='utf-8') as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)

        # Add to manifest
        manifest["pages"].append({
            "page": page_num,
            "title": page_data["title"],
            "hasContent": True
        })

        if page_num % 100 == 0:
            print(f"Processed {page_num}/{TOTAL_PAGES} pages...")

    # Save manifest
    manifest_file = os.path.join(OUTPUT_DATA_DIR, "manifest.json")
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Generated {TOTAL_PAGES} page JSON files and manifest.json")

if __name__ == "__main__":
    main()
