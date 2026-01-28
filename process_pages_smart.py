#!/usr/bin/env python3
"""
Smart processor for CLRS pages - extracts structure and creates formatted HTML content.
Identifies chapters, sections, algorithms, theorems, definitions, etc.
"""

import json
import os
import re
import html
from pathlib import Path

PAGES_DIR = Path("/Users/adrian/personal/clrs/clrs_pages")
OUTPUT_DIR = Path("/Users/adrian/personal/clrs/reader/data/pages")
MANIFEST_FILE = Path("/Users/adrian/personal/clrs/reader/data/manifest.json")

# CLRS structure patterns
CHAPTER_PATTERN = re.compile(r'^(\d+)\s+([A-Z][A-Za-z\s\-]+)$', re.MULTILINE)
SECTION_PATTERN = re.compile(r'^(\d+\.\d+)\s+([A-Z][A-Za-z\s\-,]+)', re.MULTILINE)
SUBSECTION_PATTERN = re.compile(r'^(\d+\.\d+\.\d+)\s+([A-Z][A-Za-z\s\-]+)', re.MULTILINE)
THEOREM_PATTERN = re.compile(r'(Theorem|Lemma|Corollary|Proposition)\s+(\d+[\.\d]*)', re.IGNORECASE)
DEFINITION_PATTERN = re.compile(r'(Definition|Property)\s*:?\s*(.+?)(?=\n\n|\Z)', re.DOTALL | re.IGNORECASE)
ALGORITHM_PATTERN = re.compile(r'([A-Z][A-Z\-]+)\s*\(([^)]*)\)', re.MULTILINE)
COMPLEXITY_PATTERN = re.compile(r'[OΘΩoθω]\s*\([^)]+\)')
EXERCISE_PATTERN = re.compile(r'^(\d+\.\d+-\d+|\d+\.\d+\.\d+)')

# Part titles in CLRS
PARTS = {
    "I": "Foundations",
    "II": "Sorting and Order Statistics",
    "III": "Data Structures",
    "IV": "Advanced Design and Analysis Techniques",
    "V": "Advanced Data Structures",
    "VI": "Graph Algorithms",
    "VII": "Selected Topics",
    "VIII": "Appendix: Mathematical Background"
}

def clean_text(text):
    """Clean extracted PDF text."""
    # Remove form feeds
    text = text.replace('\f', '')
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def identify_page_type(text, page_num):
    """Identify what type of content is on this page."""
    text_lower = text.lower()

    # Check for specific page types
    if page_num <= 5:
        return "front_matter"
    if "contents" in text_lower[:100]:
        return "toc"
    if "index" in text_lower[:50] and page_num > 1200:
        return "index"
    if "bibliography" in text_lower[:100]:
        return "bibliography"
    if re.search(r'^(exercises|problems)\s*$', text, re.MULTILINE | re.IGNORECASE):
        return "exercises"
    if CHAPTER_PATTERN.search(text[:500]):
        return "chapter_start"
    if "appendix" in text_lower[:100]:
        return "appendix"

    return "content"

def extract_key_concepts(text):
    """Extract key concepts, algorithms, and theorems from text."""
    concepts = {
        "theorems": [],
        "algorithms": [],
        "definitions": [],
        "complexities": [],
        "key_terms": []
    }

    # Find theorems, lemmas, corollaries
    for match in THEOREM_PATTERN.finditer(text):
        concepts["theorems"].append(f"{match.group(1)} {match.group(2)}")

    # Find algorithm names (ALL CAPS with parameters)
    for match in ALGORITHM_PATTERN.finditer(text):
        algo_name = match.group(1)
        if len(algo_name) > 2 and algo_name.isupper():
            concepts["algorithms"].append(algo_name)

    # Find complexity notations
    for match in COMPLEXITY_PATTERN.finditer(text):
        concepts["complexities"].append(match.group(0))

    # Remove duplicates
    for key in concepts:
        concepts[key] = list(dict.fromkeys(concepts[key]))

    return concepts

def extract_section_info(text):
    """Extract chapter/section information."""
    info = {"chapter": None, "section": None, "subsection": None}

    # Look for chapter
    chapter_match = CHAPTER_PATTERN.search(text[:1000])
    if chapter_match:
        info["chapter"] = f"{chapter_match.group(1)}. {chapter_match.group(2).strip()}"

    # Look for section
    section_match = SECTION_PATTERN.search(text[:500])
    if section_match:
        info["section"] = f"{section_match.group(1)} {section_match.group(2).strip()}"

    return info

def format_content_html(text, page_num, page_type, concepts, section_info):
    """Generate formatted HTML content for the page."""

    # Escape HTML in text
    safe_text = html.escape(text)

    # Determine section label
    if section_info["section"]:
        section_label = f"Section {section_info['section'].split()[0]}"
    elif section_info["chapter"]:
        section_label = f"Chapter {section_info['chapter'].split('.')[0]}"
    else:
        section_label = f"Page {page_num}"

    # Create title
    if section_info["section"]:
        title = section_info["section"]
    elif section_info["chapter"]:
        title = section_info["chapter"]
    else:
        # Extract first meaningful line as title
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 3]
        title = lines[0][:80] if lines else f"Page {page_num}"

    # Build content sections
    content_parts = []

    # Main content - format the text nicely
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []

    for para in paragraphs[:15]:  # Limit to avoid huge pages
        para = para.strip()
        if not para or len(para) < 10:
            continue

        # Check if it's a heading
        if re.match(r'^\d+(\.\d+)*\s+[A-Z]', para) and len(para) < 100:
            formatted_paragraphs.append(f'<h3>{html.escape(para)}</h3>')
        # Check if it looks like pseudocode/algorithm
        elif re.search(r'^\s*(for|while|if|return|else)\s', para, re.IGNORECASE) or para.strip().startswith('1 '):
            formatted_paragraphs.append(f'<pre class="algorithm">{html.escape(para)}</pre>')
        else:
            formatted_paragraphs.append(f'<p>{html.escape(para)}</p>')

    main_content = '\n'.join(formatted_paragraphs)

    # Build definition boxes for key concepts
    concept_boxes = []

    if concepts["theorems"]:
        theorems_list = ', '.join(concepts["theorems"][:5])
        concept_boxes.append(f'''
        <div class="highlight-box">
            <h4>Theorems & Lemmas</h4>
            <p>{html.escape(theorems_list)}</p>
        </div>''')

    if concepts["algorithms"]:
        algos_list = ', '.join(concepts["algorithms"][:5])
        concept_boxes.append(f'''
        <div class="definition-box">
            <h4>Algorithms</h4>
            <p><strong>{html.escape(algos_list)}</strong></p>
        </div>''')

    if concepts["complexities"]:
        complexity_list = ', '.join(list(set(concepts["complexities"]))[:5])
        concept_boxes.append(f'''
        <div class="figure-box">
            <h4>Complexity</h4>
            <p>{html.escape(complexity_list)}</p>
        </div>''')

    concept_html = '\n'.join(concept_boxes)

    # Build analysis section
    analysis_items = []

    if page_type == "chapter_start":
        analysis_items.append('''
        <div class="analysis-item">
            <h5>Chapter Overview</h5>
            <p>This page introduces a new chapter. Key concepts and algorithms will be developed throughout this section.</p>
        </div>''')

    if concepts["algorithms"]:
        analysis_items.append(f'''
        <div class="analysis-item">
            <h5>Key Algorithms</h5>
            <p>This page discusses: <strong>{html.escape(', '.join(concepts["algorithms"][:3]))}</strong></p>
        </div>''')

    if concepts["theorems"]:
        analysis_items.append(f'''
        <div class="analysis-item">
            <h5>Mathematical Foundations</h5>
            <p>Important results: {html.escape(', '.join(concepts["theorems"][:3]))}</p>
        </div>''')

    if not analysis_items:
        analysis_items.append('''
        <div class="analysis-item">
            <h5>Content Summary</h5>
            <p>This page continues the discussion of algorithms and data structures fundamental to computer science.</p>
        </div>''')

    analysis_html = '\n'.join(analysis_items)

    # Assemble final HTML
    html_content = f'''<div class="article-header">
    <div class="section-label">{html.escape(section_label)}</div>
    <h1>{html.escape(title)}</h1>
</div>
<div class="original-content">
    {concept_html}
    {main_content}
</div>
<div class="analysis-section">
    <h3>Quick Reference</h3>
    <div class="analysis-block">
        {analysis_html}
    </div>
</div>'''

    return html_content, title

def process_page(page_num):
    """Process a single page and return JSON data."""
    txt_file = PAGES_DIR / f"page-{page_num:04d}.txt"

    if not txt_file.exists():
        return None

    with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
        raw_text = f.read()

    text = clean_text(raw_text)

    if len(text) < 20:
        # Nearly empty page
        return {
            "page": page_num,
            "title": f"Page {page_num}",
            "content": f'''<div class="article-header">
    <div class="section-label">Page {page_num}</div>
    <h1>Page {page_num}</h1>
</div>
<div class="original-content">
    <p><em>This page contains minimal text content (diagrams, figures, or blank space).</em></p>
</div>'''
        }

    page_type = identify_page_type(text, page_num)
    concepts = extract_key_concepts(text)
    section_info = extract_section_info(text)

    content_html, title = format_content_html(text, page_num, page_type, concepts, section_info)

    return {
        "page": page_num,
        "title": title,
        "content": content_html
    }

def main():
    """Process all pages."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest_pages = []

    for page_num in range(1, 1314):
        page_data = process_page(page_num)

        if page_data:
            # Save page JSON
            output_file = OUTPUT_DIR / f"page-{page_num:04d}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(page_data, f, ensure_ascii=False, indent=2)

            manifest_pages.append({
                "page": page_num,
                "title": page_data["title"],
                "hasContent": True
            })

        if page_num % 100 == 0:
            print(f"Processed {page_num}/1313...")

    # Update manifest
    manifest = {
        "title": "Introduction to Algorithms, Third Edition",
        "authors": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "totalPages": 1313,
        "pages": manifest_pages
    }

    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Processed 1313 pages.")

if __name__ == "__main__":
    main()
