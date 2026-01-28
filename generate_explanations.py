#!/usr/bin/env python3
"""
Generate educational explanations for all CLRS pages.
This script creates rich, educational content for each page.
"""

import json
import re
import html
from pathlib import Path

PAGES_DIR = Path("/Users/adrian/personal/clrs/clrs_pages")
OUTPUT_DIR = Path("/Users/adrian/personal/clrs/reader/data/pages")
MANIFEST_FILE = Path("/Users/adrian/personal/clrs/reader/data/manifest.json")

# ============== ALGORITHM EXPLANATIONS ==============
ALGO_EXPLANATIONS = {
    "INSERTION-SORT": {
        "simple": "Like sorting playing cards in your hand - pick each card and insert it in the right position among the already-sorted cards.",
        "how": "For each element, shift larger elements right until you find the correct spot, then insert.",
        "when": "Best for small arrays or nearly-sorted data. Simple to implement.",
        "complexity": "O(n²) worst/average, O(n) best case (already sorted)",
        "space": "O(1) - sorts in place"
    },
    "MERGE-SORT": {
        "simple": "Divide the array in half, sort each half, then merge them back together.",
        "how": "Recursively split until single elements, then merge pairs in sorted order.",
        "when": "When you need guaranteed O(n log n) performance. Great for linked lists.",
        "complexity": "O(n log n) always - very consistent",
        "space": "O(n) - needs extra space for merging"
    },
    "MERGE": {
        "simple": "Combines two sorted arrays into one sorted array.",
        "how": "Compare first elements of each array, take the smaller, repeat until done.",
        "when": "Used as a subroutine in merge sort and other divide-and-conquer algorithms.",
        "complexity": "O(n) where n is total elements",
        "space": "O(n) for the merged result"
    },
    "QUICKSORT": {
        "simple": "Pick a 'pivot' element, put smaller elements left and larger elements right, then sort each side.",
        "how": "Partition around pivot, recursively sort left and right partitions.",
        "when": "Default choice for general sorting - fastest in practice for most data.",
        "complexity": "O(n log n) average, O(n²) worst case (rare with good pivot selection)",
        "space": "O(log n) for recursion stack"
    },
    "PARTITION": {
        "simple": "Rearranges array so elements smaller than pivot are left, larger are right.",
        "how": "Scan from both ends, swap elements that are on the wrong side.",
        "when": "Core subroutine of quicksort and selection algorithms.",
        "complexity": "O(n) - single pass through array",
        "space": "O(1) - in place"
    },
    "HEAPSORT": {
        "simple": "Build a heap from the data, then repeatedly extract the maximum to build sorted array.",
        "how": "Create max-heap, swap root with last element, reduce heap size, heapify, repeat.",
        "when": "When you need guaranteed O(n log n) with O(1) extra space.",
        "complexity": "O(n log n) always",
        "space": "O(1) - sorts in place"
    },
    "BUILD-MAX-HEAP": {
        "simple": "Transforms an unsorted array into a max-heap structure.",
        "how": "Start from the last non-leaf node and heapify each node going upward.",
        "when": "First step of heapsort, or when building a priority queue from existing data.",
        "complexity": "O(n) - surprisingly linear, not O(n log n)!",
        "space": "O(1) - modifies array in place"
    },
    "MAX-HEAPIFY": {
        "simple": "Fixes a single violation of the heap property by 'floating down' an element.",
        "how": "Compare node with children, swap with larger child if needed, repeat down the tree.",
        "when": "After extracting max from heap, or during heap construction.",
        "complexity": "O(log n) - proportional to tree height",
        "space": "O(1) or O(log n) if recursive"
    },
    "HEAP-EXTRACT-MAX": {
        "simple": "Removes and returns the largest element from a max-heap.",
        "how": "Save root (max), replace with last element, reduce size, heapify root.",
        "when": "Priority queue 'dequeue' operation, or during heapsort.",
        "complexity": "O(log n) due to heapify",
        "space": "O(1)"
    },
    "COUNTING-SORT": {
        "simple": "Count occurrences of each value, then place elements directly in their final positions.",
        "how": "Create count array, compute cumulative counts, place each element at its counted position.",
        "when": "Integers in a known, small range. Basis for radix sort.",
        "complexity": "O(n + k) where k is the range of values",
        "space": "O(n + k)"
    },
    "RADIX-SORT": {
        "simple": "Sort numbers digit by digit, starting from least significant.",
        "how": "Use counting sort (stable) for each digit position, right to left.",
        "when": "Large numbers of integers with bounded digits. Very fast in practice.",
        "complexity": "O(d(n + k)) where d is digits, k is base",
        "space": "O(n + k)"
    },
    "BUCKET-SORT": {
        "simple": "Distribute elements into buckets, sort each bucket, concatenate.",
        "how": "Hash elements to buckets, sort buckets (often with insertion sort), combine.",
        "when": "Uniformly distributed data in a known range. Expected linear time.",
        "complexity": "O(n) average, O(n²) worst case",
        "space": "O(n)"
    },
    "BFS": {
        "simple": "Explore a graph level by level, visiting all neighbors before going deeper.",
        "how": "Use a queue: visit node, enqueue all unvisited neighbors, repeat.",
        "when": "Shortest path in unweighted graphs, level-order traversal, testing connectivity.",
        "complexity": "O(V + E) - visits each vertex and edge once",
        "space": "O(V) for the queue"
    },
    "DFS": {
        "simple": "Explore a graph by going as deep as possible before backtracking.",
        "how": "Use recursion or stack: visit node, recurse on unvisited neighbors.",
        "when": "Detecting cycles, topological sort, finding connected components, maze solving.",
        "complexity": "O(V + E)",
        "space": "O(V) for recursion stack"
    },
    "DIJKSTRA": {
        "simple": "Find shortest paths from a source by always expanding the closest unvisited vertex.",
        "how": "Use priority queue: extract minimum distance vertex, relax all its edges, repeat.",
        "when": "Shortest paths with non-negative edge weights. GPS navigation, network routing.",
        "complexity": "O((V + E) log V) with binary heap",
        "space": "O(V)"
    },
    "BELLMAN-FORD": {
        "simple": "Find shortest paths by repeatedly relaxing all edges V-1 times.",
        "how": "For V-1 iterations, try to improve distance to each vertex via each edge.",
        "when": "Graphs with negative edge weights. Also detects negative cycles.",
        "complexity": "O(VE) - slower than Dijkstra but more general",
        "space": "O(V)"
    },
    "FLOYD-WARSHALL": {
        "simple": "Find shortest paths between ALL pairs of vertices using dynamic programming.",
        "how": "For each intermediate vertex k, update all pairs (i,j) if going through k is shorter.",
        "when": "Dense graphs where you need all-pairs shortest paths. Also for transitive closure.",
        "complexity": "O(V³)",
        "space": "O(V²)"
    },
    "PRIM": {
        "simple": "Build minimum spanning tree by always adding the cheapest edge to an unvisited vertex.",
        "how": "Start from any vertex, repeatedly add minimum-weight edge crossing the cut.",
        "when": "Finding MST, especially in dense graphs. Network design, clustering.",
        "complexity": "O(E log V) with binary heap",
        "space": "O(V)"
    },
    "KRUSKAL": {
        "simple": "Build MST by adding edges in weight order, skipping those that would create a cycle.",
        "how": "Sort edges, use union-find to check if edge connects different components.",
        "when": "Finding MST, especially in sparse graphs.",
        "complexity": "O(E log E) dominated by sorting",
        "space": "O(V) for union-find"
    },
    "TOPOLOGICAL-SORT": {
        "simple": "Order vertices so all edges point forward (from earlier to later in the order).",
        "how": "DFS and add vertices to front of list when finished, OR repeatedly remove vertices with no incoming edges.",
        "when": "Task scheduling with dependencies, build systems, course prerequisites.",
        "complexity": "O(V + E)",
        "space": "O(V)"
    },
    "BINARY-SEARCH": {
        "simple": "Find a target in a sorted array by repeatedly halving the search space.",
        "how": "Compare target with middle element, eliminate half of remaining elements, repeat.",
        "when": "Searching in sorted data. Foundation for many algorithms.",
        "complexity": "O(log n) - extremely efficient",
        "space": "O(1) iterative, O(log n) recursive"
    },
    "LCS-LENGTH": {
        "simple": "Find the longest sequence of characters that appears in both strings (not necessarily contiguous).",
        "how": "Build 2D table: if chars match, extend diagonal; otherwise, take max of left/above.",
        "when": "Diff tools, DNA sequence alignment, version control, spell checking.",
        "complexity": "O(mn) where m, n are string lengths",
        "space": "O(mn) but can be reduced to O(min(m,n))"
    },
    "MATRIX-CHAIN-ORDER": {
        "simple": "Find the best way to parenthesize matrix multiplications to minimize operations.",
        "how": "DP: for each chain length, try all split points, keep minimum cost.",
        "when": "Optimizing matrix computations in scientific computing, graphics.",
        "complexity": "O(n³) where n is number of matrices",
        "space": "O(n²)"
    },
    "HUFFMAN": {
        "simple": "Build optimal prefix-free codes for data compression based on character frequencies.",
        "how": "Repeatedly merge two lowest-frequency nodes into one, building a tree bottom-up.",
        "when": "Data compression (ZIP, JPEG, MP3 use variations). Information theory.",
        "complexity": "O(n log n) with priority queue",
        "space": "O(n)"
    },
    "FORD-FULKERSON": {
        "simple": "Find maximum flow in a network by repeatedly finding and augmenting along paths.",
        "how": "While there's a path from source to sink with available capacity, push flow along it.",
        "when": "Network flow problems: transportation, bipartite matching, image segmentation.",
        "complexity": "O(E × max_flow) - depends on path-finding method",
        "space": "O(V + E)"
    },
    "KMP-MATCHER": {
        "simple": "Efficient string matching that never backtracks in the text.",
        "how": "Precompute failure function to know where to continue after a mismatch.",
        "when": "Finding pattern in text. Used in text editors, grep, DNA analysis.",
        "complexity": "O(n + m) - linear in both text and pattern length",
        "space": "O(m) for the failure function"
    },
}

# ============== CHAPTER SUMMARIES ==============
CHAPTER_INFO = {
    1: {
        "name": "The Role of Algorithms in Computing",
        "summary": "Introduces what algorithms are and why they matter. Defines the problem of sorting as a running example.",
        "key_concepts": ["Algorithm definition", "Instance of a problem", "Correctness", "Efficiency"],
        "real_world": "Algorithms are everywhere: Google Search, GPS navigation, social media feeds, video compression."
    },
    2: {
        "name": "Getting Started",
        "summary": "Your first algorithms! Insertion sort teaches basic algorithm design. Merge sort introduces divide-and-conquer.",
        "key_concepts": ["Loop invariants", "Analyzing running time", "Divide-and-conquer", "Recursion"],
        "real_world": "Sorting is fundamental - databases, spreadsheets, and file managers all depend on it."
    },
    3: {
        "name": "Growth of Functions",
        "summary": "The mathematical tools for analyzing algorithms. Big-O, Big-Theta, and Big-Omega notation.",
        "key_concepts": ["Asymptotic notation", "O, Θ, Ω, o, ω", "Comparing growth rates", "Common functions"],
        "real_world": "Helps predict if your code will scale - can it handle 1 million users?"
    },
    4: {
        "name": "Divide-and-Conquer",
        "summary": "Break problems into smaller subproblems, solve recursively, combine solutions.",
        "key_concepts": ["Recurrence relations", "Master theorem", "Substitution method", "Recursion trees"],
        "real_world": "Merge sort, quicksort, FFT, Strassen's matrix multiplication all use this paradigm."
    },
    5: {
        "name": "Probabilistic Analysis and Randomized Algorithms",
        "summary": "Using randomness to analyze and design algorithms. Expected running time vs worst case.",
        "key_concepts": ["Indicator random variables", "Expected value", "Randomized algorithms", "Hiring problem"],
        "real_world": "Quicksort's random pivot, hash functions, Monte Carlo simulations."
    },
    6: {
        "name": "Heapsort",
        "summary": "A clever sorting algorithm using the heap data structure. Also introduces priority queues.",
        "key_concepts": ["Heap property", "Heapify", "Building a heap", "Priority queues"],
        "real_world": "Priority queues are used in Dijkstra's algorithm, task schedulers, event-driven simulation."
    },
    7: {
        "name": "Quicksort",
        "summary": "The most practical sorting algorithm. Fast average case, elegant divide-and-conquer design.",
        "key_concepts": ["Partitioning", "Pivot selection", "Randomized quicksort", "Worst-case analysis"],
        "real_world": "Default sort in many standard libraries. Used billions of times daily."
    },
    8: {
        "name": "Sorting in Linear Time",
        "summary": "Breaking the O(n log n) barrier! When we know more about our data, we can sort faster.",
        "key_concepts": ["Lower bound Ω(n log n)", "Counting sort", "Radix sort", "Bucket sort"],
        "real_world": "Sorting integers (ages, zip codes), strings, or uniformly distributed data."
    },
    9: {
        "name": "Medians and Order Statistics",
        "summary": "Finding the k-th smallest element without fully sorting. Median in linear time!",
        "key_concepts": ["Selection problem", "Randomized select", "Worst-case linear selection", "Median-of-medians"],
        "real_world": "Database queries (TOP K), statistics, quick median finding."
    },
    10: {
        "name": "Elementary Data Structures",
        "summary": "The building blocks: stacks, queues, linked lists, and trees.",
        "key_concepts": ["LIFO (stack)", "FIFO (queue)", "Pointers", "Sentinel nodes"],
        "real_world": "Browser back button (stack), print queue (queue), memory management (linked lists)."
    },
    11: {
        "name": "Hash Tables",
        "summary": "O(1) average-case lookup! The most practical data structure for key-value storage.",
        "key_concepts": ["Hash functions", "Collision resolution", "Chaining", "Open addressing"],
        "real_world": "Dictionaries in Python/JavaScript, database indexes, caches, symbol tables."
    },
    12: {
        "name": "Binary Search Trees",
        "summary": "A tree structure maintaining sorted order with O(log n) operations.",
        "key_concepts": ["BST property", "Inorder traversal", "Successor/predecessor", "Tree rotations"],
        "real_world": "Database indexes, file system directories, auto-complete suggestions."
    },
    13: {
        "name": "Red-Black Trees",
        "summary": "Self-balancing BST guaranteeing O(log n) operations even in worst case.",
        "key_concepts": ["Color properties", "Rotations", "Insertion fixup", "Deletion fixup"],
        "real_world": "Java TreeMap, C++ std::map, Linux kernel's scheduling."
    },
    14: {
        "name": "Augmenting Data Structures",
        "summary": "Extending data structures to support additional operations efficiently.",
        "key_concepts": ["Order statistics trees", "Interval trees", "Maintaining augmented info"],
        "real_world": "Range queries, finding overlapping intervals, database indexes."
    },
    15: {
        "name": "Dynamic Programming",
        "summary": "Solving optimization problems by breaking into overlapping subproblems and storing solutions.",
        "key_concepts": ["Optimal substructure", "Overlapping subproblems", "Memoization", "Bottom-up"],
        "real_world": "Spell checkers (edit distance), route planning, resource allocation, bioinformatics."
    },
    16: {
        "name": "Greedy Algorithms",
        "summary": "Making locally optimal choices hoping for global optimum. Simpler than DP when it works!",
        "key_concepts": ["Greedy choice property", "Optimal substructure", "Matroids", "Activity selection"],
        "real_world": "Huffman coding (compression), minimum spanning trees, scheduling."
    },
    17: {
        "name": "Amortized Analysis",
        "summary": "Analyzing average cost over a sequence of operations, not just worst single operation.",
        "key_concepts": ["Aggregate method", "Accounting method", "Potential method", "Dynamic arrays"],
        "real_world": "Understanding why dynamic arrays (ArrayList, vector) are efficient despite resizing."
    },
    18: {
        "name": "B-Trees",
        "summary": "Trees optimized for disk access with high branching factor.",
        "key_concepts": ["Multi-way trees", "Disk I/O", "Splitting nodes", "B+ trees"],
        "real_world": "Database indexes, file systems. Your data on disk is probably in a B-tree!"
    },
    19: {
        "name": "Fibonacci Heaps",
        "summary": "Advanced heap with O(1) amortized insert and decrease-key operations.",
        "key_concepts": ["Lazy merging", "Cascading cuts", "Amortized bounds", "Potential function"],
        "real_world": "Optimizes Dijkstra and Prim algorithms for sparse graphs."
    },
    20: {
        "name": "van Emde Boas Trees",
        "summary": "O(log log U) operations for integer keys in a fixed universe!",
        "key_concepts": ["Universe size U", "Recursive structure", "Cluster and summary"],
        "real_world": "Very fast priority queues when keys are bounded integers."
    },
    21: {
        "name": "Data Structures for Disjoint Sets",
        "summary": "Efficiently track which elements are in which group, with fast union and find.",
        "key_concepts": ["Union by rank", "Path compression", "Nearly O(1) operations"],
        "real_world": "Kruskal's MST, connected components, image segmentation, social networks."
    },
    22: {
        "name": "Elementary Graph Algorithms",
        "summary": "BFS and DFS - the foundation of all graph algorithms.",
        "key_concepts": ["Graph representations", "BFS", "DFS", "Topological sort", "SCC"],
        "real_world": "Social networks, web crawlers, GPS navigation, dependency resolution."
    },
    23: {
        "name": "Minimum Spanning Trees",
        "summary": "Connect all vertices with minimum total edge weight.",
        "key_concepts": ["Cut property", "Kruskal's algorithm", "Prim's algorithm", "Safe edges"],
        "real_world": "Network design, clustering, approximation algorithms for TSP."
    },
    24: {
        "name": "Single-Source Shortest Paths",
        "summary": "Finding shortest paths from one source to all other vertices.",
        "key_concepts": ["Relaxation", "Bellman-Ford", "Dijkstra", "DAG shortest paths"],
        "real_world": "GPS navigation, network routing protocols (OSPF, RIP)."
    },
    25: {
        "name": "All-Pairs Shortest Paths",
        "summary": "Shortest paths between every pair of vertices.",
        "key_concepts": ["Floyd-Warshall", "Johnson's algorithm", "Matrix multiplication method"],
        "real_world": "Traffic analysis, network analysis, transitive closure."
    },
    26: {
        "name": "Maximum Flow",
        "summary": "How much can 'flow' through a network from source to sink?",
        "key_concepts": ["Flow networks", "Ford-Fulkerson", "Max-flow min-cut theorem", "Bipartite matching"],
        "real_world": "Transportation networks, bipartite matching, image segmentation."
    },
    27: {
        "name": "Multithreaded Algorithms",
        "summary": "Parallel algorithms for multi-core processors.",
        "key_concepts": ["Spawn and sync", "Work and span", "Parallelism", "Race conditions"],
        "real_world": "Modern CPUs have multiple cores - parallelism is essential for performance."
    },
    28: {
        "name": "Matrix Operations",
        "summary": "Solving systems of linear equations, matrix inversion.",
        "key_concepts": ["LU decomposition", "Forward/back substitution", "Matrix inversion"],
        "real_world": "Scientific computing, graphics, machine learning."
    },
    29: {
        "name": "Linear Programming",
        "summary": "Optimizing a linear objective subject to linear constraints.",
        "key_concepts": ["Standard form", "Slack variables", "Simplex algorithm", "Duality"],
        "real_world": "Resource allocation, scheduling, operations research, economics."
    },
    30: {
        "name": "Polynomials and the FFT",
        "summary": "Fast Fourier Transform - O(n log n) polynomial multiplication!",
        "key_concepts": ["DFT", "FFT", "Convolution theorem", "Roots of unity"],
        "real_world": "Signal processing, audio/image compression, big integer multiplication."
    },
    31: {
        "name": "Number-Theoretic Algorithms",
        "summary": "Algorithms for integers: GCD, modular arithmetic, primality testing.",
        "key_concepts": ["Euclid's algorithm", "Modular exponentiation", "RSA", "Primality testing"],
        "real_world": "Cryptography! RSA, key exchange, digital signatures."
    },
    32: {
        "name": "String Matching",
        "summary": "Finding a pattern within a text efficiently.",
        "key_concepts": ["Naive matching", "Rabin-Karp", "KMP", "Finite automata"],
        "real_world": "Text editors (find/replace), grep, plagiarism detection, DNA analysis."
    },
    33: {
        "name": "Computational Geometry",
        "summary": "Algorithms for geometric problems in 2D and 3D.",
        "key_concepts": ["Line segment intersection", "Convex hull", "Closest pair"],
        "real_world": "Computer graphics, robotics, GIS, collision detection in games."
    },
    34: {
        "name": "NP-Completeness",
        "summary": "The theory of computational hardness. Some problems are (probably) inherently difficult.",
        "key_concepts": ["P vs NP", "NP-complete", "Reductions", "Cook-Levin theorem"],
        "real_world": "Understanding which problems have no efficient solution helps avoid wasted effort."
    },
    35: {
        "name": "Approximation Algorithms",
        "summary": "When problems are NP-hard, find good-enough solutions efficiently.",
        "key_concepts": ["Approximation ratio", "Vertex cover", "TSP", "Set cover"],
        "real_world": "Real-world optimization often uses approximations: delivery routing, scheduling."
    },
}

def normalize_algo_name(spaced_name):
    """Convert 'H EAP -E XTRACT-M AX' to 'HEAP-EXTRACT-MAX'."""
    result = re.sub(r'([A-Z])\s+([A-Z])', r'\1\2', spaced_name)
    result = re.sub(r'([A-Z])\s+([A-Z])', r'\1\2', result)
    result = re.sub(r'\s*-\s*', '-', result)
    return result.strip()

def extract_algorithms(text):
    """Extract algorithm blocks."""
    algorithms = []
    pattern = re.compile(
        r'^\s*([A-Z][A-Z\s\-]+)\s*\.([^/\n]*)/\s*\n((?:\s*\d+\s+[^\n]+\n?)+)',
        re.MULTILINE
    )
    for match in pattern.finditer(text):
        name = normalize_algo_name(match.group(1).strip())
        if len(name) > 2:
            algorithms.append({
                "name": name,
                "params": match.group(2).strip(),
                "code": match.group(3).strip()
            })
    return algorithms

def extract_theorems(text):
    """Extract theorems."""
    theorems = []
    pattern = re.compile(
        r'(Theorem|Lemma|Corollary)\s+(\d+[\.\d]*)\s*(?:\(([^)]+)\))?\s*\n(.*?)(?=\n\n|Proof\.|\Z)',
        re.DOTALL | re.IGNORECASE
    )
    for match in pattern.finditer(text):
        stmt = match.group(4).strip()[:500]
        if len(stmt) > 20:
            theorems.append({
                "type": match.group(1).capitalize(),
                "number": match.group(2),
                "name": match.group(3) or "",
                "statement": stmt
            })
    return theorems[:3]

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
    """Detect section."""
    match = re.search(r'^(\d+\.\d+)\s+([A-Za-z][A-Za-z\s\-]+)', text, re.MULTILINE)
    if match:
        return match.group(1), match.group(2).strip()
    return None, None

def get_page_type(text, page_num):
    """Determine page type."""
    if page_num <= 5:
        return "front"
    if page_num <= 25 and "Contents" in text[:200]:
        return "toc"
    if page_num > 1250:
        return "back"
    if re.search(r'^\d+\.\d+-\d+', text, re.MULTILINE):
        return "exercises"
    if re.search(r'^Problems\s*$', text, re.MULTILINE | re.IGNORECASE):
        return "problems"
    if "Preface" in text[:100]:
        return "preface"
    return "content"

def create_algo_html(algo):
    """Create HTML for algorithm with explanation."""
    name = algo['name']
    params = html.escape(algo['params'])

    # Get explanation
    expl = ALGO_EXPLANATIONS.get(name, {})
    simple = expl.get('simple', f"Algorithm that performs the {name.lower().replace('-', ' ')} operation.")
    how = expl.get('how', '')
    when = expl.get('when', '')
    complexity = expl.get('complexity', '')

    # Format code
    code_lines = []
    for line in algo['code'].split('\n'):
        line = line.strip()
        if not line:
            continue
        match = re.match(r'^(\d+)\s+(.*)$', line)
        if match:
            num = match.group(1)
            content = html.escape(match.group(2))
            for kw in ['for', 'while', 'if', 'else', 'elseif', 'return', 'error', 'to', 'downto', 'do', 'and', 'or', 'not', 'NIL', 'TRUE', 'FALSE', 'then']:
                content = re.sub(rf'\b{kw}\b', f'<b>{kw}</b>', content, flags=re.IGNORECASE)
            code_lines.append(f'<span style="color:#64748b">{num:>2}</span>  {content}')
    code_html = '\n'.join(code_lines)

    explanation_parts = []
    if how:
        explanation_parts.append(f'<p><strong>How it works:</strong> {html.escape(how)}</p>')
    if when:
        explanation_parts.append(f'<p><strong>When to use:</strong> {html.escape(when)}</p>')
    if complexity:
        explanation_parts.append(f'<p><strong>Complexity:</strong> <span class="complexity">{html.escape(complexity)}</span></p>')

    explanation_html = '\n'.join(explanation_parts)

    return f'''
<div class="definition-box">
    <h4>{html.escape(name)}({params})</h4>
    <p><em>{html.escape(simple)}</em></p>
</div>
<div class="algorithm">
    <pre style="font-size:0.82rem;line-height:1.7;">{code_html}</pre>
</div>
<div class="highlight-box">
    <h4>Understanding {html.escape(name)}</h4>
    {explanation_html}
</div>'''

def create_theorem_html(thm):
    """Create HTML for theorem."""
    return f'''
<div class="theorem-box">
    <h4>{html.escape(thm["type"])} {html.escape(thm["number"])}{" (" + html.escape(thm["name"]) + ")" if thm["name"] else ""}</h4>
    <p style="font-style:italic;">{html.escape(thm["statement"])}</p>
</div>'''

def create_chapter_intro_html(chapter):
    """Create chapter introduction."""
    info = CHAPTER_INFO.get(chapter, {})
    name = info.get('name', f'Chapter {chapter}')
    summary = info.get('summary', '')
    concepts = info.get('key_concepts', [])
    real_world = info.get('real_world', '')

    concepts_html = ''.join([f'<li>{html.escape(c)}</li>' for c in concepts])

    return f'''
<div class="definition-box">
    <h4>Chapter Overview</h4>
    <p>{html.escape(summary)}</p>
</div>
<div class="highlight-box">
    <h4>Key Concepts</h4>
    <ul>{concepts_html}</ul>
</div>
<div class="figure-box">
    <h4>Real-World Applications</h4>
    <p>{html.escape(real_world)}</p>
</div>'''

def process_page(page_num):
    """Process a single page."""
    txt_file = PAGES_DIR / f"page-{page_num:04d}.txt"
    if not txt_file.exists():
        return None

    with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read().replace('\f', '').strip()

    page_type = get_page_type(text, page_num)
    chapter = detect_chapter(text)
    section_num, section_title = detect_section(text)
    algorithms = extract_algorithms(text)
    theorems = extract_theorems(text)

    # Determine title and label
    if section_num:
        label = f"Section {section_num}"
        title = f"{section_num} {section_title}"
    elif chapter and chapter in CHAPTER_INFO:
        label = f"Chapter {chapter}"
        title = CHAPTER_INFO[chapter]['name']
    else:
        label = f"Page {page_num}"
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l) > 5]
        title = lines[0][:70] if lines else f"Page {page_num}"

    # Handle special page types
    if page_type == "front" and page_num <= 5:
        return create_front_matter_page(page_num, text)

    if page_type == "toc":
        return {
            "page": page_num,
            "title": "Table of Contents",
            "content": f'''<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Table of Contents</h1>
</div>
<div class="original-content">
    <p>This page contains the table of contents. Use the image view (press <kbd>V</kbd>) to see the full layout.</p>
    <div class="highlight-box">
        <h4>Navigation Tip</h4>
        <p>You can use the search function in the menu to find specific topics or algorithms.</p>
    </div>
</div>'''
        }

    if page_type == "exercises":
        return {
            "page": page_num,
            "title": title if section_num else "Exercises",
            "content": f'''<div class="article-header">
    <div class="section-label">{html.escape(label)}</div>
    <h1>Exercises</h1>
</div>
<div class="original-content">
    <div class="highlight-box">
        <h4>Practice Problems</h4>
        <p>This page contains exercises to test your understanding. Working through problems is essential for mastering algorithms!</p>
    </div>
    <p><strong>Tip:</strong> Try solving problems on paper before looking at solutions. The struggle is part of learning.</p>
</div>
<div class="analysis-section">
    <h3>Study Tips</h3>
    <div class="analysis-block">
        <div class="analysis-item">
            <h5>How to Approach Problems</h5>
            <ul>
                <li>Read the problem carefully - what are the inputs and outputs?</li>
                <li>Think about edge cases</li>
                <li>Consider multiple approaches before coding</li>
                <li>Analyze time and space complexity</li>
            </ul>
        </div>
    </div>
</div>'''
        }

    if len(text) < 50:
        return {
            "page": page_num,
            "title": title,
            "content": f'''<div class="article-header">
    <div class="section-label">{html.escape(label)}</div>
    <h1>{html.escape(title)}</h1>
</div>
<div class="original-content">
    <p><em>This page contains primarily figures or diagrams. Switch to image view (press <kbd>V</kbd>) to see the visual content.</em></p>
</div>'''
        }

    # Build main content
    parts = []

    # Chapter introduction if this looks like a chapter start
    if chapter and "Chapter" in text[:200] and chapter in CHAPTER_INFO:
        parts.append(create_chapter_intro_html(chapter))

    # Algorithms with explanations
    for algo in algorithms[:3]:
        parts.append(create_algo_html(algo))

    # Theorems
    for thm in theorems[:2]:
        parts.append(create_theorem_html(thm))

    # If no algorithms/theorems, extract key paragraphs
    if not algorithms and not theorems:
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 80]
        for p in paragraphs[:3]:
            parts.append(f'<p>{html.escape(p)}</p>')

    content = '\n'.join(parts) if parts else f'<p>{html.escape(text[:800])}</p>'

    # Analysis section
    analysis_items = []

    if algorithms:
        algo_summaries = ''.join([
            f'<li><strong>{html.escape(a["name"])}</strong>: {html.escape(ALGO_EXPLANATIONS.get(a["name"], {}).get("simple", "See details above"))}</li>'
            for a in algorithms[:3]
        ])
        analysis_items.append(f'''
<div class="analysis-item">
    <h5>Algorithms Summary</h5>
    <ul>{algo_summaries}</ul>
</div>''')

    if chapter and chapter in CHAPTER_INFO:
        info = CHAPTER_INFO[chapter]
        analysis_items.append(f'''
<div class="analysis-item">
    <h5>Chapter Context</h5>
    <p><strong>Chapter {chapter}: {html.escape(info["name"])}</strong></p>
    <p>{html.escape(info["summary"])}</p>
</div>''')

    if not analysis_items:
        analysis_items.append('''
<div class="analysis-item">
    <h5>Study Note</h5>
    <p>This page covers foundational material from CLRS. Take time to understand each concept before moving on.</p>
</div>''')

    analysis_html = '\n'.join(analysis_items)

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

def create_front_matter_page(page_num, text):
    """Create front matter pages."""
    pages = {
        1: {
            "title": "Introduction to Algorithms - Title Page",
            "content": '''<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Introduction to Algorithms</h1>
    <p style="color: var(--text-secondary); font-style: italic;">Third Edition</p>
</div>
<div class="original-content">
    <div class="definition-box">
        <h4>The Authors</h4>
        <ul>
            <li><strong>Thomas H. Cormen</strong> - Dartmouth College</li>
            <li><strong>Charles E. Leiserson</strong> - MIT</li>
            <li><strong>Ronald L. Rivest</strong> - MIT (the 'R' in RSA encryption)</li>
            <li><strong>Clifford Stein</strong> - Columbia University</li>
        </ul>
    </div>
    <p>This is <strong>CLRS</strong> - the most widely used algorithms textbook in computer science education worldwide.</p>
</div>
<div class="analysis-section">
    <h3>Why This Book Matters</h3>
    <div class="analysis-block">
        <div class="analysis-item">
            <h5>The Gold Standard</h5>
            <p>CLRS is considered the "bible" of algorithms. It's used in CS courses at universities worldwide and is essential for technical interviews.</p>
        </div>
        <div class="analysis-item">
            <h5>What You'll Learn</h5>
            <ul>
                <li>Algorithm design techniques (divide-and-conquer, DP, greedy)</li>
                <li>Data structures from basic to advanced</li>
                <li>Mathematical analysis of algorithms</li>
                <li>Graph algorithms, string matching, computational geometry</li>
                <li>NP-completeness and approximation algorithms</li>
            </ul>
        </div>
    </div>
</div>'''
        },
        2: {
            "title": "Half Title Page",
            "content": '''<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Introduction to Algorithms</h1>
</div>
<div class="original-content">
    <div class="highlight-box">
        <h4>Third Edition (2009)</h4>
        <p>This edition includes new chapters on van Emde Boas trees, multithreaded algorithms, and thoroughly revised material throughout.</p>
    </div>
</div>'''
        },
        3: {
            "title": "Blank Page",
            "content": '''<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Blank Page</h1>
</div>
<div class="original-content">
    <p><em>This page is intentionally blank in the printed edition.</em></p>
</div>'''
        },
        4: {
            "title": "Full Title Page",
            "content": '''<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Introduction to Algorithms, Third Edition</h1>
</div>
<div class="original-content">
    <div class="definition-box">
        <h4>Publication Details</h4>
        <p><strong>Publisher:</strong> The MIT Press<br>
        <strong>Location:</strong> Cambridge, Massachusetts & London, England</p>
    </div>
</div>'''
        },
        5: {
            "title": "Copyright Page",
            "content": '''<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Copyright Information</h1>
</div>
<div class="original-content">
    <div class="highlight-box">
        <h4>Publication Data</h4>
        <p><strong>ISBN (Hardcover):</strong> 978-0-262-03384-8<br>
        <strong>ISBN (Paperback):</strong> 978-0-262-53305-8<br>
        <strong>Copyright:</strong> © 2009 Massachusetts Institute of Technology</p>
    </div>
</div>
<div class="analysis-section">
    <h3>Quick Reference</h3>
    <div class="analysis-block">
        <div class="analysis-item">
            <h5>How to Cite</h5>
            <p>Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). <em>Introduction to Algorithms</em> (3rd ed.). MIT Press.</p>
        </div>
    </div>
</div>'''
        }
    }

    if page_num in pages:
        return {"page": page_num, **pages[page_num]}
    return None

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
