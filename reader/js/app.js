// app.js - Application initialization and core functions
import { State } from './state.js';

const TOTAL_PAGES = 1313;
const ZOOM_LEVELS = [70, 80, 90, 100, 110, 120, 130, 140];
let currentPage = 1;
let currentView = localStorage.getItem('readerView') || 'image';
let currentZoom = parseInt(localStorage.getItem('readerZoom')) || 100;
let menuOpen = false;
let tocOpen = false;
const pageCache = {};

// Full TOC structure
const TOC_DATA = [
    { type: 'part', title: 'PART I: FOUNDATIONS' },
    { type: 'chapter', title: '1. The Role of Algorithms in Computing', page: 5 },
    { type: 'section', title: '1.1 Algorithms', page: 5 },
    { type: 'section', title: '1.2 Algorithms as a technology', page: 12 },
    { type: 'chapter', title: '2. Getting Started', page: 16 },
    { type: 'section', title: '2.1 Insertion sort', page: 16 },
    { type: 'section', title: '2.2 Analyzing algorithms', page: 23 },
    { type: 'section', title: '2.3 Designing algorithms', page: 30 },
    { type: 'chapter', title: '3. Growth of Functions', page: 43 },
    { type: 'section', title: '3.1 Asymptotic notation', page: 43 },
    { type: 'section', title: '3.2 Standard notations and common functions', page: 54 },
    { type: 'chapter', title: '4. Divide-and-Conquer', page: 65 },
    { type: 'section', title: '4.1 The maximum-subarray problem', page: 65 },
    { type: 'section', title: '4.2 Strassen\'s algorithm', page: 76 },
    { type: 'section', title: '4.3 Substitution method', page: 83 },
    { type: 'section', title: '4.4 Recursion-tree method', page: 91 },
    { type: 'section', title: '4.5 Master method', page: 99 },
    { type: 'chapter', title: '5. Probabilistic Analysis', page: 114 },
    { type: 'section', title: '5.1 The hiring problem', page: 114 },
    { type: 'section', title: '5.2 Indicator random variables', page: 121 },
    { type: 'section', title: '5.3 Randomized algorithms', page: 129 },

    { type: 'part', title: 'PART II: SORTING AND ORDER STATISTICS' },
    { type: 'chapter', title: '6. Heapsort', page: 151 },
    { type: 'section', title: '6.1 Heaps', page: 151 },
    { type: 'section', title: '6.2 Maintaining the heap property', page: 156 },
    { type: 'section', title: '6.3 Building a heap', page: 160 },
    { type: 'section', title: '6.4 The heapsort algorithm', page: 163 },
    { type: 'section', title: '6.5 Priority queues', page: 166 },
    { type: 'chapter', title: '7. Quicksort', page: 170 },
    { type: 'section', title: '7.1 Description of quicksort', page: 170 },
    { type: 'section', title: '7.2 Performance of quicksort', page: 179 },
    { type: 'section', title: '7.3 Randomized quicksort', page: 183 },
    { type: 'chapter', title: '8. Sorting in Linear Time', page: 191 },
    { type: 'section', title: '8.1 Lower bounds for sorting', page: 191 },
    { type: 'section', title: '8.2 Counting sort', page: 196 },
    { type: 'section', title: '8.3 Radix sort', page: 200 },
    { type: 'section', title: '8.4 Bucket sort', page: 205 },
    { type: 'chapter', title: '9. Medians and Order Statistics', page: 213 },
    { type: 'section', title: '9.1 Minimum and maximum', page: 213 },
    { type: 'section', title: '9.2 Selection in expected linear time', page: 216 },
    { type: 'section', title: '9.3 Selection in worst-case linear time', page: 223 },

    { type: 'part', title: 'PART III: DATA STRUCTURES' },
    { type: 'chapter', title: '10. Elementary Data Structures', page: 232 },
    { type: 'section', title: '10.1 Stacks and queues', page: 232 },
    { type: 'section', title: '10.2 Linked lists', page: 237 },
    { type: 'section', title: '10.3 Implementing pointers and objects', page: 242 },
    { type: 'section', title: '10.4 Representing rooted trees', page: 247 },
    { type: 'chapter', title: '11. Hash Tables', page: 253 },
    { type: 'section', title: '11.1 Direct-address tables', page: 253 },
    { type: 'section', title: '11.2 Hash tables', page: 257 },
    { type: 'section', title: '11.3 Hash functions', page: 266 },
    { type: 'section', title: '11.4 Open addressing', page: 278 },
    { type: 'chapter', title: '12. Binary Search Trees', page: 286 },
    { type: 'section', title: '12.1 What is a binary search tree?', page: 286 },
    { type: 'section', title: '12.2 Querying a binary search tree', page: 291 },
    { type: 'section', title: '12.3 Insertion and deletion', page: 297 },
    { type: 'chapter', title: '13. Red-Black Trees', page: 308 },
    { type: 'section', title: '13.1 Properties of red-black trees', page: 308 },
    { type: 'section', title: '13.2 Rotations', page: 313 },
    { type: 'section', title: '13.3 Insertion', page: 317 },
    { type: 'section', title: '13.4 Deletion', page: 329 },
    { type: 'chapter', title: '14. Augmenting Data Structures', page: 339 },
    { type: 'section', title: '14.1 Dynamic order statistics', page: 339 },
    { type: 'section', title: '14.2 How to augment a data structure', page: 346 },
    { type: 'section', title: '14.3 Interval trees', page: 351 },

    { type: 'part', title: 'PART IV: ADVANCED DESIGN TECHNIQUES' },
    { type: 'chapter', title: '15. Dynamic Programming', page: 359 },
    { type: 'section', title: '15.1 Rod cutting', page: 359 },
    { type: 'section', title: '15.2 Matrix-chain multiplication', page: 371 },
    { type: 'section', title: '15.3 Elements of dynamic programming', page: 384 },
    { type: 'section', title: '15.4 Longest common subsequence', page: 394 },
    { type: 'section', title: '15.5 Optimal binary search trees', page: 404 },
    { type: 'chapter', title: '16. Greedy Algorithms', page: 414 },
    { type: 'section', title: '16.1 An activity-selection problem', page: 414 },
    { type: 'section', title: '16.2 Elements of the greedy strategy', page: 422 },
    { type: 'section', title: '16.3 Huffman codes', page: 429 },
    { type: 'chapter', title: '17. Amortized Analysis', page: 451 },
    { type: 'section', title: '17.1 Aggregate analysis', page: 451 },
    { type: 'section', title: '17.2 The accounting method', page: 457 },
    { type: 'section', title: '17.3 The potential method', page: 462 },
    { type: 'section', title: '17.4 Dynamic tables', page: 469 },

    { type: 'part', title: 'PART V: ADVANCED DATA STRUCTURES' },
    { type: 'chapter', title: '18. B-Trees', page: 484 },
    { type: 'section', title: '18.1 Definition of B-trees', page: 484 },
    { type: 'section', title: '18.2 Basic operations on B-trees', page: 491 },
    { type: 'section', title: '18.3 Deleting a key from a B-tree', page: 501 },
    { type: 'chapter', title: '19. Fibonacci Heaps', page: 505 },
    { type: 'section', title: '19.1 Structure of Fibonacci heaps', page: 506 },
    { type: 'section', title: '19.2 Mergeable-heap operations', page: 509 },
    { type: 'section', title: '19.3 Decreasing a key and deleting a node', page: 518 },
    { type: 'section', title: '19.4 Bounding the maximum degree', page: 523 },
    { type: 'chapter', title: '20. van Emde Boas Trees', page: 531 },
    { type: 'section', title: '20.1 Preliminary approaches', page: 532 },
    { type: 'section', title: '20.2 A recursive structure', page: 537 },
    { type: 'section', title: '20.3 The van Emde Boas tree', page: 545 },
    { type: 'chapter', title: '21. Data Structures for Disjoint Sets', page: 561 },
    { type: 'section', title: '21.1 Disjoint-set operations', page: 561 },
    { type: 'section', title: '21.2 Linked-list representation', page: 566 },
    { type: 'section', title: '21.3 Disjoint-set forests', page: 571 },
    { type: 'section', title: '21.4 Analysis of union by rank with path compression', page: 579 },

    { type: 'part', title: 'PART VI: GRAPH ALGORITHMS' },
    { type: 'chapter', title: '22. Elementary Graph Algorithms', page: 589 },
    { type: 'section', title: '22.1 Representations of graphs', page: 589 },
    { type: 'section', title: '22.2 Breadth-first search', page: 595 },
    { type: 'section', title: '22.3 Depth-first search', page: 604 },
    { type: 'section', title: '22.4 Topological sort', page: 613 },
    { type: 'section', title: '22.5 Strongly connected components', page: 617 },
    { type: 'chapter', title: '23. Minimum Spanning Trees', page: 624 },
    { type: 'section', title: '23.1 Growing a minimum spanning tree', page: 624 },
    { type: 'section', title: '23.2 Kruskal and Prim algorithms', page: 631 },
    { type: 'chapter', title: '24. Single-Source Shortest Paths', page: 643 },
    { type: 'section', title: '24.1 Bellman-Ford algorithm', page: 643 },
    { type: 'section', title: '24.2 Single-source shortest paths in DAGs', page: 652 },
    { type: 'section', title: '24.3 Dijkstra\'s algorithm', page: 657 },
    { type: 'section', title: '24.4 Difference constraints', page: 669 },
    { type: 'section', title: '24.5 Proofs of shortest-paths properties', page: 676 },
    { type: 'chapter', title: '25. All-Pairs Shortest Paths', page: 684 },
    { type: 'section', title: '25.1 Shortest paths and matrix multiplication', page: 684 },
    { type: 'section', title: '25.2 Floyd-Warshall algorithm', page: 691 },
    { type: 'section', title: '25.3 Johnson\'s algorithm', page: 699 },
    { type: 'chapter', title: '26. Maximum Flow', page: 708 },
    { type: 'section', title: '26.1 Flow networks', page: 708 },
    { type: 'section', title: '26.2 Ford-Fulkerson method', page: 721 },
    { type: 'section', title: '26.3 Maximum bipartite matching', page: 756 },

    { type: 'part', title: 'PART VII: SELECTED TOPICS' },
    { type: 'chapter', title: '27. Multithreaded Algorithms', page: 772 },
    { type: 'section', title: '27.1 The basics of dynamic multithreading', page: 773 },
    { type: 'section', title: '27.2 Multithreaded matrix multiplication', page: 793 },
    { type: 'section', title: '27.3 Multithreaded merge sort', page: 800 },
    { type: 'chapter', title: '28. Matrix Operations', page: 813 },
    { type: 'section', title: '28.1 Solving systems of linear equations', page: 813 },
    { type: 'section', title: '28.2 Inverting matrices', page: 828 },
    { type: 'section', title: '28.3 Symmetric positive-definite matrices', page: 833 },
    { type: 'chapter', title: '29. Linear Programming', page: 843 },
    { type: 'section', title: '29.1 Standard and slack forms', page: 850 },
    { type: 'section', title: '29.2 Formulating problems as linear programs', page: 859 },
    { type: 'section', title: '29.3 The simplex algorithm', page: 864 },
    { type: 'chapter', title: '30. Polynomials and the FFT', page: 898 },
    { type: 'section', title: '30.1 Representing polynomials', page: 899 },
    { type: 'section', title: '30.2 The DFT and FFT', page: 906 },
    { type: 'section', title: '30.3 Efficient FFT implementations', page: 915 },
    { type: 'chapter', title: '31. Number-Theoretic Algorithms', page: 926 },
    { type: 'section', title: '31.1 Elementary number-theoretic notions', page: 926 },
    { type: 'section', title: '31.2 Greatest common divisor', page: 933 },
    { type: 'section', title: '31.3 Modular arithmetic', page: 939 },
    { type: 'section', title: '31.4 Solving modular linear equations', page: 946 },
    { type: 'section', title: '31.5 The Chinese remainder theorem', page: 950 },
    { type: 'section', title: '31.6 Powers of an element', page: 954 },
    { type: 'section', title: '31.7 The RSA public-key cryptosystem', page: 958 },
    { type: 'section', title: '31.8 Primality testing', page: 965 },
    { type: 'section', title: '31.9 Integer factorization', page: 975 },
    { type: 'chapter', title: '32. String Matching', page: 985 },
    { type: 'section', title: '32.1 The naive string-matching algorithm', page: 985 },
    { type: 'section', title: '32.2 The Rabin-Karp algorithm', page: 989 },
    { type: 'section', title: '32.3 String matching with finite automata', page: 995 },
    { type: 'section', title: '32.4 The Knuth-Morris-Pratt algorithm', page: 1002 },
    { type: 'chapter', title: '33. Computational Geometry', page: 1014 },
    { type: 'section', title: '33.1 Line-segment properties', page: 1015 },
    { type: 'section', title: '33.2 Determining whether any pair of segments intersects', page: 1021 },
    { type: 'section', title: '33.3 Finding the convex hull', page: 1029 },
    { type: 'section', title: '33.4 Finding the closest pair of points', page: 1039 },
    { type: 'chapter', title: '34. NP-Completeness', page: 1048 },
    { type: 'section', title: '34.1 Polynomial time', page: 1048 },
    { type: 'section', title: '34.2 Polynomial-time verification', page: 1058 },
    { type: 'section', title: '34.3 NP-completeness and reducibility', page: 1066 },
    { type: 'section', title: '34.4 NP-completeness proofs', page: 1076 },
    { type: 'section', title: '34.5 NP-complete problems', page: 1086 },
    { type: 'chapter', title: '35. Approximation Algorithms', page: 1106 },
    { type: 'section', title: '35.1 The vertex-cover problem', page: 1108 },
    { type: 'section', title: '35.2 The traveling-salesman problem', page: 1111 },
    { type: 'section', title: '35.3 The set-covering problem', page: 1117 },
    { type: 'section', title: '35.4 Randomization and linear programming', page: 1123 },
    { type: 'section', title: '35.5 The subset-sum problem', page: 1128 },

    { type: 'part', title: 'PART VIII: APPENDIX' },
    { type: 'chapter', title: 'A. Summations', page: 1145 },
    { type: 'chapter', title: 'B. Sets, Relations, Functions, Graphs, Trees', page: 1158 },
    { type: 'chapter', title: 'C. Counting and Probability', page: 1183 },
    { type: 'chapter', title: 'D. Matrices', page: 1217 },
];

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', init);

async function init() {
    // Load manifest
    try {
        const manifest = await fetch('data/manifest.json').then(r => r.json());
        State.manifest = manifest;
        State.totalPages = manifest.totalPages;
    } catch (e) {
        console.warn('Could not load manifest, using defaults');
    }

    loadPage(currentPage);
    setView(currentView);
    setupEventListeners();
    updateUI();
}

function setupEventListeners() {
    // Menu trigger
    document.getElementById('menuTrigger').addEventListener('click', toggleMenu);
    document.getElementById('menuOverlay').addEventListener('click', closeMenu);

    // Navigation
    document.getElementById('prevBtn').addEventListener('click', () => navigate(-1));
    document.getElementById('nextBtn').addEventListener('click', () => navigate(1));
    document.getElementById('pageInput').addEventListener('change', (e) => goToPage(parseInt(e.target.value)));

    // Search
    document.getElementById('searchInput').addEventListener('input', (e) => handleSearch(e.target.value));

    // TOC
    document.getElementById('tocTrigger').addEventListener('click', toggleTOC);
    document.getElementById('tocOverlay').addEventListener('click', closeTOC);
    document.getElementById('tocClose').addEventListener('click', closeTOC);
    document.getElementById('tocSearch').addEventListener('input', (e) => filterTOC(e.target.value));

    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboard);

    // Render TOC
    renderTOC();
}

// ==================== MENU ====================
function toggleMenu() {
    menuOpen = !menuOpen;
    document.getElementById('menuTrigger').classList.toggle('active', menuOpen);
    document.getElementById('contextMenu').classList.toggle('active', menuOpen);
    document.getElementById('menuOverlay').classList.toggle('active', menuOpen);
}

function closeMenu() {
    menuOpen = false;
    document.getElementById('menuTrigger').classList.remove('active');
    document.getElementById('contextMenu').classList.remove('active');
    document.getElementById('menuOverlay').classList.remove('active');
}

// ==================== TOC SIDEBAR ====================
function toggleTOC() {
    tocOpen = !tocOpen;
    document.getElementById('tocSidebar').classList.toggle('active', tocOpen);
    document.getElementById('tocOverlay').classList.toggle('active', tocOpen);
    if (tocOpen) {
        updateTOCHighlight();
        document.getElementById('tocSearch').focus();
    }
}

function closeTOC() {
    tocOpen = false;
    document.getElementById('tocSidebar').classList.remove('active');
    document.getElementById('tocOverlay').classList.remove('active');
}

function renderTOC(filter = '') {
    const container = document.getElementById('tocContent');
    const lowerFilter = filter.toLowerCase();

    let html = '';
    let lastPart = '';

    for (const item of TOC_DATA) {
        if (item.type === 'part') {
            if (!filter || TOC_DATA.some(i =>
                (i.type === 'chapter' || i.type === 'section') &&
                i.title.toLowerCase().includes(lowerFilter)
            )) {
                html += `<div class="toc-part">${item.title}</div>`;
            }
            lastPart = item.title;
        } else if (item.type === 'chapter') {
            if (!filter || item.title.toLowerCase().includes(lowerFilter)) {
                html += `<div class="toc-chapter" data-page="${item.page}" onclick="window.tocGoToPage(${item.page})">
                    <span>${item.title}</span>
                    <span class="page-num">p.${item.page}</span>
                </div>`;
            }
        } else if (item.type === 'section') {
            if (!filter || item.title.toLowerCase().includes(lowerFilter)) {
                html += `<div class="toc-section" data-page="${item.page}" onclick="window.tocGoToPage(${item.page})">
                    <span>${item.title}</span>
                    <span class="page-num">${item.page}</span>
                </div>`;
            }
        }
    }

    container.innerHTML = html;
    updateTOCHighlight();
}

function filterTOC(query) {
    renderTOC(query);
}

function updateTOCHighlight() {
    // Find current section based on page
    document.querySelectorAll('.toc-section, .toc-chapter').forEach(el => {
        el.classList.remove('current');
    });

    // Find the section/chapter that contains the current page
    let currentItem = null;
    for (let i = TOC_DATA.length - 1; i >= 0; i--) {
        const item = TOC_DATA[i];
        if ((item.type === 'section' || item.type === 'chapter') && item.page <= currentPage) {
            currentItem = item;
            break;
        }
    }

    if (currentItem) {
        const el = document.querySelector(`.toc-section[data-page="${currentItem.page}"], .toc-chapter[data-page="${currentItem.page}"]`);
        if (el) {
            el.classList.add('current');
            // Scroll into view if TOC is open
            if (tocOpen) {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }
}

window.tocGoToPage = function(page) {
    goToPage(page);
    closeTOC();
};

// ==================== NAVIGATION ====================
function navigate(delta) {
    const newPage = currentPage + delta;
    if (newPage >= 1 && newPage <= TOTAL_PAGES) {
        goToPage(newPage);
    }
}

function goToPage(page) {
    if (page < 1 || page > TOTAL_PAGES) return;
    currentPage = page;
    loadPage(page);
    updateUI();
    updateTOCHighlight();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateUI() {
    // Progress bar
    const progress = (currentPage / TOTAL_PAGES) * 100;
    document.getElementById('progressBar').style.width = `${progress}%`;

    // Page badge
    document.getElementById('pageBadge').textContent = `Page ${currentPage} of ${TOTAL_PAGES}`;

    // Menu page input
    document.getElementById('pageInput').value = currentPage;

    // Menu page title
    const data = pageCache[currentPage];
    document.getElementById('menuPageTitle').textContent = data ? data.title : `Page ${currentPage}`;

    // Nav buttons
    document.getElementById('prevBtn').disabled = currentPage === 1;
    document.getElementById('nextBtn').disabled = currentPage === TOTAL_PAGES;
}

// ==================== PAGE LOADING ====================
async function loadPage(page) {
    const reader = document.getElementById('reader');

    // Load page data if not cached
    if (!pageCache[page]) {
        try {
            const paddedNum = String(page).padStart(4, '0');
            const data = await fetch(`data/pages/page-${paddedNum}.json`).then(r => r.json());
            pageCache[page] = data;
        } catch (e) {
            // Page data not available
            pageCache[page] = null;
        }
    }

    const data = pageCache[page];

    const zoomButtonsHTML = ZOOM_LEVELS.map(level =>
        `<button class="zoom-btn ${currentZoom === level ? 'active' : ''}" onclick="window.setZoom(${level})">${level}%</button>`
    ).join('');

    const imageHTML = `
        <div class="image-view ${currentView === 'image' ? '' : 'hidden'}" id="imageView">
            <div class="zoom-trigger"></div>
            <div class="zoom-controls">
                <span>Zoom</span>
                ${zoomButtonsHTML}
            </div>
            <img src="../clrs_pages/clrs-${String(page).padStart(4, '0')}.png"
                 alt="Page ${page}"
                 class="zoom-${currentZoom}"
                 id="pageImage">
        </div>
    `;

    const textHTML = data ? `
        <div class="text-view ${currentView === 'text' ? 'active' : ''}" id="textView">
            ${data.content}
        </div>
    ` : `
        <div class="text-view ${currentView === 'text' ? 'active' : ''}" id="textView">
            <div class="article-header">
                <div class="section-label">Page ${page}</div>
                <h1>Content</h1>
            </div>
            <div class="original-content">
                <p>Full transcription and analysis for this page is available in the image view. Use the menu or press <kbd>V</kbd> to switch views.</p>
            </div>
        </div>
    `;

    reader.innerHTML = imageHTML + textHTML;

    // Update menu title after loading
    document.getElementById('menuPageTitle').textContent = data ? data.title : `Page ${page}`;
}

// ==================== VIEW TOGGLE ====================
function setView(view) {
    currentView = view;
    localStorage.setItem('readerView', view);

    const imageView = document.getElementById('imageView');
    const textView = document.getElementById('textView');

    if (imageView) imageView.classList.toggle('hidden', view !== 'image');
    if (textView) textView.classList.toggle('active', view === 'text');

    // Update menu items
    document.getElementById('viewImage').classList.toggle('active', view === 'image');
    document.getElementById('viewText').classList.toggle('active', view === 'text');

    closeMenu();
}

function toggleView() {
    setView(currentView === 'image' ? 'text' : 'image');
}

// ==================== IMAGE ZOOM ====================
window.setZoom = function(level) {
    currentZoom = level;
    localStorage.setItem('readerZoom', level);

    const img = document.getElementById('pageImage');
    if (img) {
        // Remove all zoom classes
        ZOOM_LEVELS.forEach(l => img.classList.remove(`zoom-${l}`));
        // Add current zoom class
        img.classList.add(`zoom-${level}`);
    }

    // Update button states
    document.querySelectorAll('.zoom-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent === `${level}%`);
    });
}

function openFullscreen() {
    window.open(`../clrs_pages/clrs-${String(currentPage).padStart(4, '0')}.png`, '_blank');
    closeMenu();
}

// ==================== SEARCH ====================
async function handleSearch(query) {
    const container = document.getElementById('searchResults');
    if (query.length < 2) {
        container.innerHTML = '';
        return;
    }

    const results = [];
    const lowerQuery = query.toLowerCase();

    // Search through manifest
    if (State.manifest && State.manifest.pages) {
        for (const page of State.manifest.pages) {
            if (page.title.toLowerCase().includes(lowerQuery)) {
                results.push({ page: page.page, title: page.title });
            }
        }
    }

    // Also search cached pages for content
    for (const [pageNum, data] of Object.entries(pageCache)) {
        if (data && !results.find(r => r.page === parseInt(pageNum))) {
            if (data.content.toLowerCase().includes(lowerQuery)) {
                results.push({ page: parseInt(pageNum), title: data.title });
            }
        }
    }

    if (results.length > 0) {
        container.innerHTML = results.slice(0, 5).map(r => `
            <div class="search-result" onclick="window.appGoToPage(${r.page})">
                <div class="search-result-page">Page ${r.page}</div>
                <div>${r.title}</div>
            </div>
        `).join('');
    } else {
        container.innerHTML = '<div class="search-result">No results</div>';
    }
}

// ==================== KEYBOARD SHORTCUTS ====================
function handleKeyboard(e) {
    // Don't trigger if typing in input
    if (e.target.tagName === 'INPUT') return;

    switch(e.key) {
        case 'ArrowLeft':
            navigate(-1);
            break;
        case 'ArrowRight':
            navigate(1);
            break;
        case 'v':
        case 'V':
            toggleView();
            break;
        case 'm':
        case 'M':
            toggleMenu();
            break;
        case 't':
        case 'T':
            toggleTOC();
            break;
        case 'Escape':
            closeMenu();
            closeTOC();
            break;
        // Zoom shortcuts
        case '+':
        case '=':
            zoomIn();
            break;
        case '-':
        case '_':
            zoomOut();
            break;
        case '0':
            window.setZoom(100);
            break;
        // Number keys 1-8 for zoom levels
        case '1':
            window.setZoom(70);
            break;
        case '2':
            window.setZoom(80);
            break;
        case '3':
            window.setZoom(90);
            break;
        case '4':
            window.setZoom(100);
            break;
        case '5':
            window.setZoom(110);
            break;
        case '6':
            window.setZoom(120);
            break;
        case '7':
            window.setZoom(130);
            break;
        case '8':
            window.setZoom(140);
            break;
        // Go to page
        case 'g':
        case 'G':
            document.getElementById('pageInput').focus();
            toggleMenu();
            break;
        // Home/End
        case 'Home':
            goToPage(1);
            break;
        case 'End':
            goToPage(TOTAL_PAGES);
            break;
    }
}

function zoomIn() {
    const idx = ZOOM_LEVELS.indexOf(currentZoom);
    if (idx < ZOOM_LEVELS.length - 1) {
        window.setZoom(ZOOM_LEVELS[idx + 1]);
    }
}

function zoomOut() {
    const idx = ZOOM_LEVELS.indexOf(currentZoom);
    if (idx > 0) {
        window.setZoom(ZOOM_LEVELS[idx - 1]);
    }
}

// Expose functions to window for onclick handlers
window.appGoToPage = function(page) {
    goToPage(page);
    closeMenu();
};
window.setView = setView;
window.openFullscreen = openFullscreen;
