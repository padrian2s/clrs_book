#!/usr/bin/env python3
"""
Generate CLEAN explanations for ALL CLRS pages.
NO raw PDF text - only human-readable explanations.
"""

import json
import re
import html
from pathlib import Path

PAGES_DIR = Path("/Users/adrian/personal/clrs/clrs_pages")
OUTPUT_DIR = Path("/Users/adrian/personal/clrs/reader/data/pages")
MANIFEST_FILE = Path("/Users/adrian/personal/clrs/reader/data/manifest.json")

# ===================== PAGE CONTENT DATABASE =====================
# This contains clean explanations for specific pages and page ranges

SPECIFIC_PAGES = {
    1: {
        "title": "Title Page",
        "content": """<div class="article-header">
    <div class="section-label">Introduction to Algorithms</div>
    <h1>CLRS - The Algorithm Bible</h1>
    <p style="color: var(--text-secondary);">Third Edition by Cormen, Leiserson, Rivest, Stein</p>
</div>
<div class="original-content">
    <div class="definition-box">
        <h4>The Authors</h4>
        <ul>
            <li><strong>Thomas H. Cormen</strong> - Dartmouth College professor, lead author</li>
            <li><strong>Charles E. Leiserson</strong> - MIT professor, parallel computing expert</li>
            <li><strong>Ronald L. Rivest</strong> - MIT professor, the "R" in RSA encryption</li>
            <li><strong>Clifford Stein</strong> - Columbia professor, algorithm optimization</li>
        </ul>
    </div>
    <div class="highlight-box">
        <h4>Why This Book?</h4>
        <p>CLRS is THE standard textbook for algorithms courses worldwide. If you're preparing for:</p>
        <ul>
            <li>University CS courses</li>
            <li>Technical interviews (Google, Meta, Amazon, etc.)</li>
            <li>Competitive programming</li>
            <li>Graduate studies</li>
        </ul>
        <p>...this book covers everything you need.</p>
    </div>
</div>
<div class="analysis-section">
    <h3>How to Use This Book</h3>
    <div class="analysis-block">
        <div class="analysis-item">
            <h5>Recommended Path</h5>
            <ol>
                <li><strong>Chapters 1-3:</strong> Foundations - understand big-O notation</li>
                <li><strong>Chapters 4-9:</strong> Sorting - the classic algorithms</li>
                <li><strong>Chapters 10-14:</strong> Data structures</li>
                <li><strong>Chapters 15-16:</strong> Dynamic programming & greedy</li>
                <li><strong>Chapters 22-26:</strong> Graph algorithms</li>
            </ol>
        </div>
    </div>
</div>"""
    },

    2: {
        "title": "Half Title",
        "content": """<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Introduction to Algorithms</h1>
</div>
<div class="original-content">
    <div class="highlight-box">
        <h4>Third Edition - What's New</h4>
        <ul>
            <li>New chapter on <strong>van Emde Boas trees</strong></li>
            <li>New chapter on <strong>multithreaded algorithms</strong></li>
            <li>Revised and updated throughout</li>
            <li>More problems and exercises</li>
        </ul>
    </div>
</div>"""
    },

    3: {
        "title": "Blank Page",
        "content": """<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Intentionally Blank</h1>
</div>
<div class="original-content">
    <p><em>This page is blank in the printed book. Navigate to the next page.</em></p>
</div>"""
    },

    4: {
        "title": "Title Page (Full)",
        "content": """<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Introduction to Algorithms, Third Edition</h1>
</div>
<div class="original-content">
    <div class="definition-box">
        <h4>Publisher</h4>
        <p><strong>The MIT Press</strong><br>Cambridge, Massachusetts · London, England</p>
    </div>
    <p>MIT Press is one of the most respected publishers in computer science and technology.</p>
</div>"""
    },

    5: {
        "title": "Copyright",
        "content": """<div class="article-header">
    <div class="section-label">Front Matter</div>
    <h1>Copyright Information</h1>
</div>
<div class="original-content">
    <div class="highlight-box">
        <h4>Citation</h4>
        <p>Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). <em>Introduction to Algorithms</em> (3rd ed.). MIT Press.</p>
    </div>
    <p><strong>ISBN:</strong> 978-0-262-03384-8 (hardcover)<br>
    <strong>ISBN:</strong> 978-0-262-53305-8 (paperback)</p>
</div>"""
    },
}

# Table of Contents pages (6-15)
for i in range(6, 16):
    SPECIFIC_PAGES[i] = {
        "title": "Table of Contents",
        "content": f"""<div class="article-header">
    <div class="section-label">Navigation</div>
    <h1>Table of Contents (Page {i-5} of 10)</h1>
</div>
<div class="original-content">
    <div class="definition-box">
        <h4>Book Structure</h4>
        <p>CLRS is organized into <strong>8 parts</strong> with <strong>35 chapters</strong>:</p>
    </div>
    <div class="highlight-box">
        <h4>Part I: Foundations (Ch. 1-5)</h4>
        <p>Algorithm basics, asymptotic notation, divide-and-conquer</p>
    </div>
    <div class="highlight-box">
        <h4>Part II: Sorting (Ch. 6-9)</h4>
        <p>Heapsort, quicksort, linear-time sorting, selection</p>
    </div>
    <div class="highlight-box">
        <h4>Part III: Data Structures (Ch. 10-14)</h4>
        <p>Stacks, queues, hash tables, BSTs, red-black trees</p>
    </div>
    <div class="highlight-box">
        <h4>Part IV: Advanced Techniques (Ch. 15-17)</h4>
        <p>Dynamic programming, greedy algorithms, amortized analysis</p>
    </div>
    <p><em>Switch to image view (press V) to see the full table of contents.</em></p>
</div>"""
    }

# Preface pages (16-25)
for i in range(16, 26):
    SPECIFIC_PAGES[i] = {
        "title": "Preface",
        "content": f"""<div class="article-header">
    <div class="section-label">Preface</div>
    <h1>About This Book</h1>
</div>
<div class="original-content">
    <div class="definition-box">
        <h4>Who This Book Is For</h4>
        <ul>
            <li><strong>Students:</strong> Undergraduate/graduate CS algorithms courses</li>
            <li><strong>Professionals:</strong> Engineers preparing for technical interviews</li>
            <li><strong>Researchers:</strong> Reference for algorithm design and analysis</li>
        </ul>
    </div>
    <div class="highlight-box">
        <h4>Prerequisites</h4>
        <ul>
            <li>Basic programming experience</li>
            <li>High school math (algebra, basic calculus helps)</li>
            <li>Willingness to think mathematically</li>
        </ul>
    </div>
    <div class="figure-box">
        <h4>How to Study</h4>
        <ol>
            <li>Read the chapter introduction first</li>
            <li>Study the pseudocode carefully</li>
            <li>Work through examples by hand</li>
            <li>Do the exercises (starred ones are harder)</li>
        </ol>
    </div>
</div>"""
    }

# ===================== ALGORITHM EXPLANATIONS =====================
ALGORITHMS = {
    "INSERTION-SORT": {
        "name": "Insertion Sort",
        "simple": "Sort cards in your hand one at a time",
        "analogy": "Imagine sorting a hand of playing cards. You pick up one card at a time and insert it into its correct position among the cards you've already sorted.",
        "steps": [
            "Start with the second element (first is 'sorted')",
            "Compare current element with sorted elements to its left",
            "Shift larger elements right to make room",
            "Insert the element in its correct position",
            "Repeat for all remaining elements"
        ],
        "complexity": {
            "time_best": "O(n) - already sorted",
            "time_avg": "O(n²)",
            "time_worst": "O(n²) - reverse sorted",
            "space": "O(1) - in-place"
        },
        "when_to_use": [
            "Small arrays (< 50 elements)",
            "Nearly sorted data",
            "Online sorting (data arrives one at a time)",
            "Simple implementation needed"
        ],
        "when_not_to_use": [
            "Large unsorted arrays",
            "When O(n²) is too slow"
        ]
    },

    "MERGE-SORT": {
        "name": "Merge Sort",
        "simple": "Divide in half, sort each half, merge them",
        "analogy": "Split a deck of cards in half, sort each half separately, then merge them by always picking the smaller top card from each pile.",
        "steps": [
            "Divide array into two halves",
            "Recursively sort left half",
            "Recursively sort right half",
            "Merge the two sorted halves"
        ],
        "complexity": {
            "time_best": "O(n log n)",
            "time_avg": "O(n log n)",
            "time_worst": "O(n log n)",
            "space": "O(n) - needs extra array"
        },
        "when_to_use": [
            "Guaranteed O(n log n) needed",
            "Linked lists (no random access needed)",
            "External sorting (large files)",
            "Stable sort needed"
        ],
        "when_not_to_use": [
            "Memory is limited",
            "Small arrays (overhead not worth it)"
        ]
    },

    "QUICKSORT": {
        "name": "Quicksort",
        "simple": "Pick a pivot, put smaller left, larger right, repeat",
        "analogy": "Choose one person as the 'pivot'. Everyone shorter goes left, everyone taller goes right. Now repeat for each group.",
        "steps": [
            "Pick a pivot element (often last element)",
            "Partition: move smaller elements left, larger right",
            "Pivot is now in its final position",
            "Recursively sort left and right partitions"
        ],
        "complexity": {
            "time_best": "O(n log n)",
            "time_avg": "O(n log n)",
            "time_worst": "O(n²) - rare with good pivot",
            "space": "O(log n) - recursion stack"
        },
        "when_to_use": [
            "General-purpose sorting",
            "Average case matters most",
            "In-place sorting needed",
            "Cache efficiency important"
        ],
        "when_not_to_use": [
            "Guaranteed O(n log n) required",
            "Stable sort needed",
            "Already sorted data (unless randomized)"
        ]
    },

    "HEAPSORT": {
        "name": "Heapsort",
        "simple": "Build a heap, repeatedly extract the maximum",
        "analogy": "Build a pile where the biggest item is always on top. Keep removing the top item (the biggest) and rebuilding the pile.",
        "steps": [
            "Build a max-heap from the array",
            "Swap root (maximum) with last element",
            "Reduce heap size by 1",
            "Heapify the root",
            "Repeat until heap is empty"
        ],
        "complexity": {
            "time_best": "O(n log n)",
            "time_avg": "O(n log n)",
            "time_worst": "O(n log n)",
            "space": "O(1) - in-place"
        },
        "when_to_use": [
            "Guaranteed O(n log n) with O(1) space",
            "Priority queue operations needed too"
        ],
        "when_not_to_use": [
            "Stable sort needed",
            "Cache efficiency matters (bad locality)"
        ]
    },

    "COUNTING-SORT": {
        "name": "Counting Sort",
        "simple": "Count each value, then place them in order",
        "analogy": "Count how many of each score (0-100) students got. Then write down that many 0s, that many 1s, etc.",
        "steps": [
            "Create count array for range [0, k]",
            "Count occurrences of each element",
            "Compute cumulative sums",
            "Place elements in output array using counts"
        ],
        "complexity": {
            "time_best": "O(n + k)",
            "time_avg": "O(n + k)",
            "time_worst": "O(n + k)",
            "space": "O(n + k)"
        },
        "when_to_use": [
            "Integers in a known, small range",
            "k (range) is O(n)",
            "As subroutine in radix sort"
        ],
        "when_not_to_use": [
            "Large range of values",
            "Non-integer data"
        ]
    },

    "BFS": {
        "name": "Breadth-First Search",
        "simple": "Explore neighbors first, then neighbors' neighbors",
        "analogy": "Like ripples in a pond. Visit all nodes at distance 1, then all at distance 2, etc.",
        "steps": [
            "Start at source vertex, add to queue",
            "While queue not empty:",
            "  - Dequeue a vertex",
            "  - Visit all unvisited neighbors",
            "  - Add them to queue"
        ],
        "complexity": {
            "time": "O(V + E)",
            "space": "O(V) for queue"
        },
        "when_to_use": [
            "Shortest path in unweighted graph",
            "Level-order traversal",
            "Finding connected components",
            "Testing bipartiteness"
        ]
    },

    "DFS": {
        "name": "Depth-First Search",
        "simple": "Go as deep as possible, then backtrack",
        "analogy": "Exploring a maze by always taking the first path until you hit a dead end, then backtracking.",
        "steps": [
            "Start at source, mark as visited",
            "For each unvisited neighbor:",
            "  - Recursively DFS from that neighbor",
            "When all neighbors done, backtrack"
        ],
        "complexity": {
            "time": "O(V + E)",
            "space": "O(V) for recursion stack"
        },
        "when_to_use": [
            "Detecting cycles",
            "Topological sorting",
            "Finding strongly connected components",
            "Maze solving",
            "Pathfinding (not shortest)"
        ]
    },

    "DIJKSTRA": {
        "name": "Dijkstra's Algorithm",
        "simple": "Always expand the closest unvisited vertex",
        "analogy": "Finding the fastest route on a map by always exploring the closest city you haven't visited yet.",
        "steps": [
            "Set distance to source = 0, all others = ∞",
            "Add all vertices to priority queue",
            "While queue not empty:",
            "  - Extract vertex with minimum distance",
            "  - For each neighbor, if path through current is shorter, update"
        ],
        "complexity": {
            "time": "O((V + E) log V) with binary heap",
            "space": "O(V)"
        },
        "when_to_use": [
            "Shortest paths with non-negative weights",
            "GPS navigation",
            "Network routing"
        ],
        "when_not_to_use": [
            "Negative edge weights (use Bellman-Ford)"
        ]
    },

    "BELLMAN-FORD": {
        "name": "Bellman-Ford Algorithm",
        "simple": "Relax all edges V-1 times",
        "analogy": "Keep improving estimates of shortest distances by checking every road. After V-1 rounds, you've found the best.",
        "steps": [
            "Set distance to source = 0, all others = ∞",
            "Repeat V-1 times:",
            "  - For each edge (u,v), try to improve distance to v",
            "Check for negative cycles"
        ],
        "complexity": {
            "time": "O(VE)",
            "space": "O(V)"
        },
        "when_to_use": [
            "Graphs with negative edge weights",
            "Detecting negative cycles",
            "When Dijkstra doesn't work"
        ]
    },
}

# ===================== CHAPTER INFO =====================
CHAPTERS = {
    1: {
        "name": "The Role of Algorithms in Computing",
        "part": "I: Foundations",
        "summary": "What is an algorithm? Why do we care about efficiency?",
        "key_points": [
            "An algorithm is a well-defined procedure for solving a problem",
            "Algorithms are technology - like hardware, but for solving problems",
            "Efficiency matters: O(n) vs O(n²) can mean seconds vs years"
        ],
        "real_world": "Google Search returns results in milliseconds because of efficient algorithms"
    },
    2: {
        "name": "Getting Started",
        "part": "I: Foundations",
        "summary": "Your first algorithms: Insertion Sort and Merge Sort",
        "key_points": [
            "Loop invariants prove correctness",
            "Analyzing running time tells us how algorithm scales",
            "Divide-and-conquer: split problem, solve parts, combine"
        ],
        "real_world": "Sorting is fundamental - every spreadsheet, database, and file manager uses it"
    },
    3: {
        "name": "Growth of Functions",
        "part": "I: Foundations",
        "summary": "Big-O notation: the language of algorithm efficiency",
        "key_points": [
            "O(f(n)) means 'grows no faster than f(n)'",
            "Θ(f(n)) means 'grows exactly as fast as f(n)'",
            "Ω(f(n)) means 'grows at least as fast as f(n)'",
            "Focus on dominant terms as n → ∞"
        ],
        "real_world": "Helps predict if your code can handle 1 million users"
    },
    4: {
        "name": "Divide-and-Conquer",
        "part": "I: Foundations",
        "summary": "Break big problems into smaller ones",
        "key_points": [
            "Divide: Break problem into subproblems",
            "Conquer: Solve subproblems recursively",
            "Combine: Merge solutions",
            "Master theorem: T(n) = aT(n/b) + f(n)"
        ],
        "real_world": "Merge sort, quicksort, FFT, Strassen's matrix multiplication"
    },
    5: {
        "name": "Probabilistic Analysis and Randomized Algorithms",
        "part": "I: Foundations",
        "summary": "Using randomness to analyze and design algorithms",
        "key_points": [
            "Average-case vs worst-case analysis",
            "Randomized algorithms: add randomness for better expected performance",
            "Indicator random variables simplify probability calculations"
        ],
        "real_world": "Randomized quicksort, hash functions, Monte Carlo methods"
    },
    6: {
        "name": "Heapsort",
        "part": "II: Sorting",
        "summary": "Sorting using a clever tree structure called a heap",
        "key_points": [
            "Heap: complete binary tree with heap property",
            "Max-heap: parent ≥ children",
            "Heapify: fix one violation in O(log n)",
            "Build heap: surprisingly O(n), not O(n log n)"
        ],
        "real_world": "Priority queues for task scheduling, Dijkstra's algorithm"
    },
    7: {
        "name": "Quicksort",
        "part": "II: Sorting",
        "summary": "The fastest practical sorting algorithm",
        "key_points": [
            "Partition: put small elements left, large right",
            "Pivot choice matters: random is safest",
            "O(n log n) average, O(n²) worst (rare)",
            "In-place: only O(log n) extra space"
        ],
        "real_world": "Default sort in most programming languages"
    },
    8: {
        "name": "Sorting in Linear Time",
        "part": "II: Sorting",
        "summary": "Beating O(n log n) when we know more about our data",
        "key_points": [
            "Comparison sorts: Ω(n log n) lower bound",
            "Counting sort: O(n+k) for integers in [0,k]",
            "Radix sort: O(d(n+k)) for d-digit numbers",
            "Bucket sort: O(n) average for uniform data"
        ],
        "real_world": "Sorting integers, dates, fixed-length strings"
    },
    9: {
        "name": "Medians and Order Statistics",
        "part": "II: Sorting",
        "summary": "Finding the k-th smallest element without sorting",
        "key_points": [
            "Selection: find k-th smallest",
            "Randomized select: O(n) expected",
            "Median of medians: O(n) worst-case guaranteed",
            "No need to fully sort!"
        ],
        "real_world": "Finding median salary, percentiles, database TOP-K queries"
    },
    10: {
        "name": "Elementary Data Structures",
        "part": "III: Data Structures",
        "summary": "The building blocks: stacks, queues, linked lists",
        "key_points": [
            "Stack: Last-In-First-Out (LIFO)",
            "Queue: First-In-First-Out (FIFO)",
            "Linked list: dynamic, O(1) insert/delete",
            "Arrays vs linked lists trade-offs"
        ],
        "real_world": "Undo button (stack), print queue (queue), browser history"
    },
    11: {
        "name": "Hash Tables",
        "part": "III: Data Structures",
        "summary": "O(1) average lookup - the most practical data structure",
        "key_points": [
            "Hash function maps key → index",
            "Collisions: chaining or open addressing",
            "Load factor affects performance",
            "O(1) average for insert/search/delete"
        ],
        "real_world": "Python dictionaries, JavaScript objects, database indexes"
    },
    12: {
        "name": "Binary Search Trees",
        "part": "III: Data Structures",
        "summary": "A tree that maintains sorted order",
        "key_points": [
            "BST property: left < node < right",
            "Search/insert/delete: O(h) where h = height",
            "Balanced: h = O(log n)",
            "Unbalanced: h = O(n) worst case"
        ],
        "real_world": "Databases, file systems, auto-complete"
    },
    13: {
        "name": "Red-Black Trees",
        "part": "III: Data Structures",
        "summary": "Self-balancing BST with guaranteed O(log n)",
        "key_points": [
            "Each node is red or black",
            "5 properties ensure balance",
            "Height ≤ 2 log(n+1)",
            "Insert/delete: O(log n) worst case"
        ],
        "real_world": "Java TreeMap, C++ std::map, Linux kernel"
    },
    14: {
        "name": "Augmenting Data Structures",
        "part": "III: Data Structures",
        "summary": "Extending data structures for new operations",
        "key_points": [
            "Add extra info to each node",
            "Maintain info during updates",
            "Order-statistic trees: find k-th element",
            "Interval trees: find overlapping intervals"
        ],
        "real_world": "Range queries, interval scheduling"
    },
    15: {
        "name": "Dynamic Programming",
        "part": "IV: Advanced Techniques",
        "summary": "Solving problems with overlapping subproblems",
        "key_points": [
            "Optimal substructure: optimal solution contains optimal subsolutions",
            "Overlapping subproblems: same subproblems solved repeatedly",
            "Memoization (top-down) or tabulation (bottom-up)",
            "Think: What's the last decision? What subproblems remain?"
        ],
        "real_world": "Shortest paths, sequence alignment, resource allocation"
    },
    16: {
        "name": "Greedy Algorithms",
        "part": "IV: Advanced Techniques",
        "summary": "Making locally optimal choices for global optimum",
        "key_points": [
            "Greedy choice property: local best → global best",
            "Never reconsider choices",
            "Simpler than DP when it works",
            "Doesn't always work - need proof!"
        ],
        "real_world": "Huffman coding, MST algorithms, activity scheduling"
    },
    17: {
        "name": "Amortized Analysis",
        "part": "IV: Advanced Techniques",
        "summary": "Average cost over a sequence of operations",
        "key_points": [
            "Aggregate: total cost / number of operations",
            "Accounting: charge extra for cheap ops, use credit for expensive",
            "Potential: define potential function",
            "Different from average-case (no probability)"
        ],
        "real_world": "Dynamic arrays, splay trees, union-find"
    },
    18: {
        "name": "B-Trees",
        "part": "V: Advanced Data Structures",
        "summary": "Trees optimized for disk access",
        "key_points": [
            "High branching factor (many children per node)",
            "Minimizes disk reads",
            "All leaves at same depth",
            "B+ trees: data only in leaves"
        ],
        "real_world": "Databases, file systems - your data is probably in a B-tree"
    },
    19: {
        "name": "Fibonacci Heaps",
        "part": "V: Advanced Data Structures",
        "summary": "Heap with O(1) amortized insert and decrease-key",
        "key_points": [
            "Lazy operations: delay work until necessary",
            "Insert: O(1) amortized",
            "Decrease-key: O(1) amortized",
            "Extract-min: O(log n) amortized"
        ],
        "real_world": "Faster Dijkstra and Prim for sparse graphs"
    },
    20: {
        "name": "van Emde Boas Trees",
        "part": "V: Advanced Data Structures",
        "summary": "O(log log U) operations for integers in [0, U)",
        "key_points": [
            "Exploits fixed universe size U",
            "Recursive structure with √U clusters",
            "Much faster than BST for bounded integers",
            "Space: O(U)"
        ],
        "real_world": "Very fast priority queues for integer keys"
    },
    21: {
        "name": "Data Structures for Disjoint Sets",
        "part": "V: Advanced Data Structures",
        "summary": "Track which elements belong to which groups",
        "key_points": [
            "Make-Set: create singleton set",
            "Union: merge two sets",
            "Find-Set: which set contains element?",
            "Union by rank + path compression: nearly O(1)"
        ],
        "real_world": "Kruskal's MST, connected components, image segmentation"
    },
    22: {
        "name": "Elementary Graph Algorithms",
        "part": "VI: Graph Algorithms",
        "summary": "BFS and DFS - foundation of all graph algorithms",
        "key_points": [
            "Graph representations: adjacency list vs matrix",
            "BFS: level by level, shortest paths (unweighted)",
            "DFS: go deep, then backtrack",
            "Applications: topological sort, SCC, cycle detection"
        ],
        "real_world": "Social networks, web crawlers, GPS navigation"
    },
    23: {
        "name": "Minimum Spanning Trees",
        "part": "VI: Graph Algorithms",
        "summary": "Connect all vertices with minimum total edge weight",
        "key_points": [
            "MST: tree that spans all vertices, minimum total weight",
            "Cut property: lightest edge crossing a cut is safe",
            "Kruskal: sort edges, add if no cycle",
            "Prim: grow tree from one vertex"
        ],
        "real_world": "Network design, clustering, circuit design"
    },
    24: {
        "name": "Single-Source Shortest Paths",
        "part": "VI: Graph Algorithms",
        "summary": "Finding shortest paths from one source",
        "key_points": [
            "Relaxation: can we improve distance via this edge?",
            "Dijkstra: non-negative weights, O((V+E) log V)",
            "Bellman-Ford: handles negative weights, O(VE)",
            "DAG: topological order, O(V+E)"
        ],
        "real_world": "GPS, network routing (OSPF, RIP)"
    },
    25: {
        "name": "All-Pairs Shortest Paths",
        "part": "VI: Graph Algorithms",
        "summary": "Shortest paths between ALL pairs of vertices",
        "key_points": [
            "Floyd-Warshall: O(V³) DP, handles negative weights",
            "Johnson: O(V² log V + VE), better for sparse graphs",
            "Transitive closure: is there a path from u to v?"
        ],
        "real_world": "Traffic analysis, network analysis"
    },
    26: {
        "name": "Maximum Flow",
        "part": "VI: Graph Algorithms",
        "summary": "How much can flow through a network?",
        "key_points": [
            "Flow network: source, sink, capacities",
            "Ford-Fulkerson: find augmenting paths",
            "Max-flow = min-cut theorem",
            "Bipartite matching is a special case"
        ],
        "real_world": "Transportation, bipartite matching, image segmentation"
    },
    27: {
        "name": "Multithreaded Algorithms",
        "part": "VII: Selected Topics",
        "summary": "Parallel algorithms for multi-core processors",
        "key_points": [
            "Spawn: create parallel task",
            "Sync: wait for spawned tasks",
            "Work: total operations (serial time)",
            "Span: critical path (parallel time)"
        ],
        "real_world": "Modern CPUs have many cores - parallelism is essential"
    },
    28: {
        "name": "Matrix Operations",
        "part": "VII: Selected Topics",
        "summary": "Solving linear equations, inverting matrices",
        "key_points": [
            "LU decomposition: factor A = LU",
            "Forward/back substitution",
            "Matrix inversion: O(n³)",
            "Least squares: best fit solution"
        ],
        "real_world": "Scientific computing, graphics, machine learning"
    },
    29: {
        "name": "Linear Programming",
        "part": "VII: Selected Topics",
        "summary": "Optimize linear function subject to linear constraints",
        "key_points": [
            "Standard form: maximize cᵀx subject to Ax ≤ b, x ≥ 0",
            "Simplex algorithm: walk along edges of polytope",
            "Duality: every LP has a dual LP",
            "Polynomial-time algorithms exist (not simplex)"
        ],
        "real_world": "Resource allocation, scheduling, logistics"
    },
    30: {
        "name": "Polynomials and the FFT",
        "part": "VII: Selected Topics",
        "summary": "Fast Fourier Transform - O(n log n) polynomial multiplication",
        "key_points": [
            "Polynomial multiplication: O(n²) naively",
            "FFT: O(n log n) via divide-and-conquer",
            "DFT: evaluates polynomial at roots of unity",
            "Inverse FFT: interpolate back to coefficients"
        ],
        "real_world": "Signal processing, audio, image compression"
    },
    31: {
        "name": "Number-Theoretic Algorithms",
        "part": "VII: Selected Topics",
        "summary": "Algorithms for integers: GCD, modular arithmetic, RSA",
        "key_points": [
            "Euclidean algorithm: GCD in O(log n)",
            "Modular exponentiation: a^b mod n",
            "RSA: public-key cryptography",
            "Primality testing: Miller-Rabin"
        ],
        "real_world": "Cryptography - HTTPS, digital signatures"
    },
    32: {
        "name": "String Matching",
        "part": "VII: Selected Topics",
        "summary": "Finding a pattern within a text",
        "key_points": [
            "Naive: O(nm) - try each position",
            "Rabin-Karp: hashing, O(n+m) expected",
            "KMP: O(n+m) worst case, no backtracking",
            "Automata: precompute all transitions"
        ],
        "real_world": "Text editors, grep, DNA analysis, plagiarism detection"
    },
    33: {
        "name": "Computational Geometry",
        "part": "VII: Selected Topics",
        "summary": "Algorithms for geometric problems",
        "key_points": [
            "Cross product: left/right of a line",
            "Line segment intersection",
            "Convex hull: Graham scan, Jarvis march",
            "Closest pair: O(n log n) divide-and-conquer"
        ],
        "real_world": "Computer graphics, robotics, GIS, game collision"
    },
    34: {
        "name": "NP-Completeness",
        "part": "VII: Selected Topics",
        "summary": "Some problems are (probably) inherently hard",
        "key_points": [
            "P: solvable in polynomial time",
            "NP: verifiable in polynomial time",
            "NP-complete: hardest problems in NP",
            "P = NP? The million-dollar question"
        ],
        "real_world": "Know what's hard → don't waste time on impossible solutions"
    },
    35: {
        "name": "Approximation Algorithms",
        "part": "VII: Selected Topics",
        "summary": "Good-enough solutions for hard problems",
        "key_points": [
            "When optimal is too hard, settle for 'close enough'",
            "Approximation ratio: how close to optimal?",
            "Vertex cover: 2-approximation",
            "TSP: 2-approximation for metric"
        ],
        "real_world": "Delivery routing, scheduling, resource allocation"
    },
}

# ===================== MATH CONCEPTS =====================
MATH_CONCEPTS = {
    "floor_ceiling": {
        "title": "Floor and Ceiling Functions",
        "content": """<div class="definition-box">
    <h4>Floor ⌊x⌋</h4>
    <p><strong>Definition:</strong> Largest integer ≤ x (round DOWN)</p>
    <ul>
        <li>⌊3.7⌋ = 3</li>
        <li>⌊5.0⌋ = 5</li>
        <li>⌊-2.3⌋ = -3 (not -2!)</li>
    </ul>
</div>
<div class="definition-box">
    <h4>Ceiling ⌈x⌉</h4>
    <p><strong>Definition:</strong> Smallest integer ≥ x (round UP)</p>
    <ul>
        <li>⌈3.2⌉ = 4</li>
        <li>⌈5.0⌉ = 5</li>
        <li>⌈-2.7⌉ = -2 (not -3!)</li>
    </ul>
</div>
<div class="highlight-box">
    <h4>Why It Matters</h4>
    <p>Used constantly in algorithms:</p>
    <ul>
        <li><strong>Array splitting:</strong> ⌊n/2⌋ and ⌈n/2⌉ elements</li>
        <li><strong>Loop iterations:</strong> ⌈n/k⌉ iterations to process n items k at a time</li>
        <li><strong>Tree height:</strong> ⌊log n⌋ for binary trees</li>
    </ul>
</div>"""
    },

    "modular": {
        "title": "Modular Arithmetic",
        "content": """<div class="definition-box">
    <h4>The Modulo Operation</h4>
    <p><strong>a mod n</strong> = remainder when a is divided by n</p>
    <ul>
        <li>17 mod 5 = 2 (because 17 = 3×5 + 2)</li>
        <li>10 mod 3 = 1</li>
        <li>12 mod 4 = 0</li>
    </ul>
</div>
<div class="definition-box">
    <h4>Congruence</h4>
    <p><strong>a ≡ b (mod n)</strong> means a and b have the same remainder when divided by n</p>
    <ul>
        <li>17 ≡ 2 (mod 5) ✓</li>
        <li>17 ≡ 7 (mod 5) ✓</li>
        <li>17 ≡ 22 (mod 5) ✓</li>
    </ul>
</div>
<div class="highlight-box">
    <h4>Why It Matters</h4>
    <ul>
        <li><strong>Hash tables:</strong> index = hash(key) mod table_size</li>
        <li><strong>Cryptography:</strong> RSA uses modular exponentiation</li>
        <li><strong>Circular arrays:</strong> next_index = (i + 1) mod n</li>
    </ul>
</div>"""
    },

    "logarithms": {
        "title": "Logarithms",
        "content": """<div class="definition-box">
    <h4>What is log?</h4>
    <p><strong>log₂(n)</strong> = "how many times do I divide n by 2 to get 1?"</p>
    <ul>
        <li>log₂(8) = 3 (because 8 → 4 → 2 → 1)</li>
        <li>log₂(16) = 4</li>
        <li>log₂(1024) = 10</li>
    </ul>
</div>
<div class="highlight-box">
    <h4>Why Logs Appear Everywhere</h4>
    <ul>
        <li><strong>Binary search:</strong> O(log n) - halve search space each step</li>
        <li><strong>Balanced trees:</strong> height = O(log n)</li>
        <li><strong>Divide-and-conquer:</strong> log n levels of recursion</li>
    </ul>
</div>
<div class="figure-box">
    <h4>Log Rules (for reference)</h4>
    <ul>
        <li>log(ab) = log(a) + log(b)</li>
        <li>log(a/b) = log(a) - log(b)</li>
        <li>log(aⁿ) = n·log(a)</li>
        <li>logₐ(n) = logᵦ(n) / logᵦ(a) (change of base)</li>
    </ul>
</div>"""
    },

    "summations": {
        "title": "Summations",
        "content": """<div class="definition-box">
    <h4>Common Summation Formulas</h4>
    <ul>
        <li><strong>1 + 2 + 3 + ... + n = n(n+1)/2</strong> = O(n²)</li>
        <li><strong>1 + 2 + 4 + ... + 2ⁿ = 2ⁿ⁺¹ - 1</strong> = O(2ⁿ)</li>
        <li><strong>1 + 1/2 + 1/4 + ... → 2</strong> (geometric series)</li>
    </ul>
</div>
<div class="highlight-box">
    <h4>Why It Matters</h4>
    <p>Analyzing loops often requires summations:</p>
    <ul>
        <li><strong>Nested loops:</strong> Σᵢ Σⱼ 1 = n²</li>
        <li><strong>Insertion sort inner loop:</strong> Σᵢ₌₁ⁿ i = O(n²)</li>
        <li><strong>Geometric series:</strong> explains why build-heap is O(n)</li>
    </ul>
</div>"""
    },

    "recurrences": {
        "title": "Recurrence Relations",
        "content": """<div class="definition-box">
    <h4>What is a Recurrence?</h4>
    <p>An equation that defines T(n) in terms of T(smaller values)</p>
    <p><strong>Example:</strong> T(n) = 2T(n/2) + n</p>
</div>
<div class="highlight-box">
    <h4>Master Theorem (Quick Reference)</h4>
    <p>For T(n) = aT(n/b) + f(n):</p>
    <ul>
        <li>If f(n) < nˡᵒᵍᵇᵃ: T(n) = Θ(nˡᵒᵍᵇᵃ)</li>
        <li>If f(n) = nˡᵒᵍᵇᵃ: T(n) = Θ(nˡᵒᵍᵇᵃ log n)</li>
        <li>If f(n) > nˡᵒᵍᵇᵃ: T(n) = Θ(f(n))</li>
    </ul>
</div>
<div class="figure-box">
    <h4>Common Recurrences</h4>
    <ul>
        <li><strong>T(n) = T(n/2) + O(1):</strong> Binary search → O(log n)</li>
        <li><strong>T(n) = 2T(n/2) + O(n):</strong> Merge sort → O(n log n)</li>
        <li><strong>T(n) = 2T(n/2) + O(1):</strong> Tree traversal → O(n)</li>
    </ul>
</div>"""
    },

    "big_o": {
        "title": "Big-O Notation",
        "content": """<div class="definition-box">
    <h4>What is Big-O?</h4>
    <p><strong>O(f(n))</strong> means "grows no faster than f(n)" as n → ∞</p>
    <p>We ignore constants and lower-order terms.</p>
</div>
<div class="highlight-box">
    <h4>Common Complexities (fastest to slowest)</h4>
    <ol>
        <li><strong>O(1)</strong> - Constant: array access, hash table lookup</li>
        <li><strong>O(log n)</strong> - Logarithmic: binary search</li>
        <li><strong>O(n)</strong> - Linear: simple loop through array</li>
        <li><strong>O(n log n)</strong> - Linearithmic: merge sort, quicksort</li>
        <li><strong>O(n²)</strong> - Quadratic: nested loops, insertion sort</li>
        <li><strong>O(2ⁿ)</strong> - Exponential: brute force subset problems</li>
        <li><strong>O(n!)</strong> - Factorial: brute force permutations</li>
    </ol>
</div>
<div class="figure-box">
    <h4>Practical Impact</h4>
    <table style="width:100%;border-collapse:collapse;margin-top:10px;">
        <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">n</th><th style="padding:8px;border:1px solid #ddd">O(n)</th><th style="padding:8px;border:1px solid #ddd">O(n²)</th><th style="padding:8px;border:1px solid #ddd">O(2ⁿ)</th></tr>
        <tr><td style="padding:8px;border:1px solid #ddd">10</td><td style="padding:8px;border:1px solid #ddd">10</td><td style="padding:8px;border:1px solid #ddd">100</td><td style="padding:8px;border:1px solid #ddd">1,024</td></tr>
        <tr><td style="padding:8px;border:1px solid #ddd">100</td><td style="padding:8px;border:1px solid #ddd">100</td><td style="padding:8px;border:1px solid #ddd">10,000</td><td style="padding:8px;border:1px solid #ddd">10³⁰</td></tr>
        <tr><td style="padding:8px;border:1px solid #ddd">1000</td><td style="padding:8px;border:1px solid #ddd">1,000</td><td style="padding:8px;border:1px solid #ddd">1,000,000</td><td style="padding:8px;border:1px solid #ddd">∞</td></tr>
    </table>
</div>"""
    },
}

# ===================== HELPER FUNCTIONS =====================

def clean_text(text):
    """Clean raw PDF text."""
    text = text.replace('\f', '')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def detect_chapter(text):
    """Detect chapter number from text."""
    match = re.search(r'Chapter\s+(\d+)', text[:500])
    if match:
        return int(match.group(1))
    match = re.search(r'^(\d+)\.[\d]+', text, re.MULTILINE)
    if match:
        return int(match.group(1))
    return None

def detect_section(text):
    """Detect section number and title."""
    match = re.search(r'^(\d+\.\d+)\s+([A-Za-z][A-Za-z\s\-,]+)', text, re.MULTILINE)
    if match:
        return match.group(1), match.group(2).strip()
    return None, None

def detect_page_type(text, page_num):
    """Determine what type of content is on this page."""
    text_lower = text.lower()

    if page_num <= 5:
        return "front_matter"
    if page_num <= 15 and "contents" in text_lower[:200]:
        return "toc"
    if page_num <= 25 and "preface" in text_lower[:200]:
        return "preface"
    if page_num > 1250:
        return "back_matter"
    if re.search(r'^\d+\.\d+-\d+', text, re.MULTILINE):
        return "exercises"
    if re.search(r'^Problems?\s*$', text, re.MULTILINE | re.IGNORECASE):
        return "problems"

    # Check for specific math topics
    if "floor" in text_lower and "ceiling" in text_lower:
        return "math_floor_ceiling"
    if "modular" in text_lower and "mod" in text_lower:
        return "math_modular"
    if "logarithm" in text_lower or "log n" in text_lower:
        return "math_log"

    return "content"

def detect_algorithm(text):
    """Detect algorithm names in the text."""
    detected = []
    for algo_key in ALGORITHMS.keys():
        # Create pattern for spaced version like "I NSERTION -S ORT"
        spaced = ' '.join(algo_key)
        if algo_key.replace('-', ' ').upper() in text.upper() or spaced.replace('-', ' - ') in text:
            detected.append(algo_key)
    return detected

def create_algorithm_content(algo_key):
    """Create beautiful explanation for an algorithm."""
    algo = ALGORITHMS[algo_key]

    steps_html = '\n'.join([f'<li>{html.escape(s)}</li>' for s in algo.get('steps', [])])
    when_html = '\n'.join([f'<li>{html.escape(s)}</li>' for s in algo.get('when_to_use', [])])

    comp = algo.get('complexity', {})
    comp_html = ''
    if comp:
        comp_items = []
        for k, v in comp.items():
            label = k.replace('_', ' ').title()
            comp_items.append(f'<li><strong>{label}:</strong> {html.escape(v)}</li>')
        comp_html = f'<ul>{"".join(comp_items)}</ul>'

    return f"""<div class="definition-box">
    <h4>{html.escape(algo['name'])}</h4>
    <p><strong>{html.escape(algo['simple'])}</strong></p>
    <p><em>{html.escape(algo.get('analogy', ''))}</em></p>
</div>
<div class="highlight-box">
    <h4>How It Works</h4>
    <ol>{steps_html}</ol>
</div>
<div class="figure-box">
    <h4>Complexity</h4>
    {comp_html}
</div>
<div class="highlight-box">
    <h4>When to Use</h4>
    <ul>{when_html}</ul>
</div>"""

def create_chapter_content(chapter_num):
    """Create chapter overview content."""
    if chapter_num not in CHAPTERS:
        return None

    ch = CHAPTERS[chapter_num]
    points_html = '\n'.join([f'<li>{html.escape(p)}</li>' for p in ch['key_points']])

    return f"""<div class="definition-box">
    <h4>{html.escape(ch['part'])}</h4>
    <h3>Chapter {chapter_num}: {html.escape(ch['name'])}</h3>
    <p><em>{html.escape(ch['summary'])}</em></p>
</div>
<div class="highlight-box">
    <h4>Key Points</h4>
    <ul>{points_html}</ul>
</div>
<div class="figure-box">
    <h4>Real-World Applications</h4>
    <p>{html.escape(ch['real_world'])}</p>
</div>"""

def process_page(page_num):
    """Process a single page and generate clean explanation."""

    # Check for specific page content first
    if page_num in SPECIFIC_PAGES:
        return {
            "page": page_num,
            "title": SPECIFIC_PAGES[page_num]["title"],
            "content": SPECIFIC_PAGES[page_num]["content"]
        }

    # Read the raw text
    txt_file = PAGES_DIR / f"page-{page_num:04d}.txt"
    if not txt_file.exists():
        return None

    with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
        raw_text = f.read()

    text = clean_text(raw_text)

    # Detect page characteristics
    page_type = detect_page_type(text, page_num)
    chapter = detect_chapter(text)
    section_num, section_title = detect_section(text)
    algos = detect_algorithm(text)

    # Build content based on what we found
    parts = []

    # Check for math concepts
    if page_type == "math_floor_ceiling":
        return {
            "page": page_num,
            "title": "Floor and Ceiling Functions",
            "content": f"""<div class="article-header">
    <div class="section-label">Mathematical Foundations</div>
    <h1>Floor and Ceiling Functions</h1>
</div>
<div class="original-content">
    {MATH_CONCEPTS['floor_ceiling']['content']}
</div>"""
        }

    if page_type == "math_modular":
        return {
            "page": page_num,
            "title": "Modular Arithmetic",
            "content": f"""<div class="article-header">
    <div class="section-label">Mathematical Foundations</div>
    <h1>Modular Arithmetic</h1>
</div>
<div class="original-content">
    {MATH_CONCEPTS['modular']['content']}
</div>"""
        }

    # Handle exercises
    if page_type == "exercises":
        return {
            "page": page_num,
            "title": f"Exercises {section_num}" if section_num else "Exercises",
            "content": f"""<div class="article-header">
    <div class="section-label">Practice Problems</div>
    <h1>Exercises</h1>
</div>
<div class="original-content">
    <div class="highlight-box">
        <h4>Why Exercises Matter</h4>
        <p>You can't learn algorithms by just reading. Working through problems is how knowledge becomes skill.</p>
    </div>
    <div class="definition-box">
        <h4>Tips for Problem Solving</h4>
        <ol>
            <li>Make sure you understand the problem completely</li>
            <li>Work through small examples by hand first</li>
            <li>Think about edge cases</li>
            <li>Analyze your solution's complexity</li>
            <li>Check your answer - does it make sense?</li>
        </ol>
    </div>
    <p><em>See image view for the actual problems.</em></p>
</div>"""
        }

    # Handle algorithms
    if algos:
        for algo in algos[:2]:  # Max 2 algorithms per page
            parts.append(create_algorithm_content(algo))

    # Handle chapter start
    elif chapter and "Chapter" in text[:200]:
        ch_content = create_chapter_content(chapter)
        if ch_content:
            parts.append(ch_content)

    # Generate title
    if section_num:
        label = f"Section {section_num}"
        title = f"{section_num} {section_title}" if section_title else f"Section {section_num}"
    elif chapter:
        label = f"Chapter {chapter}"
        title = CHAPTERS.get(chapter, {}).get('name', f'Chapter {chapter}')
    else:
        label = f"Page {page_num}"
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l) > 5]
        title = lines[0][:60] if lines else f"Page {page_num}"

    # If we have content, use it; otherwise provide a default
    if parts:
        content = '\n'.join(parts)
    else:
        # Default content for pages we haven't specially handled
        content = f"""<div class="highlight-box">
    <h4>Page Content</h4>
    <p>This page contains detailed technical content. Use the image view (press <kbd>V</kbd>) to see the original material with all formulas and figures.</p>
</div>"""

        if chapter and chapter in CHAPTERS:
            ch = CHAPTERS[chapter]
            content += f"""<div class="definition-box">
    <h4>Context: Chapter {chapter}</h4>
    <p><strong>{html.escape(ch['name'])}</strong></p>
    <p>{html.escape(ch['summary'])}</p>
</div>"""

    return {
        "page": page_num,
        "title": title,
        "content": f"""<div class="article-header">
    <div class="section-label">{html.escape(label)}</div>
    <h1>{html.escape(title)}</h1>
</div>
<div class="original-content">
    {content}
</div>"""
    }

def main():
    """Process all pages."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_pages = []

    for page_num in range(1, 1314):
        data = process_page(page_num)
        if data:
            with open(OUTPUT_DIR / f"page-{page_num:04d}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            manifest_pages.append({
                "page": page_num,
                "title": data["title"],
                "hasContent": True
            })

        if page_num % 100 == 0:
            print(f"{page_num}/1313...")

    # Write manifest
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
