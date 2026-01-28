#!/usr/bin/env python3
"""
Enhanced processor for CLRS pages - creates rich formatted content
with algorithm boxes, theorem highlights, and meaningful analysis.
"""

import json
import os
import re
import html
from pathlib import Path

PAGES_DIR = Path("/Users/adrian/personal/clrs/clrs_pages")
OUTPUT_DIR = Path("/Users/adrian/personal/clrs/reader/data/pages")
MANIFEST_FILE = Path("/Users/adrian/personal/clrs/reader/data/manifest.json")

# Known CLRS algorithms and their descriptions
KNOWN_ALGORITHMS = {
    "INSERTION-SORT": "Simple sorting algorithm that builds the sorted array one element at a time",
    "MERGE-SORT": "Divide-and-conquer sorting algorithm with O(n log n) time complexity",
    "MERGE": "Combines two sorted subarrays into one sorted array",
    "HEAPSORT": "Comparison-based sorting using a binary heap data structure",
    "QUICKSORT": "Efficient divide-and-conquer sorting with average O(n log n)",
    "PARTITION": "Rearranges elements around a pivot for quicksort",
    "RANDOMIZED-QUICKSORT": "Quicksort with random pivot selection",
    "COUNTING-SORT": "Linear time sorting for integers in a known range",
    "RADIX-SORT": "Sorts integers digit by digit",
    "BUCKET-SORT": "Distributes elements into buckets then sorts each bucket",
    "BUILD-MAX-HEAP": "Converts an array into a max-heap",
    "MAX-HEAPIFY": "Maintains the max-heap property",
    "HEAP-EXTRACT-MAX": "Removes and returns the maximum element from a heap",
    "BFS": "Breadth-first search for graph traversal",
    "DFS": "Depth-first search for graph traversal",
    "DFS-VISIT": "Recursive helper for depth-first search",
    "DIJKSTRA": "Single-source shortest paths with non-negative weights",
    "BELLMAN-FORD": "Single-source shortest paths, handles negative weights",
    "FLOYD-WARSHALL": "All-pairs shortest paths using dynamic programming",
    "PRIM": "Minimum spanning tree using greedy approach",
    "KRUSKAL": "Minimum spanning tree using edge sorting",
    "TOPOLOGICAL-SORT": "Linear ordering of vertices in a DAG",
    "STRONGLY-CONNECTED-COMPONENTS": "Finds all SCCs in a directed graph",
    "BINARY-SEARCH": "Efficient search in sorted array, O(log n)",
    "RANDOMIZED-SELECT": "Linear expected time selection algorithm",
    "HASH-INSERT": "Insert element into hash table",
    "HASH-SEARCH": "Search for element in hash table",
    "CHAINED-HASH-INSERT": "Insert into hash table with chaining",
    "TREE-INSERT": "Insert node into binary search tree",
    "TREE-SEARCH": "Search for key in binary search tree",
    "TREE-DELETE": "Delete node from binary search tree",
    "RB-INSERT": "Insert into red-black tree with rebalancing",
    "RB-DELETE": "Delete from red-black tree with rebalancing",
    "LCS-LENGTH": "Longest common subsequence using DP",
    "PRINT-LCS": "Print the longest common subsequence",
    "MATRIX-CHAIN-ORDER": "Optimal matrix multiplication order",
    "OPTIMAL-BST": "Construct optimal binary search tree",
    "HUFFMAN": "Build optimal prefix-free codes",
    "ACTIVITY-SELECTOR": "Greedy activity selection",
    "GREEDY-ACTIVITY-SELECTOR": "Greedy activity selection",
    "FORD-FULKERSON": "Maximum flow algorithm",
    "EDMONDS-KARP": "Maximum flow with BFS",
    "PUSH-RELABEL": "Maximum flow using preflow",
    "RELABEL-TO-FRONT": "Maximum flow variant",
    "KMP-MATCHER": "Knuth-Morris-Pratt string matching",
    "COMPUTE-PREFIX-FUNCTION": "Compute failure function for KMP",
    "RABIN-KARP-MATCHER": "String matching with hashing",
    "FINITE-AUTOMATON-MATCHER": "String matching using automata",
    "NAIVE-STRING-MATCHER": "Brute-force string matching",
    "SQUARE-MATRIX-MULTIPLY": "Standard matrix multiplication",
    "STRASSEN": "Fast matrix multiplication",
}

# Chapter topics for context
CHAPTER_TOPICS = {
    1: ("The Role of Algorithms", "Introduction to algorithms, efficiency, and problem-solving"),
    2: ("Getting Started", "Insertion sort, analyzing algorithms, designing algorithms"),
    3: ("Growth of Functions", "Asymptotic notation, standard notations, common functions"),
    4: ("Divide-and-Conquer", "Maximum subarray, matrix multiplication, recurrences"),
    5: ("Probabilistic Analysis", "Hiring problem, indicator random variables, randomized algorithms"),
    6: ("Heapsort", "Heaps, maintaining heap property, building heaps, heapsort"),
    7: ("Quicksort", "Description, performance, randomized version"),
    8: ("Sorting in Linear Time", "Lower bounds, counting sort, radix sort, bucket sort"),
    9: ("Medians and Order Statistics", "Minimum/maximum, selection in linear time"),
    10: ("Elementary Data Structures", "Stacks, queues, linked lists, trees"),
    11: ("Hash Tables", "Direct addressing, hash functions, open addressing"),
    12: ("Binary Search Trees", "BST property, queries, insertion, deletion"),
    13: ("Red-Black Trees", "Properties, rotations, insertion, deletion"),
    14: ("Augmenting Data Structures", "Dynamic order statistics, interval trees"),
    15: ("Dynamic Programming", "Rod cutting, matrix chain, LCS, optimal BST"),
    16: ("Greedy Algorithms", "Activity selection, Huffman codes, matroids"),
    17: ("Amortized Analysis", "Aggregate, accounting, potential methods"),
    18: ("B-Trees", "Definition, operations, deletion"),
    19: ("Fibonacci Heaps", "Structure, operations, bounds"),
    20: ("van Emde Boas Trees", "Preliminary, recursive structure, operations"),
    21: ("Data Structures for Disjoint Sets", "Operations, linked lists, forests"),
    22: ("Elementary Graph Algorithms", "Representations, BFS, DFS, topological sort"),
    23: ("Minimum Spanning Trees", "Growing MST, Kruskal, Prim"),
    24: ("Single-Source Shortest Paths", "Bellman-Ford, Dijkstra, DAG shortest paths"),
    25: ("All-Pairs Shortest Paths", "Matrix multiplication, Floyd-Warshall, Johnson"),
    26: ("Maximum Flow", "Flow networks, Ford-Fulkerson, maximum bipartite matching"),
    27: ("Multithreaded Algorithms", "Parallel computing, spawn, sync"),
    28: ("Matrix Operations", "LUP decomposition, matrix inversion"),
    29: ("Linear Programming", "Formulation, simplex algorithm"),
    30: ("Polynomials and FFT", "DFT, FFT, polynomial multiplication"),
    31: ("Number-Theoretic Algorithms", "GCD, modular arithmetic, RSA"),
    32: ("String Matching", "Naive, Rabin-Karp, KMP, automata"),
    33: ("Computational Geometry", "Line segments, convex hull"),
    34: ("NP-Completeness", "P, NP, reductions, NP-complete problems"),
    35: ("Approximation Algorithms", "Vertex cover, TSP, set cover"),
}

def clean_text(text):
    """Clean extracted PDF text."""
    text = text.replace('\f', '')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def detect_chapter(text):
    """Detect chapter number from page text."""
    # Look for "Chapter X" pattern
    match = re.search(r'Chapter\s+(\d+)', text[:200])
    if match:
        return int(match.group(1))
    # Look for section number like "22.3"
    match = re.search(r'^(\d+)\.\d+\s+[A-Z]', text, re.MULTILINE)
    if match:
        return int(match.group(1))
    return None

def extract_algorithms(text):
    """Extract algorithm pseudocode blocks."""
    algorithms = []

    # Pattern for algorithm name (ALL CAPS with hyphen)
    algo_pattern = re.compile(r'([A-Z][A-Z\-]+(?:\s*\([^)]*\))?)\s*\n((?:\s*\d+\s+.*\n?)+)', re.MULTILINE)

    for match in algo_pattern.finditer(text):
        name = match.group(1).strip()
        # Clean the name
        name = re.sub(r'\s*\([^)]*\)', '', name).strip()

        if name in KNOWN_ALGORITHMS or (len(name) > 3 and name.replace('-', '').isupper()):
            code = match.group(2).strip()
            # Check if it looks like pseudocode (has line numbers)
            if re.search(r'^\s*\d+\s+', code):
                algorithms.append({
                    "name": name,
                    "code": code,
                    "description": KNOWN_ALGORITHMS.get(name, "Algorithm from CLRS")
                })

    return algorithms

def extract_theorems(text):
    """Extract theorems, lemmas, corollaries."""
    theorems = []

    pattern = re.compile(
        r'(Theorem|Lemma|Corollary|Proposition)\s+(\d+[\.\d]*)\s*(?:\(([^)]+)\))?\s*(.*?)(?=\n\n|Proof|Theorem|Lemma|Corollary|$)',
        re.DOTALL | re.IGNORECASE
    )

    for match in pattern.finditer(text):
        theorems.append({
            "type": match.group(1).capitalize(),
            "number": match.group(2),
            "name": match.group(3) or "",
            "statement": match.group(4).strip()[:500]
        })

    return theorems[:5]  # Limit to 5

def extract_complexity(text):
    """Extract complexity notations."""
    complexities = set()

    # O, Θ, Ω notations
    pattern = re.compile(r'[OΘΩ‚]\s*\([^)]+\)')
    for match in pattern.finditer(text):
        complexities.add(match.group(0))

    return list(complexities)[:5]

def get_page_type(text, page_num):
    """Determine the type of page."""
    if page_num <= 5:
        return "front"
    if "Contents" in text[:100]:
        return "toc"
    if page_num > 1250 and "Index" in text[:100]:
        return "index"
    if re.search(r'^Exercises\s*$', text, re.MULTILINE):
        return "exercises"
    if re.search(r'^\d+\.\d+-\d+', text, re.MULTILINE):
        return "exercises"
    if re.search(r'^Problems\s*$', text, re.MULTILINE):
        return "problems"

    return "content"

def create_algorithm_html(algo):
    """Create HTML for an algorithm."""
    desc = html.escape(algo['description'])
    code = html.escape(algo['code'])
    name = html.escape(algo['name'])

    return f'''
<div class="algorithm">
    <span class="algorithm-name">{name}</span>
    <p style="margin: 0.5rem 0; color: #475569; font-family: var(--font-sans); font-size: 0.85rem;">{desc}</p>
    <pre style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">{code}</pre>
</div>'''

def create_theorem_html(theorem):
    """Create HTML for a theorem."""
    type_name = html.escape(theorem['type'])
    number = html.escape(theorem['number'])
    name = f" ({html.escape(theorem['name'])})" if theorem['name'] else ""
    statement = html.escape(theorem['statement'][:300])

    return f'''
<div class="theorem-box">
    <h4>{type_name} {number}{name}</h4>
    <p>{statement}</p>
</div>'''

def format_page_content(text, page_num, algorithms, theorems, complexities, chapter):
    """Create the final HTML content for a page."""

    # Get chapter context
    chapter_info = CHAPTER_TOPICS.get(chapter, (None, None))
    chapter_name = chapter_info[0] if chapter_info[0] else ""
    chapter_desc = chapter_info[1] if chapter_info[1] else ""

    # Determine section label
    section_match = re.search(r'^(\d+\.\d+)\s+([A-Za-z\s\-]+)', text, re.MULTILINE)
    if section_match:
        section_label = f"Section {section_match.group(1)}"
        title = f"{section_match.group(1)} {section_match.group(2).strip()}"
    elif chapter:
        section_label = f"Chapter {chapter}"
        title = chapter_name or f"Chapter {chapter}"
    else:
        section_label = f"Page {page_num}"
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 5]
        title = lines[0][:60] if lines else f"Page {page_num}"

    # Build content sections
    parts = []

    # Algorithm boxes
    if algorithms:
        for algo in algorithms[:3]:
            parts.append(create_algorithm_html(algo))

    # Theorem boxes
    if theorems:
        for thm in theorems[:3]:
            parts.append(create_theorem_html(thm))

    # Complexity highlight
    if complexities:
        comp_text = ', '.join([f'<span class="complexity">{html.escape(c)}</span>' for c in complexities])
        parts.append(f'''
<div class="highlight-box">
    <h4>Time Complexity</h4>
    <p>{comp_text}</p>
</div>''')

    # Main text content (cleaned and formatted)
    paragraphs = text.split('\n\n')
    text_parts = []
    for para in paragraphs[:10]:
        para = para.strip()
        if not para or len(para) < 20:
            continue
        # Skip if it's an algorithm we already processed
        if any(algo['name'] in para for algo in algorithms):
            continue
        text_parts.append(f'<p>{html.escape(para)}</p>')

    if text_parts:
        parts.append('<div class="text-content">' + '\n'.join(text_parts[:5]) + '</div>')

    content_html = '\n'.join(parts)

    # Build analysis section
    analysis_items = []

    if algorithms:
        algo_names = ', '.join([f"<strong>{html.escape(a['name'])}</strong>" for a in algorithms[:3]])
        analysis_items.append(f'''
<div class="analysis-item">
    <h5>Algorithms Covered</h5>
    <p>This page presents: {algo_names}</p>
    <ul>
        {''.join([f"<li><strong>{html.escape(a['name'])}:</strong> {html.escape(a['description'])}</li>" for a in algorithms[:3]])}
    </ul>
</div>''')

    if theorems:
        thm_list = ', '.join([f"{t['type']} {t['number']}" for t in theorems[:3]])
        analysis_items.append(f'''
<div class="analysis-item">
    <h5>Key Results</h5>
    <p>Important theoretical foundations: {html.escape(thm_list)}</p>
</div>''')

    if complexities:
        analysis_items.append(f'''
<div class="analysis-item">
    <h5>Complexity Analysis</h5>
    <p>Running times discussed: {', '.join([html.escape(c) for c in complexities])}</p>
</div>''')

    if chapter_desc and chapter:
        analysis_items.append(f'''
<div class="analysis-item">
    <h5>Chapter Context</h5>
    <p><strong>Chapter {chapter}: {html.escape(chapter_name)}</strong><br>{html.escape(chapter_desc)}</p>
</div>''')

    if not analysis_items:
        analysis_items.append('''
<div class="analysis-item">
    <h5>Overview</h5>
    <p>This page covers fundamental concepts in algorithm design and analysis from the CLRS textbook.</p>
</div>''')

    analysis_html = '\n'.join(analysis_items)

    # Final HTML
    final_html = f'''<div class="article-header">
    <div class="section-label">{html.escape(section_label)}</div>
    <h1>{html.escape(title)}</h1>
</div>
<div class="original-content">
    {content_html}
</div>
<div class="analysis-section">
    <h3>Quick Reference</h3>
    <div class="analysis-block">
        {analysis_html}
    </div>
</div>'''

    return final_html, title

def process_page(page_num):
    """Process a single page."""
    txt_file = PAGES_DIR / f"page-{page_num:04d}.txt"

    if not txt_file.exists():
        return None

    with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
        raw_text = f.read()

    text = clean_text(raw_text)

    if len(text) < 30:
        return {
            "page": page_num,
            "title": f"Page {page_num}",
            "content": f'''<div class="article-header">
    <div class="section-label">Page {page_num}</div>
    <h1>Page {page_num}</h1>
</div>
<div class="original-content">
    <p><em>This page contains primarily figures, diagrams, or minimal text.</em></p>
</div>'''
        }

    page_type = get_page_type(text, page_num)
    chapter = detect_chapter(text)

    algorithms = extract_algorithms(text)
    theorems = extract_theorems(text)
    complexities = extract_complexity(text)

    content_html, title = format_page_content(
        text, page_num, algorithms, theorems, complexities, chapter
    )

    return {
        "page": page_num,
        "title": title,
        "content": content_html
    }

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest_pages = []

    for page_num in range(1, 1314):
        page_data = process_page(page_num)

        if page_data:
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

    manifest = {
        "title": "Introduction to Algorithms, Third Edition",
        "authors": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "totalPages": 1313,
        "pages": manifest_pages
    }

    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("\nDone!")

if __name__ == "__main__":
    main()
