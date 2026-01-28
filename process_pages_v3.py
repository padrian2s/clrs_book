#!/usr/bin/env python3
"""
Enhanced processor for CLRS - handles spaced algorithm names like H EAP -E XTRACT-M AX.
"""

import json
import re
import html
from pathlib import Path

PAGES_DIR = Path("/Users/adrian/personal/clrs/clrs_pages")
OUTPUT_DIR = Path("/Users/adrian/personal/clrs/reader/data/pages")
MANIFEST_FILE = Path("/Users/adrian/personal/clrs/reader/data/manifest.json")

# Algorithm descriptions
ALGO_DESC = {
    "INSERTION-SORT": "Builds sorted array one element at a time, O(n²)",
    "MERGE-SORT": "Divide-and-conquer sorting, O(n log n)",
    "MERGE": "Combines two sorted subarrays",
    "HEAPSORT": "Sorting using binary heap, O(n log n)",
    "BUILD-MAX-HEAP": "Converts array into max-heap",
    "MAX-HEAPIFY": "Maintains max-heap property",
    "HEAP-MAXIMUM": "Returns maximum element in heap",
    "HEAP-EXTRACT-MAX": "Removes and returns max from heap",
    "HEAP-INCREASE-KEY": "Increases key value in heap",
    "MAX-HEAP-INSERT": "Inserts element into max-heap",
    "QUICKSORT": "Divide-and-conquer sorting, average O(n log n)",
    "PARTITION": "Partitions array around pivot",
    "RANDOMIZED-PARTITION": "Random pivot selection",
    "RANDOMIZED-QUICKSORT": "Quicksort with randomization",
    "COUNTING-SORT": "Linear time sorting for integers",
    "RADIX-SORT": "Sorts by digits, O(d(n+k))",
    "BUCKET-SORT": "Distribution sort, average O(n)",
    "MINIMUM": "Finds minimum element",
    "MAXIMUM": "Finds maximum element",
    "RANDOMIZED-SELECT": "Linear expected time selection",
    "SELECT": "Worst-case linear selection",
    "STACK-EMPTY": "Checks if stack is empty",
    "PUSH": "Pushes element onto stack",
    "POP": "Pops element from stack",
    "ENQUEUE": "Adds element to queue",
    "DEQUEUE": "Removes element from queue",
    "LIST-SEARCH": "Searches linked list",
    "LIST-INSERT": "Inserts into linked list",
    "LIST-DELETE": "Deletes from linked list",
    "ALLOCATE-OBJECT": "Allocates memory",
    "FREE-OBJECT": "Frees memory",
    "TREE-SEARCH": "Searches binary search tree",
    "ITERATIVE-TREE-SEARCH": "Non-recursive BST search",
    "TREE-MINIMUM": "Finds minimum in BST",
    "TREE-MAXIMUM": "Finds maximum in BST",
    "TREE-SUCCESSOR": "Finds successor node",
    "TREE-INSERT": "Inserts node into BST",
    "TRANSPLANT": "Replaces subtree",
    "TREE-DELETE": "Deletes node from BST",
    "LEFT-ROTATE": "Red-black tree rotation",
    "RIGHT-ROTATE": "Red-black tree rotation",
    "RB-INSERT": "Red-black tree insertion",
    "RB-INSERT-FIXUP": "Fixes RB properties after insert",
    "RB-TRANSPLANT": "RB tree transplant",
    "RB-DELETE": "Red-black tree deletion",
    "RB-DELETE-FIXUP": "Fixes RB properties after delete",
    "OS-SELECT": "Order-statistics selection",
    "OS-RANK": "Computes rank in tree",
    "INTERVAL-SEARCH": "Searches interval tree",
    "CUT-ROD": "Naive rod cutting",
    "MEMOIZED-CUT-ROD": "Top-down DP rod cutting",
    "BOTTOM-UP-CUT-ROD": "Bottom-up DP rod cutting",
    "PRINT-CUT-ROD-SOLUTION": "Prints optimal rod cuts",
    "MATRIX-CHAIN-ORDER": "Optimal matrix chain multiplication",
    "PRINT-OPTIMAL-PARENS": "Prints optimal parenthesization",
    "LCS-LENGTH": "Longest common subsequence DP",
    "PRINT-LCS": "Prints LCS",
    "OPTIMAL-BST": "Optimal binary search tree",
    "RECURSIVE-ACTIVITY-SELECTOR": "Recursive greedy activity selection",
    "GREEDY-ACTIVITY-SELECTOR": "Iterative greedy activity selection",
    "HUFFMAN": "Huffman encoding algorithm",
    "BFS": "Breadth-first search, O(V+E)",
    "DFS": "Depth-first search, O(V+E)",
    "DFS-VISIT": "DFS recursive helper",
    "TOPOLOGICAL-SORT": "Topological ordering of DAG",
    "STRONGLY-CONNECTED-COMPONENTS": "Finds SCCs",
    "MST-KRUSKAL": "Minimum spanning tree - Kruskal",
    "MST-PRIM": "Minimum spanning tree - Prim",
    "INITIALIZE-SINGLE-SOURCE": "Initializes shortest path estimates",
    "RELAX": "Relaxation for shortest paths",
    "BELLMAN-FORD": "Single-source shortest paths, handles negative edges",
    "DAG-SHORTEST-PATHS": "Shortest paths in DAG",
    "DIJKSTRA": "Single-source shortest paths, non-negative weights",
    "EXTEND-SHORTEST-PATHS": "Matrix multiplication approach",
    "FLOYD-WARSHALL": "All-pairs shortest paths DP",
    "TRANSITIVE-CLOSURE": "Computes transitive closure",
    "JOHNSON": "All-pairs with Bellman-Ford + Dijkstra",
    "FORD-FULKERSON": "Maximum flow algorithm",
    "FORD-FULKERSON-METHOD": "Maximum flow method",
    "EDMONDS-KARP": "BFS-based max flow",
    "PUSH": "Push operation for preflow",
    "RELABEL": "Relabel operation",
    "GENERIC-PUSH-RELABEL": "Generic push-relabel",
    "INITIALIZE-PREFLOW": "Initializes preflow",
    "DISCHARGE": "Discharge operation",
    "RELABEL-TO-FRONT": "Relabel-to-front max flow",
    "FIB-HEAP-INSERT": "Fibonacci heap insert",
    "FIB-HEAP-MINIMUM": "Fibonacci heap minimum",
    "FIB-HEAP-EXTRACT-MIN": "Fibonacci heap extract-min",
    "CONSOLIDATE": "Fibonacci heap consolidate",
    "FIB-HEAP-DECREASE-KEY": "Fibonacci heap decrease-key",
    "CUT": "Fibonacci heap cut",
    "CASCADING-CUT": "Fibonacci heap cascading cut",
    "FIB-HEAP-DELETE": "Fibonacci heap delete",
    "MAKE-SET": "Creates singleton set",
    "UNION": "Union of two sets",
    "LINK": "Links two trees",
    "FIND-SET": "Finds representative",
    "CONNECTED-COMPONENTS": "Finds connected components",
    "SAME-COMPONENT": "Tests same component",
    "VEB-TREE-MEMBER": "van Emde Boas membership",
    "VEB-TREE-MINIMUM": "van Emde Boas minimum",
    "VEB-TREE-SUCCESSOR": "van Emde Boas successor",
    "VEB-TREE-INSERT": "van Emde Boas insert",
    "VEB-TREE-DELETE": "van Emde Boas delete",
    "NAIVE-STRING-MATCHER": "Brute-force string matching",
    "RABIN-KARP-MATCHER": "String matching with hashing",
    "FINITE-AUTOMATON-MATCHER": "String matching with automata",
    "COMPUTE-TRANSITION-FUNCTION": "Computes automaton transitions",
    "KMP-MATCHER": "Knuth-Morris-Pratt matching",
    "COMPUTE-PREFIX-FUNCTION": "Computes KMP failure function",
    "SEGMENTS-INTERSECT": "Tests segment intersection",
    "ANY-SEGMENTS-INTERSECT": "Detects any intersection",
    "GRAHAM-SCAN": "Convex hull algorithm",
    "JARVIS-MARCH": "Gift wrapping convex hull",
    "APPROX-VERTEX-COVER": "2-approximation vertex cover",
    "APPROX-TSP-TOUR": "TSP approximation",
    "GREEDY-SET-COVER": "Set cover approximation",
    "APPROX-SUBSET-SUM": "Subset sum approximation",
}

# Chapter info
CHAPTERS = {
    1: "The Role of Algorithms in Computing",
    2: "Getting Started",
    3: "Growth of Functions",
    4: "Divide-and-Conquer",
    5: "Probabilistic Analysis and Randomized Algorithms",
    6: "Heapsort",
    7: "Quicksort",
    8: "Sorting in Linear Time",
    9: "Medians and Order Statistics",
    10: "Elementary Data Structures",
    11: "Hash Tables",
    12: "Binary Search Trees",
    13: "Red-Black Trees",
    14: "Augmenting Data Structures",
    15: "Dynamic Programming",
    16: "Greedy Algorithms",
    17: "Amortized Analysis",
    18: "B-Trees",
    19: "Fibonacci Heaps",
    20: "van Emde Boas Trees",
    21: "Data Structures for Disjoint Sets",
    22: "Elementary Graph Algorithms",
    23: "Minimum Spanning Trees",
    24: "Single-Source Shortest Paths",
    25: "All-Pairs Shortest Paths",
    26: "Maximum Flow",
    27: "Multithreaded Algorithms",
    28: "Matrix Operations",
    29: "Linear Programming",
    30: "Polynomials and the FFT",
    31: "Number-Theoretic Algorithms",
    32: "String Matching",
    33: "Computational Geometry",
    34: "NP-Completeness",
    35: "Approximation Algorithms",
}

def normalize_algo_name(spaced_name):
    """Convert 'H EAP -E XTRACT-M AX' to 'HEAP-EXTRACT-MAX'."""
    # Remove spaces between letters but keep hyphens
    result = re.sub(r'([A-Z])\s+([A-Z])', r'\1\2', spaced_name)
    result = re.sub(r'([A-Z])\s+([A-Z])', r'\1\2', result)  # Run twice for consecutive
    result = re.sub(r'\s*-\s*', '-', result)
    return result.strip()

def extract_algorithms(text):
    """Extract algorithm blocks from CLRS text."""
    algorithms = []

    # Pattern: Algorithm name (with possible spaces) followed by parameters, then numbered lines
    # Example: H EAP -E XTRACT-M AX .A/
    #          1 if A:heap-size < 1
    # Allow leading whitespace
    pattern = re.compile(
        r'^\s*([A-Z][A-Z\s\-]+)\s*\.([^/\n]*)/\s*\n((?:\s*\d+\s+[^\n]+\n?)+)',
        re.MULTILINE
    )

    for match in pattern.finditer(text):
        raw_name = match.group(1).strip()
        params = match.group(2).strip()
        code = match.group(3).strip()

        # Normalize the name
        name = normalize_algo_name(raw_name)

        # Only include if it looks like a real algorithm
        if len(name) > 2 and name.replace('-', '').isalpha():
            desc = ALGO_DESC.get(name, "Algorithm from CLRS textbook")
            algorithms.append({
                "name": name,
                "params": params,
                "code": code,
                "description": desc
            })

    return algorithms

def extract_theorems(text):
    """Extract theorems, lemmas, corollaries."""
    theorems = []

    pattern = re.compile(
        r'(Theorem|Lemma|Corollary)\s+(\d+[\.\d]*)\s*(?:\(([^)]+)\))?\s*\n(.*?)(?=\n\n|Proof\.|\Z)',
        re.DOTALL | re.IGNORECASE
    )

    for match in pattern.finditer(text):
        stmt = match.group(4).strip()[:400]
        if len(stmt) > 30:
            theorems.append({
                "type": match.group(1).capitalize(),
                "number": match.group(2),
                "name": match.group(3) or "",
                "statement": stmt
            })

    return theorems[:4]

def extract_complexity(text):
    """Extract big-O notations."""
    complexities = set()
    # Match O(xxx), Θ(xxx), Ω(xxx), ‚(xxx) patterns
    for match in re.finditer(r'[OΘΩ‚]\s*\([^)]{1,30}\)', text):
        complexities.add(match.group(0).replace(' ', ''))
    return list(complexities)[:6]

def detect_chapter(text):
    """Detect chapter number."""
    match = re.search(r'Chapter\s+(\d+)', text[:300])
    if match:
        return int(match.group(1))
    match = re.search(r'^(\d+)\.[\d\.]+\s+', text, re.MULTILINE)
    if match:
        return int(match.group(1))
    return None

def detect_section(text):
    """Detect section number and title."""
    match = re.search(r'^(\d+\.\d+)\s+([A-Za-z][A-Za-z\s\-]+)', text, re.MULTILINE)
    if match:
        return match.group(1), match.group(2).strip()
    return None, None

def create_algo_html(algo):
    """Create formatted HTML for algorithm."""
    name = html.escape(algo['name'])
    params = html.escape(algo['params'])
    code_lines = algo['code'].split('\n')
    formatted_lines = []

    for line in code_lines:
        line = line.strip()
        if not line:
            continue
        # Extract line number and content
        match = re.match(r'^(\d+)\s+(.*)$', line)
        if match:
            num = match.group(1)
            content = html.escape(match.group(2))
            # Highlight keywords
            for kw in ['for', 'while', 'if', 'else', 'return', 'error', 'to', 'downto', 'do', 'and', 'or', 'not', 'NIL', 'TRUE', 'FALSE']:
                content = re.sub(rf'\b{kw}\b', f'<b>{kw}</b>', content)
            formatted_lines.append(f'<span style="color:#64748b">{num:>2}</span>  {content}')
        else:
            formatted_lines.append(html.escape(line))

    code_html = '\n'.join(formatted_lines)
    desc = html.escape(algo['description'])

    return f'''
<div class="algorithm">
    <span class="algorithm-name">{name}({params})</span>
    <p style="margin:0.3rem 0;color:#475569;font-size:0.85rem;font-family:var(--font-sans);">{desc}</p>
    <pre style="margin-top:0.5rem;font-size:0.82rem;line-height:1.7;">{code_html}</pre>
</div>'''

def create_theorem_html(thm):
    """Create formatted HTML for theorem."""
    type_n = html.escape(thm['type'])
    num = html.escape(thm['number'])
    name = f" ({html.escape(thm['name'])})" if thm['name'] else ""
    stmt = html.escape(thm['statement'])

    return f'''
<div class="theorem-box">
    <h4>{type_n} {num}{name}</h4>
    <p style="font-style:italic;">{stmt}</p>
</div>'''

def process_page(page_num):
    """Process a single page."""
    txt_file = PAGES_DIR / f"page-{page_num:04d}.txt"
    if not txt_file.exists():
        return None

    with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read().replace('\f', '').strip()

    if len(text) < 50:
        return {
            "page": page_num,
            "title": f"Page {page_num}",
            "content": f'''<div class="article-header">
    <div class="section-label">Page {page_num}</div>
    <h1>Page {page_num}</h1>
</div>
<div class="original-content">
    <p><em>Primarily figures or diagrams.</em></p>
</div>'''
        }

    chapter = detect_chapter(text)
    section_num, section_title = detect_section(text)
    algorithms = extract_algorithms(text)
    theorems = extract_theorems(text)
    complexities = extract_complexity(text)

    # Determine title and label
    if section_num:
        label = f"Section {section_num}"
        title = f"{section_num} {section_title}"
    elif chapter:
        label = f"Chapter {chapter}"
        title = CHAPTERS.get(chapter, f"Chapter {chapter}")
    else:
        label = f"Page {page_num}"
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l) > 5]
        title = lines[0][:70] if lines else f"Page {page_num}"

    # Build content
    parts = []

    # Algorithms
    for algo in algorithms[:3]:
        parts.append(create_algo_html(algo))

    # Theorems
    for thm in theorems[:2]:
        parts.append(create_theorem_html(thm))

    # Complexity box
    if complexities and not algorithms:
        comp_html = ', '.join([f'<span class="complexity">{html.escape(c)}</span>' for c in complexities])
        parts.append(f'''
<div class="highlight-box">
    <h4>Complexity Analysis</h4>
    <p>{comp_html}</p>
</div>''')

    # Text summary (if no algorithms found)
    if not algorithms:
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
        for p in paragraphs[:4]:
            parts.append(f'<p>{html.escape(p)}</p>')

    content = '\n'.join(parts) if parts else f'<p>{html.escape(text[:1000])}</p>'

    # Analysis section
    analysis = []

    if algorithms:
        algo_items = ''.join([f'<li><strong>{html.escape(a["name"])}</strong>: {html.escape(a["description"])}</li>' for a in algorithms[:4]])
        analysis.append(f'''
<div class="analysis-item">
    <h5>Algorithms on This Page</h5>
    <ul>{algo_items}</ul>
</div>''')

    if theorems:
        thm_names = ', '.join([f'{t["type"]} {t["number"]}' for t in theorems])
        analysis.append(f'''
<div class="analysis-item">
    <h5>Key Results</h5>
    <p>{html.escape(thm_names)}</p>
</div>''')

    if complexities and algorithms:
        analysis.append(f'''
<div class="analysis-item">
    <h5>Running Times</h5>
    <p>{', '.join([html.escape(c) for c in complexities])}</p>
</div>''')

    if chapter:
        analysis.append(f'''
<div class="analysis-item">
    <h5>Chapter</h5>
    <p><strong>{chapter}. {html.escape(CHAPTERS.get(chapter, ""))}</strong></p>
</div>''')

    if not analysis:
        analysis.append('''
<div class="analysis-item">
    <h5>Overview</h5>
    <p>Foundational material from Introduction to Algorithms (CLRS).</p>
</div>''')

    analysis_html = '\n'.join(analysis)

    return {
        "page": page_num,
        "title": title,
        "content": f'''<div class="article-header">
    <div class="section-label">{html.escape(label)}</div>
    <h1>{html.escape(title)}</h1>
</div>
<div class="original-content">
    {content}
</div>
<div class="analysis-section">
    <h3>Quick Reference</h3>
    <div class="analysis-block">
        {analysis_html}
    </div>
</div>'''
    }

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_pages = []

    for page_num in range(1, 1314):
        data = process_page(page_num)
        if data:
            with open(OUTPUT_DIR / f"page-{page_num:04d}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            manifest_pages.append({"page": page_num, "title": data["title"], "hasContent": True})

        if page_num % 100 == 0:
            print(f"{page_num}/1313...")

    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "title": "Introduction to Algorithms, Third Edition",
            "authors": "Cormen, Leiserson, Rivest, Stein",
            "totalPages": 1313,
            "pages": manifest_pages
        }, f, ensure_ascii=False, indent=2)

    print("Done!")

if __name__ == "__main__":
    main()
