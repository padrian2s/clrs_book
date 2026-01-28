#!/usr/bin/env python3
"""
Batch generate detailed explanations for ALL CLRS pages.
Each page gets full, rich content - not one-liners.
"""

import json
import re
import html
from pathlib import Path

PAGES_DIR = Path("/Users/adrian/personal/clrs/clrs_pages")
OUTPUT_DIR = Path("/Users/adrian/personal/clrs/reader/data/pages")
MANIFEST_FILE = Path("/Users/adrian/personal/clrs/reader/data/manifest.json")

# ============ FULL TABLE OF CONTENTS ============
TOC = """
PART I: FOUNDATIONS
  1. The Role of Algorithms in Computing (p.5)
     1.1 Algorithms - What is an algorithm? The sorting problem
     1.2 Algorithms as a technology - Efficiency matters

  2. Getting Started (p.16)
     2.1 Insertion sort - Your first algorithm
     2.2 Analyzing algorithms - How to measure performance
     2.3 Designing algorithms - Divide-and-conquer, merge sort

  3. Growth of Functions (p.43)
     3.1 Asymptotic notation - O, Θ, Ω explained
     3.2 Standard notations - Floors, ceilings, logs, factorials

  4. Divide-and-Conquer (p.65)
     4.1 Maximum-subarray problem
     4.2 Strassen's matrix multiplication
     4.3-4.5 Solving recurrences - Substitution, recursion trees, master method

  5. Probabilistic Analysis (p.114)
     5.1 The hiring problem
     5.2 Indicator random variables
     5.3 Randomized algorithms

PART II: SORTING AND ORDER STATISTICS
  6. Heapsort (p.151)
     6.1 Heaps - The heap data structure
     6.2 Maintaining heap property - MAX-HEAPIFY
     6.3 Building a heap - BUILD-MAX-HEAP
     6.4 Heapsort algorithm
     6.5 Priority queues

  7. Quicksort (p.170)
     7.1 Description - PARTITION and QUICKSORT
     7.2 Performance analysis
     7.3 Randomized quicksort
     7.4 Analysis of quicksort

  8. Sorting in Linear Time (p.191)
     8.1 Lower bounds - Ω(n lg n) for comparison sorts
     8.2 Counting sort
     8.3 Radix sort
     8.4 Bucket sort

  9. Medians and Order Statistics (p.213)
     9.1 Minimum and maximum
     9.2 Selection in expected linear time
     9.3 Selection in worst-case linear time

PART III: DATA STRUCTURES
  10. Elementary Data Structures (p.232)
      10.1 Stacks and queues
      10.2 Linked lists
      10.3 Implementing pointers and objects
      10.4 Representing rooted trees

  11. Hash Tables (p.253)
      11.1 Direct-address tables
      11.2 Hash tables - Chaining
      11.3 Hash functions
      11.4 Open addressing

  12. Binary Search Trees (p.286)
      12.1 What is a BST?
      12.2 Querying - Search, Min, Max, Successor
      12.3 Insertion and deletion

  13. Red-Black Trees (p.308)
      13.1 Properties of red-black trees
      13.2 Rotations
      13.3 Insertion
      13.4 Deletion

  14. Augmenting Data Structures (p.339)
      14.1 Dynamic order statistics
      14.2 How to augment a data structure
      14.3 Interval trees

PART IV: ADVANCED DESIGN AND ANALYSIS TECHNIQUES
  15. Dynamic Programming (p.359)
      15.1 Rod cutting
      15.2 Matrix-chain multiplication
      15.3 Elements of DP - Optimal substructure, overlapping subproblems
      15.4 Longest common subsequence
      15.5 Optimal binary search trees

  16. Greedy Algorithms (p.414)
      16.1 Activity-selection problem
      16.2 Elements of greedy strategy
      16.3 Huffman codes

  17. Amortized Analysis (p.451)
      17.1 Aggregate analysis
      17.2 Accounting method
      17.3 Potential method
      17.4 Dynamic tables

PART V: ADVANCED DATA STRUCTURES
  18. B-Trees (p.484)
  19. Fibonacci Heaps (p.505)
  20. van Emde Boas Trees (p.531)
  21. Data Structures for Disjoint Sets (p.561)

PART VI: GRAPH ALGORITHMS
  22. Elementary Graph Algorithms (p.589)
      22.1 Representations - Adjacency list vs matrix
      22.2 Breadth-first search (BFS)
      22.3 Depth-first search (DFS)
      22.4 Topological sort
      22.5 Strongly connected components

  23. Minimum Spanning Trees (p.624)
      23.1 Growing a MST
      23.2 Kruskal and Prim algorithms

  24. Single-Source Shortest Paths (p.643)
      24.1 Bellman-Ford algorithm
      24.2 Shortest paths in DAGs
      24.3 Dijkstra's algorithm

  25. All-Pairs Shortest Paths (p.684)
      25.1 Matrix multiplication method
      25.2 Floyd-Warshall algorithm
      25.3 Johnson's algorithm

  26. Maximum Flow (p.708)
      26.1 Flow networks
      26.2 Ford-Fulkerson method
      26.3 Maximum bipartite matching

PART VII: SELECTED TOPICS
  27. Multithreaded Algorithms (p.772)
  28. Matrix Operations (p.813)
  29. Linear Programming (p.843)
  30. Polynomials and the FFT (p.898)
  31. Number-Theoretic Algorithms (p.926)
  32. String Matching (p.985)
  33. Computational Geometry (p.1014)
  34. NP-Completeness (p.1048)
  35. Approximation Algorithms (p.1106)

PART VIII: APPENDIX
  A. Summations (p.1145)
  B. Sets, Relations, Functions, Graphs, Trees (p.1158)
  C. Counting and Probability (p.1183)
  D. Matrices (p.1217)
"""

# ============ DETAILED SECTION EXPLANATIONS ============
SECTIONS = {
    # Chapter 1
    "1.1": {
        "title": "Algorithms",
        "summary": "What exactly is an algorithm? A step-by-step procedure for solving a problem.",
        "key_points": [
            "An algorithm is a well-defined computational procedure",
            "Takes input, produces output",
            "Must be correct (solve the problem) and efficient (use reasonable resources)",
            "Sorting is used as the main example throughout the book"
        ],
        "example": "Sorting: Input = sequence of numbers, Output = sorted sequence. Many algorithms exist: insertion sort, merge sort, quicksort, etc.",
        "why_matters": "Algorithms are the foundation of all computer programs. Better algorithms = faster programs."
    },
    "1.2": {
        "title": "Algorithms as a Technology",
        "summary": "Algorithms are as important as hardware. A good algorithm on slow hardware beats a bad algorithm on fast hardware.",
        "key_points": [
            "Efficiency matters: O(n²) vs O(n log n) is the difference between seconds and years",
            "Hardware gets faster, but better algorithms provide bigger speedups",
            "Example: sorting 10 million numbers - insertion sort (5.5 hours) vs merge sort (17 minutes)"
        ],
        "example": "Computer A (10 billion ops/sec) with O(n²) algorithm vs Computer B (10 million ops/sec) with O(n log n). For n=10 million, B wins!",
        "why_matters": "Choosing the right algorithm can make impossible problems solvable."
    },
    # Chapter 2
    "2.1": {
        "title": "Insertion Sort",
        "summary": "Sort by inserting each element into its correct position in the already-sorted portion.",
        "key_points": [
            "Like sorting playing cards in your hand",
            "Start with second element, insert into sorted portion to the left",
            "Shift larger elements right to make room",
            "Time: O(n²) worst/average, O(n) best (already sorted)",
            "Space: O(1) - in-place"
        ],
        "pseudocode": """for j = 2 to n:
    key = A[j]
    i = j - 1
    while i > 0 and A[i] > key:
        A[i+1] = A[i]
        i = i - 1
    A[i+1] = key""",
        "example": "Sorting [5,2,4,6,1,3]: After each iteration: [2,5,4,6,1,3] → [2,4,5,6,1,3] → [2,4,5,6,1,3] → [1,2,4,5,6,3] → [1,2,3,4,5,6]",
        "why_matters": "Simple, efficient for small arrays, good for nearly-sorted data."
    },
    "2.2": {
        "title": "Analyzing Algorithms",
        "summary": "How to measure algorithm performance: count operations as a function of input size.",
        "key_points": [
            "Running time = number of primitive operations executed",
            "Focus on worst-case (guarantees), sometimes average-case",
            "Express time as T(n) where n = input size",
            "Ignore constants, focus on growth rate",
            "Insertion sort: T(n) = c₁n² + c₂n + c₃ ≈ O(n²)"
        ],
        "example": "Insertion sort inner loop runs at most j-1 times for element j. Total: 1+2+3+...+(n-1) = n(n-1)/2 = O(n²)",
        "why_matters": "Analysis lets us predict performance and compare algorithms before implementing."
    },
    "2.3": {
        "title": "Designing Algorithms",
        "summary": "Divide-and-conquer: break problem into subproblems, solve recursively, combine solutions.",
        "key_points": [
            "Divide: split problem into smaller instances",
            "Conquer: solve subproblems recursively",
            "Combine: merge solutions into final answer",
            "Merge sort: divide in half, sort each, merge",
            "Merge sort time: T(n) = 2T(n/2) + O(n) = O(n log n)"
        ],
        "pseudocode": """MERGE-SORT(A, p, r):
    if p < r:
        q = (p + r) / 2
        MERGE-SORT(A, p, q)
        MERGE-SORT(A, q+1, r)
        MERGE(A, p, q, r)""",
        "example": "Sorting [5,2,4,7,1,3,2,6]: Split into [5,2,4,7] and [1,3,2,6], sort each, merge into [1,2,2,3,4,5,6,7]",
        "why_matters": "Divide-and-conquer is a powerful paradigm used in quicksort, FFT, Strassen's algorithm, and many more."
    },
    # Chapter 3
    "3.1": {
        "title": "Asymptotic Notation",
        "summary": "Mathematical notation for describing algorithm growth rates: O, Θ, Ω, o, ω.",
        "key_points": [
            "O(g(n)): grows at most as fast as g(n) - upper bound",
            "Ω(g(n)): grows at least as fast as g(n) - lower bound",
            "Θ(g(n)): grows exactly as fast as g(n) - tight bound",
            "o(g(n)): grows strictly slower than g(n)",
            "ω(g(n)): grows strictly faster than g(n)"
        ],
        "example": "2n² + 3n + 1 = Θ(n²) because it's both O(n²) and Ω(n²). The constants (2, 3, 1) don't matter for large n.",
        "why_matters": "Asymptotic notation lets us compare algorithms independent of hardware or implementation details."
    },
    "3.2": {
        "title": "Standard Notations and Common Functions",
        "summary": "Mathematical building blocks: floors, ceilings, logs, factorials, and their properties.",
        "key_points": [
            "Floor ⌊x⌋: largest integer ≤ x (round down)",
            "Ceiling ⌈x⌉: smallest integer ≥ x (round up)",
            "log₂ n: how many times divide n by 2 to get 1",
            "n! = n × (n-1) × ... × 1 (grows faster than exponential)",
            "Stirling: n! ≈ √(2πn)(n/e)ⁿ"
        ],
        "example": "⌊3.7⌋ = 3, ⌈3.2⌉ = 4, log₂(8) = 3, 5! = 120",
        "why_matters": "These functions appear everywhere in algorithm analysis."
    },
    # Chapter 6
    "6.1": {
        "title": "Heaps",
        "summary": "A heap is a nearly complete binary tree stored in an array with the heap property.",
        "key_points": [
            "Max-heap: every parent ≥ its children",
            "Min-heap: every parent ≤ its children",
            "Height = ⌊log n⌋",
            "Array representation: parent(i) = ⌊i/2⌋, left(i) = 2i, right(i) = 2i+1",
            "Root (maximum) is always at index 1"
        ],
        "example": "Array [16,14,10,8,7,9,3,2,4,1] represents a max-heap tree with 16 at root.",
        "why_matters": "Heaps enable O(log n) priority queue operations and O(n log n) sorting."
    },
    "6.2": {
        "title": "Maintaining the Heap Property",
        "summary": "MAX-HEAPIFY fixes a single violation by floating an element down.",
        "key_points": [
            "Assumes left and right subtrees are valid max-heaps",
            "If root violates, swap with larger child",
            "Repeat down the tree until fixed",
            "Time: O(log n) - proportional to height"
        ],
        "pseudocode": """MAX-HEAPIFY(A, i):
    l = LEFT(i), r = RIGHT(i)
    largest = i
    if l ≤ heap-size and A[l] > A[i]: largest = l
    if r ≤ heap-size and A[r] > A[largest]: largest = r
    if largest ≠ i:
        swap A[i] and A[largest]
        MAX-HEAPIFY(A, largest)""",
        "why_matters": "Core operation for heap insert, extract-max, and heapsort."
    },
    "6.3": {
        "title": "Building a Heap",
        "summary": "Convert an unsorted array into a max-heap in O(n) time.",
        "key_points": [
            "Start from last non-leaf node, heapify each going up",
            "Leaves (n/2+1 to n) are already valid heaps",
            "Time: O(n), not O(n log n)!",
            "Why O(n)? Most nodes are near leaves where heapify is fast"
        ],
        "pseudocode": """BUILD-MAX-HEAP(A):
    heap-size = n
    for i = ⌊n/2⌋ downto 1:
        MAX-HEAPIFY(A, i)""",
        "why_matters": "Enables heapsort and efficient priority queue construction."
    },
    "6.4": {
        "title": "The Heapsort Algorithm",
        "summary": "Sort by building a heap, then repeatedly extracting the maximum.",
        "key_points": [
            "Build max-heap from input array",
            "Swap root (max) with last element",
            "Reduce heap size, heapify the root",
            "Repeat until sorted",
            "Time: O(n log n), Space: O(1)"
        ],
        "pseudocode": """HEAPSORT(A):
    BUILD-MAX-HEAP(A)
    for i = n downto 2:
        swap A[1] and A[i]
        heap-size = heap-size - 1
        MAX-HEAPIFY(A, 1)""",
        "why_matters": "In-place O(n log n) sorting with guaranteed worst-case performance."
    },
    "6.5": {
        "title": "Priority Queues",
        "summary": "A data structure for maintaining a set with priority-based extraction.",
        "key_points": [
            "Operations: INSERT, MAXIMUM, EXTRACT-MAX, INCREASE-KEY",
            "MAXIMUM: O(1) - just return root",
            "EXTRACT-MAX: O(log n) - remove root, heapify",
            "INSERT: O(log n) - add at end, bubble up",
            "INCREASE-KEY: O(log n) - update key, bubble up"
        ],
        "example": "Task scheduler: tasks with priorities, always run highest priority next.",
        "why_matters": "Used in Dijkstra's algorithm, Huffman coding, event simulation."
    },
    # Chapter 7
    "7.1": {
        "title": "Description of Quicksort",
        "summary": "Divide-and-conquer sorting: partition around a pivot, recursively sort partitions.",
        "key_points": [
            "PARTITION: rearrange so elements < pivot are left, > pivot are right",
            "Pivot ends up in its final sorted position",
            "Recursively sort left and right partitions",
            "Average: O(n log n), Worst: O(n²)"
        ],
        "pseudocode": """QUICKSORT(A, p, r):
    if p < r:
        q = PARTITION(A, p, r)
        QUICKSORT(A, p, q-1)
        QUICKSORT(A, q+1, r)

PARTITION(A, p, r):
    x = A[r]  # pivot
    i = p - 1
    for j = p to r-1:
        if A[j] ≤ x:
            i = i + 1
            swap A[i] and A[j]
    swap A[i+1] and A[r]
    return i + 1""",
        "why_matters": "Fastest practical sorting algorithm for most data."
    },
    "7.2": {
        "title": "Performance of Quicksort",
        "summary": "Quicksort's performance depends on how balanced the partitions are.",
        "key_points": [
            "Worst case O(n²): already sorted, always unbalanced",
            "Best case O(n log n): perfect splits every time",
            "Average case O(n log n): even slightly unbalanced splits are fine",
            "Even 99-1 splits give O(n log n)!"
        ],
        "example": "Worst: [1,2,3,4,5] with last element as pivot → partitions of size n-1 and 0 each time.",
        "why_matters": "Understanding performance helps choose when to use quicksort."
    },
    "7.3": {
        "title": "A Randomized Version of Quicksort",
        "summary": "Randomize pivot selection to avoid worst-case on any specific input.",
        "key_points": [
            "Pick pivot randomly instead of always using last element",
            "Expected time O(n log n) for ANY input",
            "No adversary can construct worst-case input",
            "Simple change: swap random element with A[r] before partition"
        ],
        "pseudocode": """RANDOMIZED-PARTITION(A, p, r):
    i = RANDOM(p, r)
    swap A[i] and A[r]
    return PARTITION(A, p, r)""",
        "why_matters": "Makes quicksort robust against adversarial inputs."
    },
    # Chapter 15
    "15.1": {
        "title": "Rod Cutting",
        "summary": "Given a rod of length n and prices for each length, find the maximum revenue from cutting.",
        "key_points": [
            "Optimal substructure: best cut = some first piece + best cut of remainder",
            "Overlapping subproblems: same subproblems solved repeatedly",
            "Naive recursion: O(2ⁿ)",
            "Memoization (top-down): O(n²)",
            "Bottom-up DP: O(n²)"
        ],
        "pseudocode": """BOTTOM-UP-CUT-ROD(p, n):
    r[0] = 0
    for j = 1 to n:
        q = -∞
        for i = 1 to j:
            q = max(q, p[i] + r[j-i])
        r[j] = q
    return r[n]""",
        "example": "Rod of length 4, prices [1,5,8,9]. Best: cut into 2+2 for revenue 5+5=10.",
        "why_matters": "Classic DP problem that illustrates the technique clearly."
    },
    "15.2": {
        "title": "Matrix-Chain Multiplication",
        "summary": "Find the optimal way to parenthesize a chain of matrix multiplications.",
        "key_points": [
            "Order matters! (A·B)·C vs A·(B·C) can have very different costs",
            "Goal: minimize total scalar multiplications",
            "DP: m[i,j] = min cost to multiply matrices i through j",
            "Try all split points k: m[i,j] = min(m[i,k] + m[k+1,j] + cost of final multiply)",
            "Time: O(n³), Space: O(n²)"
        ],
        "example": "Matrices with dimensions 10×100, 100×5, 5×50. ((A·B)·C) costs 7500, (A·(B·C)) costs 75000!",
        "why_matters": "Shows how DP finds optimal structure among exponentially many options."
    },
    "15.3": {
        "title": "Elements of Dynamic Programming",
        "summary": "When to use DP: optimal substructure + overlapping subproblems.",
        "key_points": [
            "Optimal substructure: optimal solution contains optimal solutions to subproblems",
            "Overlapping subproblems: same subproblems solved many times",
            "Memoization: top-down recursion with caching",
            "Tabulation: bottom-up, fill table in dependency order",
            "Reconstruct solution by storing choices"
        ],
        "example": "Fibonacci: fib(5) = fib(4) + fib(3), and both fib(4) and fib(3) need fib(2).",
        "why_matters": "Recognizing DP problems is a key interview skill."
    },
    "15.4": {
        "title": "Longest Common Subsequence",
        "summary": "Find the longest subsequence common to two sequences.",
        "key_points": [
            "Subsequence: not necessarily contiguous, but in order",
            "DP: c[i,j] = LCS length for first i chars of X and first j chars of Y",
            "If X[i] = Y[j]: c[i,j] = c[i-1,j-1] + 1",
            "Else: c[i,j] = max(c[i-1,j], c[i,j-1])",
            "Time: O(mn), Space: O(mn) or O(min(m,n))"
        ],
        "example": "X = 'ABCBDAB', Y = 'BDCABA'. LCS = 'BCBA' (length 4).",
        "why_matters": "Used in diff tools, DNA sequence alignment, version control."
    },
    # Chapter 22
    "22.1": {
        "title": "Representations of Graphs",
        "summary": "Two ways to represent graphs: adjacency lists and adjacency matrices.",
        "key_points": [
            "Adjacency list: array of linked lists, one per vertex",
            "Adjacency matrix: n×n matrix, M[i,j] = 1 if edge (i,j) exists",
            "List space: O(V + E), good for sparse graphs",
            "Matrix space: O(V²), good for dense graphs",
            "List: O(degree) to check edge. Matrix: O(1) to check edge"
        ],
        "example": "Graph with 4 vertices, 5 edges. List uses ~9 entries. Matrix uses 16 entries.",
        "why_matters": "Choosing the right representation affects algorithm performance."
    },
    "22.2": {
        "title": "Breadth-First Search",
        "summary": "Explore graph level by level from a source vertex.",
        "key_points": [
            "Use a queue: visit vertex, enqueue unvisited neighbors",
            "Discovers shortest paths (fewest edges) from source",
            "Colors: white (undiscovered), gray (discovered), black (finished)",
            "Time: O(V + E) - each vertex and edge examined once",
            "Produces BFS tree of shortest-path distances"
        ],
        "pseudocode": """BFS(G, s):
    for each vertex u: color[u] = WHITE, d[u] = ∞
    color[s] = GRAY, d[s] = 0
    Q = {s}
    while Q not empty:
        u = DEQUEUE(Q)
        for each v in Adj[u]:
            if color[v] == WHITE:
                color[v] = GRAY
                d[v] = d[u] + 1
                ENQUEUE(Q, v)
        color[u] = BLACK""",
        "why_matters": "Foundation for shortest paths in unweighted graphs, level-order traversal."
    },
    "22.3": {
        "title": "Depth-First Search",
        "summary": "Explore as deep as possible before backtracking.",
        "key_points": [
            "Use recursion (or explicit stack)",
            "Discovery time d[v] and finish time f[v]",
            "Edge classification: tree, back, forward, cross edges",
            "Back edge ⟺ cycle exists",
            "Time: O(V + E)"
        ],
        "pseudocode": """DFS(G):
    for each vertex u: color[u] = WHITE
    time = 0
    for each vertex u:
        if color[u] == WHITE:
            DFS-VISIT(G, u)

DFS-VISIT(G, u):
    time = time + 1
    d[u] = time
    color[u] = GRAY
    for each v in Adj[u]:
        if color[v] == WHITE:
            DFS-VISIT(G, v)
    color[u] = BLACK
    time = time + 1
    f[u] = time""",
        "why_matters": "Foundation for topological sort, SCC, cycle detection."
    },
    "22.4": {
        "title": "Topological Sort",
        "summary": "Linear ordering of vertices such that all edges go forward.",
        "key_points": [
            "Only for directed acyclic graphs (DAGs)",
            "If edge (u,v), then u appears before v in ordering",
            "Algorithm: DFS, prepend vertex to list when finished",
            "Time: O(V + E)",
            "Alternative: repeatedly remove vertices with no incoming edges"
        ],
        "example": "Course prerequisites: must take CS101 before CS201, CS201 before CS301. Topological sort gives valid course order.",
        "why_matters": "Scheduling tasks with dependencies, build systems, spreadsheet evaluation."
    },
    # Chapter 24
    "24.1": {
        "title": "The Bellman-Ford Algorithm",
        "summary": "Single-source shortest paths that handles negative edge weights.",
        "key_points": [
            "Relax all edges V-1 times",
            "Relaxation: if d[v] > d[u] + w(u,v), update d[v]",
            "After V-1 iterations, all shortest paths found",
            "One more iteration: if any edge relaxes, negative cycle exists",
            "Time: O(VE)"
        ],
        "pseudocode": """BELLMAN-FORD(G, w, s):
    INITIALIZE-SINGLE-SOURCE(G, s)
    for i = 1 to |V| - 1:
        for each edge (u,v) in E:
            RELAX(u, v, w)
    for each edge (u,v) in E:
        if d[v] > d[u] + w(u,v):
            return FALSE  # negative cycle
    return TRUE""",
        "why_matters": "Works with negative weights, detects negative cycles."
    },
    "24.3": {
        "title": "Dijkstra's Algorithm",
        "summary": "Single-source shortest paths for non-negative edge weights.",
        "key_points": [
            "Greedy: always process vertex with smallest distance estimate",
            "Use priority queue (min-heap) for efficiency",
            "Once vertex is processed, its distance is final",
            "Time: O((V + E) log V) with binary heap",
            "Does NOT work with negative edge weights"
        ],
        "pseudocode": """DIJKSTRA(G, w, s):
    INITIALIZE-SINGLE-SOURCE(G, s)
    S = ∅
    Q = V  # min-priority queue by d values
    while Q not empty:
        u = EXTRACT-MIN(Q)
        S = S ∪ {u}
        for each v in Adj[u]:
            RELAX(u, v, w)""",
        "example": "GPS navigation: find shortest route from current location to destination.",
        "why_matters": "Fastest algorithm for shortest paths with non-negative weights."
    },
    # Chapter 4
    "4.1": {
        "title": "The Maximum-Subarray Problem",
        "summary": "Find the contiguous subarray with the largest sum.",
        "key_points": [
            "Divide-and-conquer approach: split array in half",
            "Maximum subarray is in left half, right half, or crosses the midpoint",
            "Finding crossing subarray is O(n)",
            "Recurrence: T(n) = 2T(n/2) + O(n) = O(n log n)",
            "There's also an O(n) solution (Kadane's algorithm)"
        ],
        "pseudocode": """FIND-MAX-CROSSING-SUBARRAY(A, low, mid, high):
    left-sum = -∞
    sum = 0
    for i = mid downto low:
        sum = sum + A[i]
        if sum > left-sum:
            left-sum = sum
            max-left = i
    # Similar for right side
    return (max-left, max-right, left-sum + right-sum)""",
        "example": "Array [-2,1,-3,4,-1,2,1,-5,4]. Max subarray is [4,-1,2,1] with sum 6.",
        "why_matters": "Classic divide-and-conquer problem, useful for stock trading (buy low, sell high)."
    },
    "4.2": {
        "title": "Strassen's Algorithm for Matrix Multiplication",
        "summary": "Multiply two n×n matrices faster than O(n³) using divide-and-conquer.",
        "key_points": [
            "Standard matrix multiplication: O(n³)",
            "Divide each matrix into four n/2 × n/2 submatrices",
            "Naive divide-and-conquer: 8 multiplications → still O(n³)",
            "Strassen's key insight: 7 multiplications suffice!",
            "Time: T(n) = 7T(n/2) + O(n²) = O(n^2.81)"
        ],
        "example": "For large matrices (n > 32), Strassen beats standard multiplication. Not used for small matrices due to overhead.",
        "why_matters": "Shows that seemingly optimal algorithms can sometimes be improved with clever math."
    },
    "4.3": {
        "title": "The Substitution Method for Solving Recurrences",
        "summary": "Guess the solution, then prove it correct by induction.",
        "key_points": [
            "Step 1: Guess the form of the solution",
            "Step 2: Use induction to prove the guess is correct",
            "Step 3: Solve for constants",
            "Common technique: guess based on recursion tree",
            "Subtlety: sometimes need to subtract lower-order terms"
        ],
        "example": "T(n) = 2T(n/2) + n. Guess: T(n) = O(n log n). Prove: T(n) ≤ cn log n for some c.",
        "why_matters": "Powerful technique when you have intuition about the answer."
    },
    "4.4": {
        "title": "The Recursion-Tree Method",
        "summary": "Visualize recurrence as a tree to sum up the total work.",
        "key_points": [
            "Each node represents cost of a subproblem",
            "Sum costs at each level, then sum all levels",
            "Root = original problem, leaves = base cases",
            "Tree depth = number of levels of recursion",
            "Good for developing intuition and guessing for substitution"
        ],
        "example": "T(n) = 3T(n/4) + cn². Level i has 3^i nodes, each with cost c(n/4^i)². Total work converges to O(n²).",
        "why_matters": "Visual approach makes complex recurrences tractable."
    },
    "4.5": {
        "title": "The Master Method",
        "summary": "A cookbook method for solving recurrences of the form T(n) = aT(n/b) + f(n).",
        "key_points": [
            "Compare f(n) with n^(log_b a)",
            "Case 1: f(n) = O(n^(log_b a - ε)) → T(n) = Θ(n^(log_b a))",
            "Case 2: f(n) = Θ(n^(log_b a)) → T(n) = Θ(n^(log_b a) log n)",
            "Case 3: f(n) = Ω(n^(log_b a + ε)) → T(n) = Θ(f(n))",
            "Most common divide-and-conquer recurrences fall into these cases"
        ],
        "example": "T(n) = 9T(n/3) + n. Here a=9, b=3, n^(log_3 9) = n². Since n = O(n^(2-ε)), Case 1: T(n) = Θ(n²).",
        "why_matters": "Quick way to solve most divide-and-conquer recurrences without detailed analysis."
    },
    # Chapter 5
    "5.1": {
        "title": "The Hiring Problem",
        "summary": "A model problem for analyzing randomized algorithms.",
        "key_points": [
            "Interview candidates, hire if better than current best",
            "Hiring cost >> interview cost",
            "Worst case: candidates arrive in increasing order → hire everyone",
            "Best case: best candidate first → hire once",
            "Average case: hire O(log n) candidates (assuming random order)"
        ],
        "example": "Interview 10 candidates. If they arrive randomly, expect to hire about ln(10) + 1 ≈ 3 people.",
        "why_matters": "Introduces probabilistic analysis and randomized algorithms."
    },
    "5.2": {
        "title": "Indicator Random Variables",
        "summary": "A simple but powerful technique for computing expected values.",
        "key_points": [
            "Indicator I{A} = 1 if event A occurs, 0 otherwise",
            "E[I{A}] = Pr{A} (expected value equals probability!)",
            "Key insight: E[X + Y] = E[X] + E[Y], even if X and Y are dependent",
            "Use indicators to break complex counting into simple events",
            "Avoid complex probability calculations"
        ],
        "example": "Expected number of heads in n coin flips. X = X₁ + X₂ + ... + Xₙ where Xᵢ = 1 if flip i is heads. E[X] = n/2.",
        "why_matters": "Makes many probabilistic analyses surprisingly simple."
    },
    "5.3": {
        "title": "Randomized Algorithms",
        "summary": "Algorithms that make random choices during execution.",
        "key_points": [
            "No adversary can construct worst-case input",
            "Permuting input randomly: RANDOMIZE-IN-PLACE",
            "Expected running time vs average-case running time",
            "Monte Carlo: always fast, probably correct",
            "Las Vegas: always correct, probably fast"
        ],
        "pseudocode": """RANDOMIZE-IN-PLACE(A):
    n = A.length
    for i = 1 to n:
        swap A[i] with A[RANDOM(i, n)]""",
        "example": "Randomized quicksort: O(n log n) expected time for ANY input.",
        "why_matters": "Randomization can make algorithms simpler and more robust."
    },
    # Chapter 8
    "8.1": {
        "title": "Lower Bounds for Sorting",
        "summary": "Comparison-based sorting cannot be faster than Ω(n log n).",
        "key_points": [
            "Any comparison sort can be viewed as a decision tree",
            "n! possible orderings → tree needs n! leaves",
            "Height h ≥ log(n!) = Ω(n log n)",
            "Therefore: worst-case comparisons ≥ Ω(n log n)",
            "Merge sort and heapsort are asymptotically optimal!"
        ],
        "example": "Sorting 3 elements requires at least ⌈log(3!)⌉ = ⌈log 6⌉ = 3 comparisons.",
        "why_matters": "Proves we can't do better with comparisons alone. Need different model to beat n log n."
    },
    "8.2": {
        "title": "Counting Sort",
        "summary": "Sort integers in O(n + k) time where k is the range of values.",
        "key_points": [
            "Not comparison-based → can beat Ω(n log n)",
            "Count occurrences of each value",
            "Compute cumulative counts (positions)",
            "Place each element at its correct position",
            "Stable: equal elements maintain relative order"
        ],
        "pseudocode": """COUNTING-SORT(A, B, k):
    let C[0..k] be new array of zeros
    for j = 1 to n:
        C[A[j]] = C[A[j]] + 1
    for i = 1 to k:
        C[i] = C[i] + C[i-1]
    for j = n downto 1:
        B[C[A[j]]] = A[j]
        C[A[j]] = C[A[j]] - 1""",
        "example": "Sort [4,1,3,4,3]: counts=[0,1,0,2,2], cumulative=[0,1,1,3,5]. Output: [1,3,3,4,4].",
        "why_matters": "Linear time sorting when values have bounded range. Building block for radix sort."
    },
    "8.3": {
        "title": "Radix Sort",
        "summary": "Sort numbers digit by digit, from least significant to most significant.",
        "key_points": [
            "Sort by least significant digit first using stable sort",
            "Then by next digit, and so on",
            "Must use stable sort (counting sort works well)",
            "Time: O(d(n + k)) where d = digits, k = base",
            "For n d-digit numbers: O(dn) if k = O(n)"
        ],
        "pseudocode": """RADIX-SORT(A, d):
    for i = 1 to d:
        use stable sort to sort A on digit i""",
        "example": "Sort [329, 457, 657, 839, 436, 720, 355]. By ones: [720,355,436,457,657,329,839]. By tens: ... By hundreds: sorted!",
        "why_matters": "Linear time for fixed-width integers. Used in practice for specific applications."
    },
    "8.4": {
        "title": "Bucket Sort",
        "summary": "Sort uniformly distributed numbers by distributing into buckets.",
        "key_points": [
            "Assume input uniformly distributed in [0, 1)",
            "Create n buckets, put each element in bucket ⌊n·x⌋",
            "Sort each bucket (insertion sort works since buckets are small)",
            "Concatenate all buckets",
            "Expected time: O(n) for uniform distribution"
        ],
        "pseudocode": """BUCKET-SORT(A):
    n = A.length
    let B[0..n-1] be new array of empty lists
    for i = 1 to n:
        insert A[i] into list B[⌊n·A[i]⌋]
    for i = 0 to n-1:
        sort list B[i] with insertion sort
    concatenate lists B[0], B[1], ..., B[n-1]""",
        "example": "Sort [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68] with 10 buckets.",
        "why_matters": "O(n) expected time when input is uniformly distributed."
    },
    # Chapter 9
    "9.1": {
        "title": "Minimum and Maximum",
        "summary": "Find min or max in n-1 comparisons; find both in 3⌊n/2⌋ comparisons.",
        "key_points": [
            "Finding min: n-1 comparisons (compare each to current min)",
            "Finding max: also n-1 comparisons",
            "Finding both naively: 2(n-1) comparisons",
            "Better: compare pairs first, then min with mins, max with maxes",
            "This gives 3⌊n/2⌋ comparisons total"
        ],
        "example": "Array of 8 elements: 4 pairwise comparisons, 3 to find min of losers, 3 to find max of winners = 10 total (vs 14 naive).",
        "why_matters": "Shows careful algorithm design can reduce constant factors."
    },
    "9.2": {
        "title": "Selection in Expected Linear Time",
        "summary": "Find the i-th smallest element in expected O(n) time using randomized partition.",
        "key_points": [
            "Like quicksort, but only recurse on one side",
            "RANDOMIZED-SELECT: pick random pivot, partition",
            "If pivot is i-th element, done!",
            "Else recurse on appropriate side",
            "Expected time: O(n), worst case: O(n²)"
        ],
        "pseudocode": """RANDOMIZED-SELECT(A, p, r, i):
    if p == r: return A[p]
    q = RANDOMIZED-PARTITION(A, p, r)
    k = q - p + 1
    if i == k: return A[q]
    elif i < k: return RANDOMIZED-SELECT(A, p, q-1, i)
    else: return RANDOMIZED-SELECT(A, q+1, r, i-k)""",
        "example": "Find 3rd smallest in [7,10,4,3,20,15]. After partition around pivot 15: [7,10,4,3,15,20]. 3rd is in left side.",
        "why_matters": "Finding medians and percentiles without fully sorting."
    },
    "9.3": {
        "title": "Selection in Worst-Case Linear Time",
        "summary": "The MEDIAN-OF-MEDIANS algorithm guarantees O(n) worst-case selection.",
        "key_points": [
            "Divide into groups of 5, find median of each group",
            "Recursively find median of medians",
            "Use median of medians as pivot → guaranteed good split",
            "At least 3n/10 elements smaller AND 3n/10 larger",
            "Recurrence: T(n) ≤ T(n/5) + T(7n/10) + O(n) = O(n)"
        ],
        "example": "25 elements: 5 groups of 5, find 5 medians, find median of those 5. Use as pivot for guaranteed balanced partition.",
        "why_matters": "Proves selection can be done in linear time, though randomized is faster in practice."
    },
    # Chapter 10
    "10.1": {
        "title": "Stacks and Queues",
        "summary": "Basic data structures with restricted access patterns.",
        "key_points": [
            "Stack: LIFO (Last-In-First-Out) - PUSH and POP",
            "Queue: FIFO (First-In-First-Out) - ENQUEUE and DEQUEUE",
            "Both can be implemented with arrays or linked lists",
            "All operations O(1)",
            "Stack: function calls, undo, parsing. Queue: BFS, scheduling"
        ],
        "pseudocode": """PUSH(S, x):
    S.top = S.top + 1
    S[S.top] = x

POP(S):
    if S.top == 0: error "underflow"
    S.top = S.top - 1
    return S[S.top + 1]""",
        "example": "Stack for expression evaluation: push operands, pop two when operator seen, push result.",
        "why_matters": "Fundamental building blocks used in countless algorithms."
    },
    "10.2": {
        "title": "Linked Lists",
        "summary": "Elements connected by pointers, supporting efficient insertion/deletion.",
        "key_points": [
            "Each element has key and next pointer (and prev for doubly-linked)",
            "Search: O(n) - must traverse from head",
            "Insert/Delete at known position: O(1) with pointer manipulation",
            "Singly-linked: next only. Doubly-linked: next and prev",
            "Circular: tail points to head"
        ],
        "pseudocode": """LIST-INSERT(L, x):
    x.next = L.head
    if L.head ≠ NIL:
        L.head.prev = x
    L.head = x
    x.prev = NIL

LIST-DELETE(L, x):
    if x.prev ≠ NIL:
        x.prev.next = x.next
    else: L.head = x.next
    if x.next ≠ NIL:
        x.next.prev = x.prev""",
        "why_matters": "When frequent insertions/deletions needed without reallocation."
    },
    "10.3": {
        "title": "Implementing Pointers and Objects",
        "summary": "How to implement linked structures in languages without pointers.",
        "key_points": [
            "Multiple-array representation: separate arrays for key, next, prev",
            "Single-array representation: pack all fields into one array",
            "Free list: linked list of available slots",
            "Allocate: remove from free list. Free: add to free list",
            "Useful for embedded systems, some languages"
        ],
        "example": "Arrays key[1..n], next[1..n], prev[1..n]. Element at index 4 has key[4], next[4], prev[4].",
        "why_matters": "Understanding pointers at a low level, implementing in constrained environments."
    },
    "10.4": {
        "title": "Representing Rooted Trees",
        "summary": "Different ways to store tree structures in memory.",
        "key_points": [
            "Binary trees: left, right, parent pointers",
            "Unbounded branching: left-child, right-sibling representation",
            "Each node has: parent, left-child, right-sibling",
            "Children form a linked list via right-sibling",
            "Compact: only 3 pointers regardless of number of children"
        ],
        "example": "Node with 5 children: left-child points to first child, that child's right-sibling points to second child, etc.",
        "why_matters": "Foundation for tree-based data structures throughout the book."
    },
    # Chapter 11
    "11.1": {
        "title": "Direct-Address Tables",
        "summary": "The simplest dictionary: use key directly as array index.",
        "key_points": [
            "Array T[0..m-1] where m = size of key universe",
            "T[k] holds element with key k (or NIL if empty)",
            "INSERT, DELETE, SEARCH all O(1)",
            "Problem: universe might be huge (e.g., all possible strings)",
            "Wastes space if actual keys are sparse"
        ],
        "example": "Keys 0-999: array of 1000 slots. T[42] = element with key 42.",
        "why_matters": "Conceptual foundation for hash tables."
    },
    "11.2": {
        "title": "Hash Tables",
        "summary": "Map large key universe to small table using hash function.",
        "key_points": [
            "Hash function h: U → {0, 1, ..., m-1}",
            "Element with key k goes in slot h(k)",
            "Collision: two keys hash to same slot",
            "Chaining: each slot is a linked list",
            "Expected search time O(1 + α) where α = n/m (load factor)"
        ],
        "pseudocode": """CHAINED-HASH-INSERT(T, x):
    insert x at head of list T[h(x.key)]

CHAINED-HASH-SEARCH(T, k):
    search for element with key k in list T[h(k)]

CHAINED-HASH-DELETE(T, x):
    delete x from list T[h(x.key)]""",
        "example": "Table size 10, h(k) = k mod 10. Keys 12, 22, 32 all go to slot 2.",
        "why_matters": "One of the most useful data structures. O(1) average operations."
    },
    "11.3": {
        "title": "Hash Functions",
        "summary": "How to design good hash functions that distribute keys uniformly.",
        "key_points": [
            "Goal: each key equally likely to hash to any slot",
            "Division method: h(k) = k mod m (avoid powers of 2 for m)",
            "Multiplication method: h(k) = ⌊m(kA mod 1)⌋ where 0 < A < 1",
            "Universal hashing: randomly choose h to prevent adversarial inputs",
            "Cryptographic hashes for security applications"
        ],
        "example": "Multiplication with A = (√5-1)/2 ≈ 0.618 (golden ratio) works well. For k=123, m=100: h = ⌊100(123·0.618 mod 1)⌋.",
        "why_matters": "Good hash functions are crucial for hash table performance."
    },
    "11.4": {
        "title": "Open Addressing",
        "summary": "Handle collisions by probing for empty slots within the table itself.",
        "key_points": [
            "No chaining: all elements stored in the table",
            "Linear probing: h(k,i) = (h'(k) + i) mod m",
            "Quadratic probing: h(k,i) = (h'(k) + c₁i + c₂i²) mod m",
            "Double hashing: h(k,i) = (h₁(k) + i·h₂(k)) mod m",
            "Deletion is tricky: use DELETED marker"
        ],
        "pseudocode": """HASH-INSERT(T, k):
    i = 0
    repeat
        j = h(k, i)
        if T[j] == NIL:
            T[j] = k
            return j
        i = i + 1
    until i == m
    error "hash table overflow\"""",
        "example": "Linear probing: insert 12, 22, 32 (all hash to 2). 12→slot 2, 22→slot 3, 32→slot 4.",
        "why_matters": "Better cache performance than chaining, but clustering can be an issue."
    },
    # Chapter 12
    "12.1": {
        "title": "What is a Binary Search Tree?",
        "summary": "A binary tree where left descendants ≤ node ≤ right descendants.",
        "key_points": [
            "Binary search tree property: for node x, all keys in left subtree ≤ x.key ≤ all keys in right subtree",
            "Inorder traversal visits keys in sorted order",
            "Height h: operations are O(h)",
            "Balanced tree: h = O(log n). Unbalanced: h = O(n)",
            "Supports: search, min, max, successor, predecessor, insert, delete"
        ],
        "pseudocode": """INORDER-TREE-WALK(x):
    if x ≠ NIL:
        INORDER-TREE-WALK(x.left)
        print x.key
        INORDER-TREE-WALK(x.right)""",
        "example": "Tree with root 5, left child 3, right child 7. Inorder: 3, 5, 7 (sorted!).",
        "why_matters": "Foundation for many balanced tree structures."
    },
    "12.2": {
        "title": "Querying a Binary Search Tree",
        "summary": "Search, minimum, maximum, successor, and predecessor in O(h) time.",
        "key_points": [
            "SEARCH: compare with root, go left or right recursively",
            "MINIMUM: follow left pointers to the end",
            "MAXIMUM: follow right pointers to the end",
            "SUCCESSOR: right subtree min, or first ancestor where node is in left subtree",
            "PREDECESSOR: symmetric to successor"
        ],
        "pseudocode": """TREE-SEARCH(x, k):
    if x == NIL or k == x.key:
        return x
    if k < x.key:
        return TREE-SEARCH(x.left, k)
    else:
        return TREE-SEARCH(x.right, k)

TREE-MINIMUM(x):
    while x.left ≠ NIL:
        x = x.left
    return x""",
        "example": "Find 4 in BST rooted at 5: 4 < 5 → go left to 3. 4 > 3 → go right. Found 4!",
        "why_matters": "Efficient dictionary operations when tree is balanced."
    },
    "12.3": {
        "title": "Insertion and Deletion",
        "summary": "Modify BST while maintaining the BST property.",
        "key_points": [
            "INSERT: search for key, insert at leaf position found",
            "DELETE has three cases based on children count",
            "Case 1: no children → just remove",
            "Case 2: one child → replace with child",
            "Case 3: two children → replace with successor, delete successor"
        ],
        "pseudocode": """TREE-INSERT(T, z):
    y = NIL
    x = T.root
    while x ≠ NIL:
        y = x
        if z.key < x.key:
            x = x.left
        else:
            x = x.right
    z.parent = y
    if y == NIL: T.root = z
    elif z.key < y.key: y.left = z
    else: y.right = z""",
        "example": "Insert 6 into BST [5,3,7]: 6 > 5 → right, 6 < 7 → left of 7.",
        "why_matters": "Dynamic set operations. Balanced variants maintain O(log n) height."
    },
    # Chapter 13
    "13.1": {
        "title": "Properties of Red-Black Trees",
        "summary": "A self-balancing BST with color properties ensuring O(log n) height.",
        "key_points": [
            "Every node is RED or BLACK",
            "Root is BLACK",
            "Every leaf (NIL) is BLACK",
            "Red node's children must be BLACK (no two reds in a row)",
            "All paths from node to descendant leaves have same black-height",
            "Height ≤ 2 log(n+1) guaranteed!"
        ],
        "example": "A red-black tree with 15 nodes has height at most 2·log(16) = 8.",
        "why_matters": "Guaranteed O(log n) for all operations. Used in many standard libraries."
    },
    "13.2": {
        "title": "Rotations",
        "summary": "Local operations that maintain BST property while rebalancing.",
        "key_points": [
            "LEFT-ROTATE: move node down-left, right child up",
            "RIGHT-ROTATE: move node down-right, left child up",
            "Maintain BST property: inorder traversal unchanged",
            "O(1) time: only pointer changes",
            "Used after insert/delete to restore red-black properties"
        ],
        "pseudocode": """LEFT-ROTATE(T, x):
    y = x.right
    x.right = y.left
    if y.left ≠ NIL: y.left.parent = x
    y.parent = x.parent
    if x.parent == NIL: T.root = y
    elif x == x.parent.left: x.parent.left = y
    else: x.parent.right = y
    y.left = x
    x.parent = y""",
        "why_matters": "Fundamental operation for all balanced tree restructuring."
    },
    "13.3": {
        "title": "Insertion",
        "summary": "Insert like BST, color red, then fix violations with rotations.",
        "key_points": [
            "Insert as in regular BST, color new node RED",
            "May violate: root is black, or red-red parent-child",
            "Six cases (symmetric pairs) handled by rotations and recoloring",
            "Key insight: push violations up the tree toward root",
            "At most O(log n) time, at most 2 rotations"
        ],
        "example": "Insert creates red node. If parent is red, uncle determines which case. Recolor and/or rotate.",
        "why_matters": "Maintains balance automatically during insertions."
    },
    "13.4": {
        "title": "Deletion",
        "summary": "Delete as BST, then fix violations with rotations and recoloring.",
        "key_points": [
            "Delete using BST delete (three cases)",
            "If deleted node was BLACK, black-height may be violated",
            "Move 'extra black' up the tree until it can be absorbed",
            "Four cases (with symmetric mirrors) for fixing",
            "At most O(log n) time, at most 3 rotations"
        ],
        "example": "Delete black node → 'double black' at replacement. Rotate and recolor based on sibling's color and its children.",
        "why_matters": "Complete the red-black tree implementation for dynamic sets."
    },
    # Chapter 14
    "14.1": {
        "title": "Dynamic Order Statistics",
        "summary": "Augment red-black trees to support rank queries.",
        "key_points": [
            "Add size field to each node: number of nodes in subtree",
            "OS-SELECT(x, i): find i-th smallest element",
            "OS-RANK(T, x): find rank of element x",
            "size[x] = size[x.left] + size[x.right] + 1",
            "Update sizes during insert/delete/rotate in O(1) per operation"
        ],
        "pseudocode": """OS-SELECT(x, i):
    r = x.left.size + 1
    if i == r: return x
    elif i < r: return OS-SELECT(x.left, i)
    else: return OS-SELECT(x.right, i - r)

OS-RANK(T, x):
    r = x.left.size + 1
    y = x
    while y ≠ T.root:
        if y == y.parent.right:
            r = r + y.parent.left.size + 1
        y = y.parent
    return r""",
        "why_matters": "Find k-th smallest or rank in O(log n). Used in databases."
    },
    "14.2": {
        "title": "How to Augment a Data Structure",
        "summary": "A systematic method for adding information to data structures.",
        "key_points": [
            "Step 1: Choose underlying data structure",
            "Step 2: Determine additional information to maintain",
            "Step 3: Verify info can be maintained during modifications",
            "Step 4: Develop new operations using the info",
            "Theorem: if info depends only on node and children, can maintain in O(1) per rotation"
        ],
        "example": "For order statistics: use red-black tree, add size field, update size on rotations, implement SELECT and RANK.",
        "why_matters": "General technique applicable to many data structure design problems."
    },
    "14.3": {
        "title": "Interval Trees",
        "summary": "Red-black tree augmented to store intervals and find overlaps efficiently.",
        "key_points": [
            "Each node stores an interval [low, high]",
            "Key = low endpoint of interval",
            "Augmented info: max = maximum high endpoint in subtree",
            "INTERVAL-SEARCH: find any interval overlapping query interval",
            "All operations O(log n)"
        ],
        "pseudocode": """INTERVAL-SEARCH(T, i):
    x = T.root
    while x ≠ NIL and i does not overlap x.int:
        if x.left ≠ NIL and x.left.max ≥ i.low:
            x = x.left
        else:
            x = x.right
    return x""",
        "example": "Find interval overlapping [15,20]. Go left if left subtree's max ≥ 15, else go right.",
        "why_matters": "Used in computational geometry, scheduling, database queries."
    },
    # Chapter 16
    "16.1": {
        "title": "An Activity-Selection Problem",
        "summary": "Select maximum number of non-overlapping activities.",
        "key_points": [
            "Activities have start and finish times",
            "Goal: select maximum set of compatible (non-overlapping) activities",
            "Greedy: always pick activity that finishes earliest",
            "Sort by finish time, greedily select compatible activities",
            "Greedy choice: earliest finish leaves most room for others"
        ],
        "pseudocode": """GREEDY-ACTIVITY-SELECTOR(s, f):
    n = s.length
    A = {a₁}  # first activity (earliest finish)
    k = 1
    for m = 2 to n:
        if s[m] ≥ f[k]:  # compatible with last selected
            A = A ∪ {aₘ}
            k = m
    return A""",
        "example": "Activities: [1-4], [3-5], [0-6], [5-7], [3-9], [5-9], [6-10], [8-11]. Select: [1-4], [5-7], [8-11].",
        "why_matters": "Classic greedy problem. Shows greedy can be optimal when it has greedy-choice property."
    },
    "16.2": {
        "title": "Elements of the Greedy Strategy",
        "summary": "When does greedy work? Greedy-choice property and optimal substructure.",
        "key_points": [
            "Greedy-choice property: local optimal choice leads to global optimal",
            "Optimal substructure: optimal solution contains optimal solutions to subproblems",
            "Contrast with DP: greedy makes one choice, DP considers all",
            "Greedy is usually simpler and faster than DP",
            "Must prove greedy-choice property holds!"
        ],
        "example": "Activity selection: choosing earliest-finish activity leaves subproblem that also has optimal greedy solution.",
        "why_matters": "Understanding when greedy works vs when you need DP."
    },
    "16.3": {
        "title": "Huffman Codes",
        "summary": "Optimal prefix-free codes for data compression.",
        "key_points": [
            "Variable-length codes: frequent symbols get shorter codes",
            "Prefix-free: no code is prefix of another → unambiguous decoding",
            "Greedy: repeatedly merge two lowest-frequency nodes",
            "Build tree bottom-up, leaves are symbols",
            "Produces optimal prefix-free code!"
        ],
        "pseudocode": """HUFFMAN(C):
    n = |C|
    Q = C  # priority queue by frequency
    for i = 1 to n-1:
        allocate new node z
        z.left = x = EXTRACT-MIN(Q)
        z.right = y = EXTRACT-MIN(Q)
        z.freq = x.freq + y.freq
        INSERT(Q, z)
    return EXTRACT-MIN(Q)  # root of tree""",
        "example": "Frequencies: a:45, b:13, c:12, d:16, e:9, f:5. Huffman codes: a:0, c:100, b:101, f:1100, e:1101, d:111.",
        "why_matters": "Foundation of data compression. Used in JPEG, MP3, ZIP."
    },
    # Chapter 17
    "17.1": {
        "title": "Aggregate Analysis",
        "summary": "Calculate total cost of n operations, divide by n for amortized cost.",
        "key_points": [
            "Amortized cost: average cost per operation over worst-case sequence",
            "Different from average case: no probability involved",
            "Aggregate: sum total cost, divide by n operations",
            "Example: stack with MULTIPOP - O(1) amortized despite O(n) worst single op",
            "Key insight: expensive operations must be rare"
        ],
        "example": "n PUSH operations, then n/2 MULTIPOP operations. Total: 2n operations, at most 2n pops total. Amortized: O(1) per op.",
        "why_matters": "More accurate performance analysis for data structures."
    },
    "17.2": {
        "title": "The Accounting Method",
        "summary": "Charge each operation an amortized cost, store credit for later.",
        "key_points": [
            "Assign amortized cost (possibly different from actual) to each op",
            "Overcharging stores credit with objects",
            "Credit pays for future expensive operations",
            "Rule: total amortized cost ≥ total actual cost",
            "Credit can never go negative"
        ],
        "example": "Stack: charge PUSH $2 (actual $1, store $1 credit). MULTIPOP uses stored credit. Amortized O(1) per op.",
        "why_matters": "Intuitive way to think about amortized analysis."
    },
    "17.3": {
        "title": "The Potential Method",
        "summary": "Define potential function, amortized cost = actual + ΔΦ.",
        "key_points": [
            "Φ(D): potential function mapping data structure state to number",
            "Amortized cost: ĉᵢ = cᵢ + Φ(Dᵢ) - Φ(Dᵢ₋₁)",
            "Sum of amortized = sum of actual + Φ(Dₙ) - Φ(D₀)",
            "If Φ(Dₙ) ≥ Φ(D₀), amortized ≥ actual (what we want)",
            "Art: choosing the right potential function"
        ],
        "example": "Stack potential = number of items. PUSH: actual 1, Φ increases by 1, amortized = 2. POP: actual 1, Φ decreases by 1, amortized = 0.",
        "why_matters": "Most powerful and general amortized analysis technique."
    },
    "17.4": {
        "title": "Dynamic Tables",
        "summary": "Tables that grow and shrink automatically with amortized O(1) operations.",
        "key_points": [
            "Insert: if full, allocate double-size table, copy everything",
            "Delete: if quarter full, allocate half-size table, copy",
            "Single insert/delete: O(n) worst case!",
            "Amortized analysis: O(1) per operation",
            "Potential: captures how close to needing expansion/contraction"
        ],
        "example": "Table with n items. Insert doubles to 2n when full. But doubling happens only after n inserts. Cost n spread over n ops = O(1) each.",
        "why_matters": "How ArrayList/vector implementations work. Crucial for practical performance."
    },
    # Chapter 23
    "23.1": {
        "title": "Growing a Minimum Spanning Tree",
        "summary": "Generic MST algorithm: grow tree edge by edge using safe edges.",
        "key_points": [
            "MST connects all vertices with minimum total edge weight",
            "Generic approach: maintain set A of edges, add safe edges",
            "Safe edge: adding it keeps A a subset of some MST",
            "Cut property: lightest edge crossing any cut is safe",
            "A cut (S, V-S) respects A if no edge of A crosses it"
        ],
        "example": "Start with empty A. Find any cut, add its lightest crossing edge. Repeat until tree complete.",
        "why_matters": "Framework for understanding Kruskal and Prim algorithms."
    },
    "23.2": {
        "title": "The Algorithms of Kruskal and Prim",
        "summary": "Two efficient algorithms for finding minimum spanning trees.",
        "key_points": [
            "Kruskal: sort edges by weight, add if doesn't create cycle",
            "Use Union-Find to detect cycles efficiently",
            "Kruskal time: O(E log E) = O(E log V)",
            "Prim: grow tree from single vertex, always add lightest edge to tree",
            "Prim with binary heap: O(E log V). With Fibonacci heap: O(E + V log V)"
        ],
        "pseudocode": """MST-KRUSKAL(G, w):
    A = ∅
    for each vertex v: MAKE-SET(v)
    sort edges by weight
    for each edge (u,v) in sorted order:
        if FIND-SET(u) ≠ FIND-SET(v):
            A = A ∪ {(u,v)}
            UNION(u, v)
    return A

MST-PRIM(G, w, r):
    for each u: key[u] = ∞, π[u] = NIL
    key[r] = 0
    Q = V  # min-priority queue
    while Q not empty:
        u = EXTRACT-MIN(Q)
        for each v adjacent to u:
            if v ∈ Q and w(u,v) < key[v]:
                π[v] = u
                key[v] = w(u,v)""",
        "why_matters": "Network design, clustering, approximation algorithms."
    },
    # Chapter 24 - already have 24.1 and 24.3, add 24.2
    "24.2": {
        "title": "Single-Source Shortest Paths in DAGs",
        "summary": "Shortest paths in directed acyclic graphs using topological sort.",
        "key_points": [
            "Works with negative edges (unlike Dijkstra)",
            "Topologically sort vertices first",
            "Relax edges in topological order",
            "Each vertex and edge processed exactly once",
            "Time: O(V + E) - linear!"
        ],
        "pseudocode": """DAG-SHORTEST-PATHS(G, w, s):
    topologically sort vertices of G
    INITIALIZE-SINGLE-SOURCE(G, s)
    for each vertex u in topological order:
        for each vertex v adjacent to u:
            RELAX(u, v, w)""",
        "example": "PERT chart: find longest path = critical path for project scheduling.",
        "why_matters": "Linear time shortest paths for DAGs. Critical path analysis."
    },
    # Chapter 25
    "25.1": {
        "title": "Shortest Paths and Matrix Multiplication",
        "summary": "All-pairs shortest paths using matrix multiplication approach.",
        "key_points": [
            "L⁽ᵐ⁾[i,j] = shortest path from i to j using at most m edges",
            "L⁽ᵐ⁾ computed from L⁽ᵐ⁻¹⁾ like matrix multiplication",
            "Substitute min for +, + for ×",
            "L⁽ⁿ⁻¹⁾ contains all shortest paths (no neg cycles)",
            "Time: O(n⁴) naive, O(n³ log n) with repeated squaring"
        ],
        "example": "Compute L¹, L², L⁴, L⁸, ... until L⁽ⁿ⁻¹⁾. Each squaring doubles the path length considered.",
        "why_matters": "Shows connection between shortest paths and matrix algebra."
    },
    "25.2": {
        "title": "The Floyd-Warshall Algorithm",
        "summary": "All-pairs shortest paths using dynamic programming in O(V³).",
        "key_points": [
            "DP on intermediate vertices: d⁽ᵏ⁾[i,j] = shortest i→j using only 1..k as intermediates",
            "Recurrence: d⁽ᵏ⁾[i,j] = min(d⁽ᵏ⁻¹⁾[i,j], d⁽ᵏ⁻¹⁾[i,k] + d⁽ᵏ⁻¹⁾[k,j])",
            "Either use vertex k or don't",
            "Time: O(V³), Space: O(V²)",
            "Can also compute transitive closure"
        ],
        "pseudocode": """FLOYD-WARSHALL(W):
    n = W.rows
    D⁽⁰⁾ = W
    for k = 1 to n:
        for i = 1 to n:
            for j = 1 to n:
                d⁽ᵏ⁾[i,j] = min(d⁽ᵏ⁻¹⁾[i,j], d⁽ᵏ⁻¹⁾[i,k] + d⁽ᵏ⁻¹⁾[k,j])
    return D⁽ⁿ⁾""",
        "example": "4 vertices. Start with edge weights. After k=1: consider paths through vertex 1. After k=2: through 1,2. Etc.",
        "why_matters": "Simple, elegant O(V³) algorithm. Works with negative edges (no negative cycles)."
    },
    "25.3": {
        "title": "Johnson's Algorithm",
        "summary": "All-pairs shortest paths in sparse graphs using reweighting.",
        "key_points": [
            "Better than Floyd-Warshall for sparse graphs",
            "Add new vertex s, run Bellman-Ford from s",
            "Reweight edges: ŵ(u,v) = w(u,v) + h(u) - h(v) ≥ 0",
            "Run Dijkstra from each vertex with new weights",
            "Time: O(VE + V² log V) with Fibonacci heaps"
        ],
        "pseudocode": """JOHNSON(G, w):
    add vertex s, edges (s,v) with weight 0
    if BELLMAN-FORD(G', w, s) == FALSE:
        return "negative cycle"
    for each v: h(v) = δ(s, v)
    for each edge (u,v):
        ŵ(u,v) = w(u,v) + h(u) - h(v)
    for each vertex u:
        run DIJKSTRA(G, ŵ, u)
        for each v: d(u,v) = δ̂(u,v) + h(v) - h(u)
    return D""",
        "why_matters": "Fastest for sparse graphs with negative edges."
    },
    # Chapter 26
    "26.1": {
        "title": "Flow Networks",
        "summary": "Model flow of commodities through a network with capacities.",
        "key_points": [
            "Directed graph with source s and sink t",
            "Each edge (u,v) has capacity c(u,v) ≥ 0",
            "Flow f(u,v): actual flow through edge",
            "Capacity constraint: 0 ≤ f(u,v) ≤ c(u,v)",
            "Flow conservation: flow into v = flow out of v (except s,t)"
        ],
        "example": "Water pipes, network bandwidth, traffic routing. Source produces, sink consumes, edges have maximum capacity.",
        "why_matters": "Models many real-world optimization problems."
    },
    "26.2": {
        "title": "The Ford-Fulkerson Method",
        "summary": "Find maximum flow by repeatedly finding augmenting paths.",
        "key_points": [
            "Residual network: remaining capacity after current flow",
            "Augmenting path: path from s to t in residual network",
            "Augment flow along path by minimum residual capacity",
            "Max-flow min-cut theorem: max flow = min cut capacity",
            "Edmonds-Karp: use BFS for paths → O(VE²)"
        ],
        "pseudocode": """FORD-FULKERSON(G, s, t):
    for each edge (u,v): f(u,v) = 0
    while exists augmenting path p in residual network:
        cf(p) = min{cf(u,v) : (u,v) on p}
        for each edge (u,v) on p:
            f(u,v) = f(u,v) + cf(p)
            f(v,u) = f(v,u) - cf(p)
    return f""",
        "example": "Find path s→a→b→t with bottleneck capacity 5. Augment by 5. Repeat until no path exists.",
        "why_matters": "Foundational algorithm for network optimization."
    },
    "26.3": {
        "title": "Maximum Bipartite Matching",
        "summary": "Find maximum matching in bipartite graph using max flow.",
        "key_points": [
            "Bipartite graph: vertices in two sets L and R, edges only between sets",
            "Matching: set of edges with no shared vertices",
            "Reduction to max flow: add source (edges to L) and sink (edges from R)",
            "All capacities = 1",
            "Max flow = max matching size"
        ],
        "example": "Job assignment: L = workers, R = jobs, edge if worker can do job. Max matching = max workers assigned.",
        "why_matters": "Job assignment, resource allocation, many applications."
    },
    # Chapter 22 - add 22.5
    "22.5": {
        "title": "Strongly Connected Components",
        "summary": "Decompose directed graph into maximal strongly connected subgraphs.",
        "key_points": [
            "SCC: maximal set where every vertex reachable from every other",
            "Component graph is always a DAG",
            "Algorithm: two DFS passes",
            "First DFS: compute finish times",
            "Second DFS on transpose graph in decreasing finish time order"
        ],
        "pseudocode": """SCC(G):
    call DFS(G) to compute finish times f[u]
    compute Gᵀ (transpose graph)
    call DFS(Gᵀ) with vertices in decreasing f[u] order
    each DFS tree in second pass is an SCC""",
        "example": "Web pages: SCC = group of pages all mutually reachable. Component graph shows relationships between groups.",
        "why_matters": "Graph decomposition, 2-SAT, many graph problems reduce to SCCs."
    },
    # Chapter 18 - B-Trees
    "18.1": {
        "title": "Definition of B-trees",
        "summary": "Balanced search trees optimized for disk-based storage with high branching factor.",
        "key_points": [
            "Every node has many keys: between t-1 and 2t-1 keys",
            "All leaves at same depth (perfectly balanced)",
            "Internal nodes have one more child than keys",
            "Height h ≤ log_t((n+1)/2) - much shorter than binary trees",
            "Minimizes disk I/O by reading/writing whole pages"
        ],
        "example": "B-tree with t=1000: 1 billion keys in height 3. Compare to balanced binary tree needing height 30!",
        "why_matters": "Foundation of database indexes. Every major database uses B-trees or variants."
    },
    "18.2": {
        "title": "Basic Operations on B-trees",
        "summary": "Search, create, and split operations on B-trees.",
        "key_points": [
            "SEARCH: like BST search but scan within node to find child",
            "All operations O(t log_t n) = O(log n)",
            "Split: when node has 2t-1 keys, split into two t-1 nodes",
            "Splitting moves middle key up to parent",
            "Split before insert avoids propagating splits up"
        ],
        "pseudocode": """B-TREE-SEARCH(x, k):
    i = 1
    while i ≤ x.n and k > x.key[i]:
        i = i + 1
    if i ≤ x.n and k == x.key[i]:
        return (x, i)
    elif x.leaf:
        return NIL
    else:
        DISK-READ(x.c[i])
        return B-TREE-SEARCH(x.c[i], k)""",
        "why_matters": "Core operations for database queries."
    },
    "18.3": {
        "title": "Deleting a Key from a B-tree",
        "summary": "Remove keys while maintaining B-tree properties.",
        "key_points": [
            "Case 1: key in leaf → just remove (if ≥ t keys)",
            "Case 2: key in internal node → replace with predecessor/successor",
            "Case 3: ensure child has ≥ t keys before descending",
            "Merge siblings when both have t-1 keys",
            "Always delete from a node with ≥ t keys (single pass)"
        ],
        "example": "Delete from internal node: find predecessor (largest in left subtree), swap, delete from leaf.",
        "why_matters": "Complete B-tree implementation for dynamic databases."
    },
    # Chapter 21 - Disjoint Sets
    "21.1": {
        "title": "Disjoint-set Operations",
        "summary": "Data structure for maintaining disjoint sets with efficient union and find.",
        "key_points": [
            "MAKE-SET(x): create singleton set containing x",
            "UNION(x, y): merge sets containing x and y",
            "FIND-SET(x): return representative of set containing x",
            "Used for connected components, Kruskal's MST",
            "Goal: very fast operations (nearly O(1))"
        ],
        "example": "Connected components: MAKE-SET for each vertex. For each edge (u,v), if FIND-SET(u) ≠ FIND-SET(v), UNION(u,v).",
        "why_matters": "Efficiently track connectivity as edges are added."
    },
    "21.2": {
        "title": "Linked-list Representation",
        "summary": "Simple representation using linked lists.",
        "key_points": [
            "Each set is a linked list",
            "Representative = head of list",
            "FIND-SET: follow pointer to head, O(1)",
            "UNION: append one list to another",
            "Naive UNION: O(n) - must update all pointers"
        ],
        "example": "Union by appending smaller list to larger: amortized O(log n) per operation.",
        "why_matters": "Simple but not optimal - motivates tree-based approach."
    },
    "21.3": {
        "title": "Disjoint-set Forests",
        "summary": "Tree-based representation with union by rank and path compression.",
        "key_points": [
            "Each set is a rooted tree, root is representative",
            "FIND-SET: follow parent pointers to root",
            "Union by rank: attach shorter tree under taller",
            "Path compression: make all nodes point directly to root during FIND",
            "With both: nearly O(1) per operation!"
        ],
        "pseudocode": """FIND-SET(x):
    if x ≠ x.p:
        x.p = FIND-SET(x.p)  # path compression
    return x.p

UNION(x, y):
    LINK(FIND-SET(x), FIND-SET(y))

LINK(x, y):
    if x.rank > y.rank:
        y.p = x
    else:
        x.p = y
        if x.rank == y.rank:
            y.rank = y.rank + 1""",
        "example": "m operations on n elements: O(m · α(n)) where α is inverse Ackermann (practically constant).",
        "why_matters": "One of the most efficient data structures known. Used in Kruskal's algorithm."
    },
    # Chapter 32 - String Matching
    "32.1": {
        "title": "The Naive String-Matching Algorithm",
        "summary": "Check for pattern at every position in text.",
        "key_points": [
            "Text T of length n, pattern P of length m",
            "Try each position 0 to n-m",
            "Compare P with T[s..s+m-1] at each shift s",
            "Time: O((n-m+1)m) worst case",
            "Simple but slow for long patterns"
        ],
        "pseudocode": """NAIVE-STRING-MATCHER(T, P):
    n = T.length
    m = P.length
    for s = 0 to n - m:
        if P[1..m] == T[s+1..s+m]:
            print "Pattern at shift" s""",
        "example": "T='AAAAAAB', P='AAB'. Check 5 positions, each comparing 3 chars = 15 comparisons.",
        "why_matters": "Baseline for understanding more efficient algorithms."
    },
    "32.2": {
        "title": "The Rabin-Karp Algorithm",
        "summary": "Use hashing to quickly filter potential matches.",
        "key_points": [
            "Compute hash of pattern and sliding window of text",
            "If hashes match, verify with character comparison",
            "Rolling hash: compute next hash from previous in O(1)",
            "Expected time: O(n + m)",
            "Worst case O(nm) if many hash collisions"
        ],
        "pseudocode": """RABIN-KARP(T, P, d, q):
    p = hash of P
    t = hash of T[1..m]
    for s = 0 to n-m:
        if p == t:
            if P == T[s+1..s+m]:
                print "Match at" s
        t = ((t - T[s+1]·h) · d + T[s+m+1]) mod q""",
        "example": "Multiple pattern search: compute hash of each pattern once, check text against all hashes.",
        "why_matters": "Plagiarism detection, multiple pattern matching."
    },
    "32.3": {
        "title": "String Matching with Finite Automata",
        "summary": "Build state machine that processes text character by character.",
        "key_points": [
            "States 0 to m represent 'matched i characters'",
            "Transition function δ(q, a): next state after seeing character a in state q",
            "Process each text character once: O(n) matching",
            "Preprocessing: O(m|Σ|) to build transition table",
            "Total: O(m|Σ| + n)"
        ],
        "example": "Pattern 'aba': state 0 →(a)→ 1 →(b)→ 2 →(a)→ 3 (accept). On mismatch, go to longest proper prefix that's also suffix.",
        "why_matters": "Foundation for KMP algorithm, shows pattern matching as state machine."
    },
    "32.4": {
        "title": "The Knuth-Morris-Pratt Algorithm",
        "summary": "Linear-time string matching using failure function.",
        "key_points": [
            "Never re-compare characters already matched",
            "Failure function π[q]: length of longest proper prefix of P[1..q] that's also suffix",
            "On mismatch at position q, shift pattern to align at π[q-1]",
            "Preprocessing: O(m), Matching: O(n), Total: O(n + m)",
            "Optimal in the comparison model"
        ],
        "pseudocode": """KMP-MATCHER(T, P):
    n = T.length, m = P.length
    π = COMPUTE-PREFIX-FUNCTION(P)
    q = 0
    for i = 1 to n:
        while q > 0 and P[q+1] ≠ T[i]:
            q = π[q]
        if P[q+1] == T[i]:
            q = q + 1
        if q == m:
            print "Match at" i-m
            q = π[q]""",
        "example": "Pattern 'abab': π = [0,0,1,2]. Match T='abababab': shifts after each match use π to avoid re-checking.",
        "why_matters": "Optimal string matching algorithm. Foundation for many text processing tools."
    },
    # Chapter 34 - NP-Completeness
    "34.1": {
        "title": "Polynomial Time",
        "summary": "Problems solvable efficiently - the class P.",
        "key_points": [
            "Polynomial time = O(n^k) for some constant k",
            "Class P: decision problems solvable in polynomial time",
            "Polynomial-time reductions: problem A ≤_P B",
            "If A ≤_P B and B ∈ P, then A ∈ P",
            "Efficiency: polynomial is 'tractable', exponential is 'intractable'"
        ],
        "example": "Sorting: O(n log n) ⊂ O(n²) = polynomial. Brute-force satisfiability: O(2^n) = exponential.",
        "why_matters": "Defines what 'efficiently solvable' means in complexity theory."
    },
    "34.2": {
        "title": "Polynomial-Time Verification",
        "summary": "Problems where solutions can be verified quickly - the class NP.",
        "key_points": [
            "NP: decision problems where YES instances have polynomial-time verifiable certificates",
            "Certificate: proof that answer is YES",
            "Example: Hamiltonian cycle - given cycle, verify in O(n)",
            "P ⊆ NP (every problem in P has trivial certificate)",
            "Open question: P = NP?"
        ],
        "example": "3-SAT: given assignment, check all clauses satisfied in O(n). Finding satisfying assignment may be hard.",
        "why_matters": "Captures intuitively 'checkable but maybe not findable' problems."
    },
    "34.3": {
        "title": "NP-Completeness and Reducibility",
        "summary": "The hardest problems in NP.",
        "key_points": [
            "NP-hard: at least as hard as any problem in NP",
            "NP-complete = NP-hard ∩ NP",
            "Reduction: A ≤_P B means solving B solves A",
            "If any NP-complete problem is in P, then P = NP",
            "Cook-Levin theorem: SAT is NP-complete"
        ],
        "example": "3-SAT ≤_P CLIQUE: convert formula to graph where clique exists iff formula satisfiable.",
        "why_matters": "Shows many problems are computationally equivalent - solving one solves all."
    },
    "34.4": {
        "title": "NP-Completeness Proofs",
        "summary": "How to prove a problem is NP-complete.",
        "key_points": [
            "Step 1: Show problem is in NP (verify solution in poly time)",
            "Step 2: Show problem is NP-hard (reduce from known NP-complete)",
            "Key: transform instances in polynomial time",
            "Preserve YES/NO answers",
            "Common source problems: 3-SAT, CLIQUE, VERTEX-COVER"
        ],
        "example": "Prove VERTEX-COVER NP-complete: reduce from CLIQUE. G has k-clique iff complement has (n-k)-vertex-cover.",
        "why_matters": "Toolkit for proving computational difficulty of new problems."
    },
    "34.5": {
        "title": "NP-Complete Problems",
        "summary": "A collection of important NP-complete problems.",
        "key_points": [
            "CLIQUE: is there a k-clique in graph G?",
            "VERTEX-COVER: can k vertices cover all edges?",
            "HAMILTONIAN-CYCLE: is there a cycle visiting all vertices?",
            "TRAVELING-SALESMAN: tour of length ≤ k?",
            "SUBSET-SUM: subset summing to target value?"
        ],
        "example": "All these problems: easy to verify (NP), hard to solve (NP-hard), polynomially equivalent via reductions.",
        "why_matters": "Recognize NP-complete problems to know when to use heuristics/approximations."
    },
}

# ============ PAGE TO SECTION MAPPING ============
# Based on TOC - maps page ranges to section numbers
PAGE_TO_SECTION = {
    # Chapter 1
    5: "1.1", 6: "1.1", 7: "1.1", 8: "1.1", 9: "1.1", 10: "1.1", 11: "1.1",
    12: "1.2", 13: "1.2", 14: "1.2", 15: "1.2",
    # Chapter 2
    16: "2.1", 17: "2.1", 18: "2.1", 19: "2.1", 20: "2.1", 21: "2.1", 22: "2.1",
    23: "2.2", 24: "2.2", 25: "2.2", 26: "2.2", 27: "2.2", 28: "2.2", 29: "2.2",
    30: "2.3", 31: "2.3", 32: "2.3", 33: "2.3", 34: "2.3", 35: "2.3", 36: "2.3", 37: "2.3", 38: "2.3", 39: "2.3", 40: "2.3", 41: "2.3", 42: "2.3",
    # Chapter 3
    43: "3.1", 44: "3.1", 45: "3.1", 46: "3.1", 47: "3.1", 48: "3.1", 49: "3.1", 50: "3.1", 51: "3.1", 52: "3.1", 53: "3.1",
    54: "3.2", 55: "3.2", 56: "3.2", 57: "3.2", 58: "3.2", 59: "3.2", 60: "3.2", 61: "3.2", 62: "3.2", 63: "3.2", 64: "3.2",
    # Chapter 4
    65: "4.1", 66: "4.1", 67: "4.1", 68: "4.1", 69: "4.1", 70: "4.1", 71: "4.1", 72: "4.1", 73: "4.1", 74: "4.1", 75: "4.1",
    76: "4.2", 77: "4.2", 78: "4.2", 79: "4.2", 80: "4.2", 81: "4.2", 82: "4.2",
    83: "4.3", 84: "4.3", 85: "4.3", 86: "4.3", 87: "4.3", 88: "4.3", 89: "4.3", 90: "4.3",
    91: "4.4", 92: "4.4", 93: "4.4", 94: "4.4", 95: "4.4", 96: "4.4", 97: "4.4", 98: "4.4",
    99: "4.5", 100: "4.5", 101: "4.5", 102: "4.5", 103: "4.5", 104: "4.5", 105: "4.5", 106: "4.5", 107: "4.5", 108: "4.5", 109: "4.5", 110: "4.5", 111: "4.5", 112: "4.5", 113: "4.5",
    # Chapter 5
    114: "5.1", 115: "5.1", 116: "5.1", 117: "5.1", 118: "5.1", 119: "5.1", 120: "5.1",
    121: "5.2", 122: "5.2", 123: "5.2", 124: "5.2", 125: "5.2", 126: "5.2", 127: "5.2", 128: "5.2",
    129: "5.3", 130: "5.3", 131: "5.3", 132: "5.3", 133: "5.3", 134: "5.3", 135: "5.3", 136: "5.3", 137: "5.3", 138: "5.3", 139: "5.3", 140: "5.3", 141: "5.3", 142: "5.3", 143: "5.3", 144: "5.3", 145: "5.3", 146: "5.3", 147: "5.3", 148: "5.3", 149: "5.3", 150: "5.3",
    # Chapter 6
    151: "6.1", 152: "6.1", 153: "6.1", 154: "6.1", 155: "6.1",
    156: "6.2", 157: "6.2", 158: "6.2", 159: "6.2",
    160: "6.3", 161: "6.3", 162: "6.3",
    163: "6.4", 164: "6.4", 165: "6.4",
    166: "6.5", 167: "6.5", 168: "6.5", 169: "6.5",
    # Chapter 7
    170: "7.1", 171: "7.1", 172: "7.1", 173: "7.1", 174: "7.1", 175: "7.1", 176: "7.1", 177: "7.1", 178: "7.1",
    179: "7.2", 180: "7.2", 181: "7.2", 182: "7.2",
    183: "7.3", 184: "7.3", 185: "7.3", 186: "7.3", 187: "7.3", 188: "7.3", 189: "7.3", 190: "7.3",
    # Chapter 8
    191: "8.1", 192: "8.1", 193: "8.1", 194: "8.1", 195: "8.1",
    196: "8.2", 197: "8.2", 198: "8.2", 199: "8.2",
    200: "8.3", 201: "8.3", 202: "8.3", 203: "8.3", 204: "8.3",
    205: "8.4", 206: "8.4", 207: "8.4", 208: "8.4", 209: "8.4", 210: "8.4", 211: "8.4", 212: "8.4",
    # Chapter 9
    213: "9.1", 214: "9.1", 215: "9.1",
    216: "9.2", 217: "9.2", 218: "9.2", 219: "9.2", 220: "9.2", 221: "9.2", 222: "9.2",
    223: "9.3", 224: "9.3", 225: "9.3", 226: "9.3", 227: "9.3", 228: "9.3", 229: "9.3", 230: "9.3", 231: "9.3",
    # Chapter 10
    232: "10.1", 233: "10.1", 234: "10.1", 235: "10.1", 236: "10.1",
    237: "10.2", 238: "10.2", 239: "10.2", 240: "10.2", 241: "10.2",
    242: "10.3", 243: "10.3", 244: "10.3", 245: "10.3", 246: "10.3",
    247: "10.4", 248: "10.4", 249: "10.4", 250: "10.4", 251: "10.4", 252: "10.4",
    # Chapter 11
    253: "11.1", 254: "11.1", 255: "11.1", 256: "11.1",
    257: "11.2", 258: "11.2", 259: "11.2", 260: "11.2", 261: "11.2", 262: "11.2", 263: "11.2", 264: "11.2", 265: "11.2",
    266: "11.3", 267: "11.3", 268: "11.3", 269: "11.3", 270: "11.3", 271: "11.3", 272: "11.3", 273: "11.3", 274: "11.3", 275: "11.3", 276: "11.3", 277: "11.3",
    278: "11.4", 279: "11.4", 280: "11.4", 281: "11.4", 282: "11.4", 283: "11.4", 284: "11.4", 285: "11.4",
    # Chapter 12
    286: "12.1", 287: "12.1", 288: "12.1", 289: "12.1", 290: "12.1",
    291: "12.2", 292: "12.2", 293: "12.2", 294: "12.2", 295: "12.2", 296: "12.2",
    297: "12.3", 298: "12.3", 299: "12.3", 300: "12.3", 301: "12.3", 302: "12.3", 303: "12.3", 304: "12.3", 305: "12.3", 306: "12.3", 307: "12.3",
    # Chapter 13
    308: "13.1", 309: "13.1", 310: "13.1", 311: "13.1", 312: "13.1",
    313: "13.2", 314: "13.2", 315: "13.2", 316: "13.2",
    317: "13.3", 318: "13.3", 319: "13.3", 320: "13.3", 321: "13.3", 322: "13.3", 323: "13.3", 324: "13.3", 325: "13.3", 326: "13.3", 327: "13.3", 328: "13.3",
    329: "13.4", 330: "13.4", 331: "13.4", 332: "13.4", 333: "13.4", 334: "13.4", 335: "13.4", 336: "13.4", 337: "13.4", 338: "13.4",
    # Chapter 14
    339: "14.1", 340: "14.1", 341: "14.1", 342: "14.1", 343: "14.1", 344: "14.1", 345: "14.1",
    346: "14.2", 347: "14.2", 348: "14.2", 349: "14.2", 350: "14.2",
    351: "14.3", 352: "14.3", 353: "14.3", 354: "14.3", 355: "14.3", 356: "14.3", 357: "14.3", 358: "14.3",
    # Chapter 15
    359: "15.1", 360: "15.1", 361: "15.1", 362: "15.1", 363: "15.1", 364: "15.1", 365: "15.1", 366: "15.1", 367: "15.1", 368: "15.1", 369: "15.1", 370: "15.1",
    371: "15.2", 372: "15.2", 373: "15.2", 374: "15.2", 375: "15.2", 376: "15.2", 377: "15.2", 378: "15.2", 379: "15.2", 380: "15.2", 381: "15.2", 382: "15.2", 383: "15.2",
    384: "15.3", 385: "15.3", 386: "15.3", 387: "15.3", 388: "15.3", 389: "15.3", 390: "15.3", 391: "15.3", 392: "15.3", 393: "15.3",
    394: "15.4", 395: "15.4", 396: "15.4", 397: "15.4", 398: "15.4", 399: "15.4", 400: "15.4", 401: "15.4", 402: "15.4", 403: "15.4",
    # Chapter 16
    414: "16.1", 415: "16.1", 416: "16.1", 417: "16.1", 418: "16.1", 419: "16.1", 420: "16.1", 421: "16.1",
    422: "16.2", 423: "16.2", 424: "16.2", 425: "16.2", 426: "16.2", 427: "16.2", 428: "16.2",
    429: "16.3", 430: "16.3", 431: "16.3", 432: "16.3", 433: "16.3", 434: "16.3", 435: "16.3", 436: "16.3", 437: "16.3", 438: "16.3", 439: "16.3", 440: "16.3",
    # Chapter 17
    451: "17.1", 452: "17.1", 453: "17.1", 454: "17.1", 455: "17.1", 456: "17.1",
    457: "17.2", 458: "17.2", 459: "17.2", 460: "17.2", 461: "17.2",
    462: "17.3", 463: "17.3", 464: "17.3", 465: "17.3", 466: "17.3", 467: "17.3", 468: "17.3",
    469: "17.4", 470: "17.4", 471: "17.4", 472: "17.4", 473: "17.4", 474: "17.4", 475: "17.4", 476: "17.4", 477: "17.4", 478: "17.4", 479: "17.4", 480: "17.4", 481: "17.4", 482: "17.4", 483: "17.4",
    # Chapter 22
    589: "22.1", 590: "22.1", 591: "22.1", 592: "22.1", 593: "22.1", 594: "22.1",
    595: "22.2", 596: "22.2", 597: "22.2", 598: "22.2", 599: "22.2", 600: "22.2", 601: "22.2", 602: "22.2", 603: "22.2",
    604: "22.3", 605: "22.3", 606: "22.3", 607: "22.3", 608: "22.3", 609: "22.3", 610: "22.3", 611: "22.3", 612: "22.3",
    613: "22.4", 614: "22.4", 615: "22.4", 616: "22.4",
    617: "22.5", 618: "22.5", 619: "22.5", 620: "22.5", 621: "22.5", 622: "22.5", 623: "22.5",
    # Chapter 23
    624: "23.1", 625: "23.1", 626: "23.1", 627: "23.1", 628: "23.1", 629: "23.1", 630: "23.1",
    631: "23.2", 632: "23.2", 633: "23.2", 634: "23.2", 635: "23.2", 636: "23.2", 637: "23.2", 638: "23.2", 639: "23.2", 640: "23.2", 641: "23.2", 642: "23.2",
    # Chapter 24
    643: "24.1", 644: "24.1", 645: "24.1", 646: "24.1", 647: "24.1", 648: "24.1", 649: "24.1", 650: "24.1", 651: "24.1",
    652: "24.2", 653: "24.2", 654: "24.2", 655: "24.2", 656: "24.2",
    657: "24.3", 658: "24.3", 659: "24.3", 660: "24.3", 661: "24.3", 662: "24.3", 663: "24.3", 664: "24.3", 665: "24.3", 666: "24.3", 667: "24.3", 668: "24.3",
    # Chapter 25
    684: "25.1", 685: "25.1", 686: "25.1", 687: "25.1", 688: "25.1", 689: "25.1", 690: "25.1",
    691: "25.2", 692: "25.2", 693: "25.2", 694: "25.2", 695: "25.2", 696: "25.2", 697: "25.2", 698: "25.2",
    699: "25.3", 700: "25.3", 701: "25.3", 702: "25.3", 703: "25.3", 704: "25.3", 705: "25.3", 706: "25.3", 707: "25.3",
    # Chapter 26
    708: "26.1", 709: "26.1", 710: "26.1", 711: "26.1", 712: "26.1", 713: "26.1", 714: "26.1", 715: "26.1", 716: "26.1", 717: "26.1", 718: "26.1", 719: "26.1", 720: "26.1",
    721: "26.2", 722: "26.2", 723: "26.2", 724: "26.2", 725: "26.2", 726: "26.2", 727: "26.2", 728: "26.2", 729: "26.2", 730: "26.2", 731: "26.2", 732: "26.2", 733: "26.2", 734: "26.2", 735: "26.2", 736: "26.2", 737: "26.2", 738: "26.2", 739: "26.2", 740: "26.2", 741: "26.2", 742: "26.2", 743: "26.2", 744: "26.2", 745: "26.2", 746: "26.2", 747: "26.2", 748: "26.2", 749: "26.2", 750: "26.2", 751: "26.2", 752: "26.2", 753: "26.2", 754: "26.2", 755: "26.2",
    756: "26.3", 757: "26.3", 758: "26.3", 759: "26.3", 760: "26.3", 761: "26.3", 762: "26.3", 763: "26.3", 764: "26.3", 765: "26.3", 766: "26.3", 767: "26.3", 768: "26.3", 769: "26.3", 770: "26.3", 771: "26.3",
    # Chapter 18 - B-Trees (p.484)
    484: "18.1", 485: "18.1", 486: "18.1", 487: "18.1", 488: "18.1", 489: "18.1", 490: "18.1",
    491: "18.2", 492: "18.2", 493: "18.2", 494: "18.2", 495: "18.2", 496: "18.2", 497: "18.2", 498: "18.2", 499: "18.2", 500: "18.2",
    501: "18.3", 502: "18.3", 503: "18.3", 504: "18.3",
    # Chapter 21 - Disjoint Sets (p.561)
    561: "21.1", 562: "21.1", 563: "21.1", 564: "21.1", 565: "21.1",
    566: "21.2", 567: "21.2", 568: "21.2", 569: "21.2", 570: "21.2",
    571: "21.3", 572: "21.3", 573: "21.3", 574: "21.3", 575: "21.3", 576: "21.3", 577: "21.3", 578: "21.3", 579: "21.3", 580: "21.3", 581: "21.3", 582: "21.3", 583: "21.3", 584: "21.3", 585: "21.3", 586: "21.3", 587: "21.3", 588: "21.3",
    # Chapter 32 - String Matching (p.985)
    985: "32.1", 986: "32.1", 987: "32.1", 988: "32.1",
    989: "32.2", 990: "32.2", 991: "32.2", 992: "32.2", 993: "32.2", 994: "32.2",
    995: "32.3", 996: "32.3", 997: "32.3", 998: "32.3", 999: "32.3", 1000: "32.3", 1001: "32.3",
    1002: "32.4", 1003: "32.4", 1004: "32.4", 1005: "32.4", 1006: "32.4", 1007: "32.4", 1008: "32.4", 1009: "32.4", 1010: "32.4", 1011: "32.4", 1012: "32.4", 1013: "32.4",
    # Chapter 34 - NP-Completeness (p.1048)
    1048: "34.1", 1049: "34.1", 1050: "34.1", 1051: "34.1", 1052: "34.1", 1053: "34.1", 1054: "34.1", 1055: "34.1", 1056: "34.1", 1057: "34.1",
    1058: "34.2", 1059: "34.2", 1060: "34.2", 1061: "34.2", 1062: "34.2", 1063: "34.2", 1064: "34.2", 1065: "34.2",
    1066: "34.3", 1067: "34.3", 1068: "34.3", 1069: "34.3", 1070: "34.3", 1071: "34.3", 1072: "34.3", 1073: "34.3", 1074: "34.3", 1075: "34.3",
    1076: "34.4", 1077: "34.4", 1078: "34.4", 1079: "34.4", 1080: "34.4", 1081: "34.4", 1082: "34.4", 1083: "34.4", 1084: "34.4", 1085: "34.4",
    1086: "34.5", 1087: "34.5", 1088: "34.5", 1089: "34.5", 1090: "34.5", 1091: "34.5", 1092: "34.5", 1093: "34.5", 1094: "34.5", 1095: "34.5", 1096: "34.5", 1097: "34.5", 1098: "34.5", 1099: "34.5", 1100: "34.5", 1101: "34.5", 1102: "34.5", 1103: "34.5", 1104: "34.5", 1105: "34.5",
    # Chapter 19 - Fibonacci Heaps (p.505)
    505: "19.1", 506: "19.1", 507: "19.1", 508: "19.1",
    509: "19.2", 510: "19.2", 511: "19.2", 512: "19.2", 513: "19.2", 514: "19.2", 515: "19.2", 516: "19.2", 517: "19.2",
    518: "19.3", 519: "19.3", 520: "19.3", 521: "19.3", 522: "19.3",
    523: "19.4", 524: "19.4", 525: "19.4", 526: "19.4", 527: "19.4", 528: "19.4", 529: "19.4", 530: "19.4",
    # Chapter 20 - van Emde Boas Trees (p.531)
    531: "20.1", 532: "20.1", 533: "20.1", 534: "20.1", 535: "20.1", 536: "20.1",
    537: "20.2", 538: "20.2", 539: "20.2", 540: "20.2", 541: "20.2", 542: "20.2", 543: "20.2", 544: "20.2",
    545: "20.3", 546: "20.3", 547: "20.3", 548: "20.3", 549: "20.3", 550: "20.3", 551: "20.3", 552: "20.3", 553: "20.3", 554: "20.3", 555: "20.3", 556: "20.3", 557: "20.3", 558: "20.3", 559: "20.3", 560: "20.3",
    # Chapter 27 - Multithreaded Algorithms (p.772)
    772: "27.1", 773: "27.1", 774: "27.1", 775: "27.1", 776: "27.1", 777: "27.1", 778: "27.1", 779: "27.1", 780: "27.1", 781: "27.1", 782: "27.1", 783: "27.1", 784: "27.1", 785: "27.1", 786: "27.1", 787: "27.1", 788: "27.1", 789: "27.1", 790: "27.1", 791: "27.1", 792: "27.1",
    793: "27.2", 794: "27.2", 795: "27.2", 796: "27.2", 797: "27.2", 798: "27.2", 799: "27.2",
    800: "27.3", 801: "27.3", 802: "27.3", 803: "27.3", 804: "27.3", 805: "27.3", 806: "27.3", 807: "27.3", 808: "27.3", 809: "27.3", 810: "27.3", 811: "27.3", 812: "27.3",
    # Chapter 28 - Matrix Operations (p.813)
    813: "28.1", 814: "28.1", 815: "28.1", 816: "28.1", 817: "28.1", 818: "28.1", 819: "28.1", 820: "28.1", 821: "28.1", 822: "28.1", 823: "28.1", 824: "28.1", 825: "28.1", 826: "28.1", 827: "28.1",
    828: "28.2", 829: "28.2", 830: "28.2", 831: "28.2", 832: "28.2",
    833: "28.3", 834: "28.3", 835: "28.3", 836: "28.3", 837: "28.3", 838: "28.3", 839: "28.3", 840: "28.3", 841: "28.3", 842: "28.3",
    # Chapter 29 - Linear Programming (p.843)
    843: "29.1", 844: "29.1", 845: "29.1", 846: "29.1", 847: "29.1", 848: "29.1", 849: "29.1", 850: "29.1", 851: "29.1", 852: "29.1", 853: "29.1", 854: "29.1", 855: "29.1", 856: "29.1", 857: "29.1", 858: "29.1",
    859: "29.2", 860: "29.2", 861: "29.2", 862: "29.2", 863: "29.2",
    864: "29.3", 865: "29.3", 866: "29.3", 867: "29.3", 868: "29.3", 869: "29.3", 870: "29.3", 871: "29.3", 872: "29.3", 873: "29.3", 874: "29.3", 875: "29.3", 876: "29.3", 877: "29.3", 878: "29.3", 879: "29.3", 880: "29.3",
    # Chapter 30 - FFT (p.898)
    898: "30.1", 899: "30.1", 900: "30.1", 901: "30.1", 902: "30.1", 903: "30.1", 904: "30.1", 905: "30.1",
    906: "30.2", 907: "30.2", 908: "30.2", 909: "30.2", 910: "30.2", 911: "30.2", 912: "30.2", 913: "30.2", 914: "30.2",
    915: "30.3", 916: "30.3", 917: "30.3", 918: "30.3", 919: "30.3", 920: "30.3", 921: "30.3", 922: "30.3", 923: "30.3", 924: "30.3", 925: "30.3",
    # Chapter 31 - Number Theory (p.926)
    926: "31.1", 927: "31.1", 928: "31.1", 929: "31.1", 930: "31.1", 931: "31.1", 932: "31.1",
    933: "31.2", 934: "31.2", 935: "31.2", 936: "31.2", 937: "31.2", 938: "31.2",
    939: "31.3", 940: "31.3", 941: "31.3", 942: "31.3", 943: "31.3", 944: "31.3", 945: "31.3",
    958: "31.7", 959: "31.7", 960: "31.7", 961: "31.7", 962: "31.7", 963: "31.7", 964: "31.7",
    # Chapter 33 - Computational Geometry (p.1014)
    1014: "33.1", 1015: "33.1", 1016: "33.1", 1017: "33.1", 1018: "33.1", 1019: "33.1", 1020: "33.1",
    1021: "33.2", 1022: "33.2", 1023: "33.2", 1024: "33.2", 1025: "33.2", 1026: "33.2", 1027: "33.2", 1028: "33.2",
    1029: "33.3", 1030: "33.3", 1031: "33.3", 1032: "33.3", 1033: "33.3", 1034: "33.3", 1035: "33.3", 1036: "33.3", 1037: "33.3", 1038: "33.3",
    1039: "33.4", 1040: "33.4", 1041: "33.4", 1042: "33.4", 1043: "33.4", 1044: "33.4", 1045: "33.4", 1046: "33.4", 1047: "33.4",
    # Chapter 35 - Approximation Algorithms (p.1106)
    1106: "35.1", 1107: "35.1", 1108: "35.1", 1109: "35.1", 1110: "35.1",
    1111: "35.2", 1112: "35.2", 1113: "35.2", 1114: "35.2", 1115: "35.2", 1116: "35.2",
    1117: "35.3", 1118: "35.3", 1119: "35.3", 1120: "35.3", 1121: "35.3", 1122: "35.3",
    1123: "35.4", 1124: "35.4", 1125: "35.4", 1126: "35.4", 1127: "35.4",
    1128: "35.5", 1129: "35.5", 1130: "35.5", 1131: "35.5", 1132: "35.5", 1133: "35.5", 1134: "35.5", 1135: "35.5",
}

# ============ PAGE GENERATION ============

def create_toc_page(page_num):
    """Create table of contents pages."""
    return {
        "page": page_num,
        "title": "Table of Contents",
        "content": f"""<div class="article-header">
    <div class="section-label">Navigation</div>
    <h1>Table of Contents</h1>
</div>
<div class="original-content">
    <pre style="font-family: var(--font-sans); font-size: 0.85rem; line-height: 1.8; white-space: pre-wrap;">{TOC}</pre>
</div>
<div class="analysis-section">
    <h3>How to Navigate</h3>
    <div class="analysis-block">
        <div class="analysis-item">
            <h5>Keyboard Shortcuts</h5>
            <ul>
                <li><kbd>←</kbd> <kbd>→</kbd> Previous/Next page</li>
                <li><kbd>G</kbd> Go to specific page</li>
                <li><kbd>V</kbd> Toggle image/text view</li>
                <li><kbd>+</kbd> <kbd>-</kbd> Zoom in/out</li>
                <li><kbd>1-8</kbd> Zoom levels (70%-140%)</li>
                <li><kbd>Home</kbd> <kbd>End</kbd> First/Last page</li>
            </ul>
        </div>
    </div>
</div>"""
    }

def create_section_page(section_num, page_num, text):
    """Create a page for a specific section."""
    if section_num not in SECTIONS:
        return None

    sec = SECTIONS[section_num]

    points_html = '\n'.join([f'<li>{html.escape(p)}</li>' for p in sec.get('key_points', [])])

    pseudocode_html = ''
    if 'pseudocode' in sec:
        pseudocode_html = f'''<div class="algorithm">
    <h4>Pseudocode</h4>
    <pre style="font-size: 0.85rem; line-height: 1.6;">{html.escape(sec['pseudocode'])}</pre>
</div>'''

    example_html = ''
    if 'example' in sec:
        example_html = f'''<div class="figure-box">
    <h4>Example</h4>
    <p>{html.escape(sec['example'])}</p>
</div>'''

    why_html = ''
    if 'why_matters' in sec:
        why_html = f'''<div class="highlight-box">
    <h4>Why It Matters</h4>
    <p>{html.escape(sec['why_matters'])}</p>
</div>'''

    return {
        "page": page_num,
        "title": f"{section_num} {sec['title']}",
        "content": f"""<div class="article-header">
    <div class="section-label">Section {section_num}</div>
    <h1>{sec['title']}</h1>
</div>
<div class="original-content">
    <div class="definition-box">
        <h4>Summary</h4>
        <p><strong>{html.escape(sec['summary'])}</strong></p>
    </div>

    <div class="highlight-box">
        <h4>Key Points</h4>
        <ul>{points_html}</ul>
    </div>

    {pseudocode_html}
    {example_html}
    {why_html}
</div>"""
    }

def detect_section(text):
    """Detect section number from text."""
    match = re.search(r'^(\d+\.\d+)\s+', text, re.MULTILINE)
    if match:
        return match.group(1)
    return None

def process_page(page_num):
    """Process a single page."""
    # TOC pages (pages 6-15 are table of contents in CLRS)
    if 6 <= page_num <= 15:
        return create_toc_page(page_num)

    # First check explicit page-to-section mapping
    if page_num in PAGE_TO_SECTION:
        section = PAGE_TO_SECTION[page_num]
        if section in SECTIONS:
            return create_section_page(section, page_num, "")

    # Fall back to text detection
    txt_file = PAGES_DIR / f"page-{page_num:04d}.txt"
    if txt_file.exists():
        with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read().replace('\f', '').strip()

        section = detect_section(text)
        if section and section in SECTIONS:
            return create_section_page(section, page_num, text)

    # Return existing content for other pages
    existing_file = OUTPUT_DIR / f"page-{page_num:04d}.json"
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    return None

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
        else:
            # Keep existing manifest entry
            manifest_pages.append({
                "page": page_num,
                "title": f"Page {page_num}",
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
