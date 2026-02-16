"""
GATE Preparation Data
Contains GATE exam topics, questions, and study materials
"""

GATE_SUBJECTS = {
    "CSE": [
        "Data Structures",
        "Algorithms",
        "Theory of Computation",
        "Compiler Design",
        "Operating Systems",
        "Computer Networks",
        "Database Management Systems",
        "Digital Logic",
        "Computer Organization and Architecture",
        "Discrete Mathematics",
        "Engineering Mathematics",
        "Programming and Data Structures"
    ],
    "ECE": [
        "Networks",
        "Electronic Devices",
        "Analog Circuits",
        "Digital Circuits",
        "Signals and Systems",
        "Control Systems",
        "Communications",
        "Electromagnetics",
        "Engineering Mathematics"
    ],
    "EEE": [
        "Electric Circuits",
        "Electromagnetic Fields",
        "Signals and Systems",
        "Electrical Machines",
        "Power Systems",
        "Control Systems",
        "Electrical and Electronic Measurements",
        "Analog and Digital Electronics",
        "Power Electronics"
    ],
    "ME": [
        "Engineering Mechanics",
        "Strength of Materials",
        "Theory of Machines",
        "Vibrations",
        "Machine Design",
        "Fluid Mechanics",
        "Heat Transfer",
        "Thermodynamics",
        "Manufacturing Engineering",
        "Industrial Engineering"
    ],
    "Civil": [
        "Structural Engineering",
        "Geotechnical Engineering",
        "Water Resources Engineering",
        "Environmental Engineering",
        "Transportation Engineering",
        "Surveying",
        "Engineering Mathematics"
    ]
}

# Sample GATE Questions for CSE
GATE_QUESTIONS_CSE = [
    {
        "subject": "Data Structures",
        "topic": "Binary Trees",
        "difficulty": "Medium",
        "question": "What is the maximum number of nodes in a binary tree of height h?",
        "options": [
            "2^h - 1",
            "2^(h+1) - 1",
            "2^h",
            "2^(h-1)"
        ],
        "correct_answer": 1,
        "explanation": "A binary tree of height h can have at most 2^(h+1) - 1 nodes. This occurs when the tree is a complete binary tree.",
        "marks": 2,
        "year": 2023
    },
    {
        "subject": "Algorithms",
        "topic": "Time Complexity",
        "difficulty": "Easy",
        "question": "What is the time complexity of binary search on a sorted array of n elements?",
        "options": [
            "O(n)",
            "O(log n)",
            "O(n log n)",
            "O(1)"
        ],
        "correct_answer": 1,
        "explanation": "Binary search divides the search space in half at each step, resulting in O(log n) time complexity.",
        "marks": 1,
        "year": 2023
    },
    {
        "subject": "Operating Systems",
        "topic": "Process Scheduling",
        "difficulty": "Medium",
        "question": "Which scheduling algorithm may cause starvation?",
        "options": [
            "First Come First Serve (FCFS)",
            "Round Robin (RR)",
            "Shortest Job First (SJF)",
            "Priority Scheduling"
        ],
        "correct_answer": 3,
        "explanation": "Priority Scheduling can cause starvation when high-priority processes continuously arrive, preventing low-priority processes from executing.",
        "marks": 2,
        "year": 2022
    },
    {
        "subject": "Database Management Systems",
        "topic": "Normalization",
        "difficulty": "Hard",
        "question": "A relation is in BCNF if and only if:",
        "options": [
            "Every determinant is a candidate key",
            "It is in 3NF",
            "It has no partial dependencies",
            "It has no transitive dependencies"
        ],
        "correct_answer": 0,
        "explanation": "A relation is in Boyce-Codd Normal Form (BCNF) if for every functional dependency X → Y, X is a superkey (candidate key).",
        "marks": 2,
        "year": 2022
    },
    {
        "subject": "Computer Networks",
        "topic": "TCP/IP",
        "difficulty": "Medium",
        "question": "What is the maximum size of a TCP segment?",
        "options": [
            "64 KB",
            "32 KB",
            "16 KB",
            "8 KB"
        ],
        "correct_answer": 0,
        "explanation": "The maximum TCP segment size is 64 KB (65,535 bytes) due to the 16-bit length field in the TCP header.",
        "marks": 2,
        "year": 2023
    },
    {
        "subject": "Theory of Computation",
        "topic": "Regular Languages",
        "difficulty": "Hard",
        "question": "Which of the following languages is NOT regular?",
        "options": [
            "L = {a^n b^n | n ≥ 0}",
            "L = {a^n | n ≥ 0}",
            "L = {ab, aabb, aaabbb}",
            "L = {a, b}*"
        ],
        "correct_answer": 0,
        "explanation": "L = {a^n b^n | n ≥ 0} is a context-free language but not regular, as it requires counting which cannot be done with finite automata.",
        "marks": 2,
        "year": 2021
    },
    {
        "subject": "Compiler Design",
        "topic": "Parsing",
        "difficulty": "Medium",
        "question": "Which parser is more powerful?",
        "options": [
            "LL(1)",
            "LR(0)",
            "SLR(1)",
            "LALR(1)"
        ],
        "correct_answer": 3,
        "explanation": "LALR(1) is more powerful than SLR(1), LR(0), and LL(1) parsers in terms of the class of grammars it can parse.",
        "marks": 2,
        "year": 2022
    },
    {
        "subject": "Digital Logic",
        "topic": "Boolean Algebra",
        "difficulty": "Easy",
        "question": "What is the simplified form of A'B + AB' + AB?",
        "options": [
            "A + B",
            "A'B'",
            "AB",
            "A ⊕ B"
        ],
        "correct_answer": 0,
        "explanation": "A'B + AB' + AB = A'B + A(B' + B) = A'B + A = A + B (using absorption law).",
        "marks": 1,
        "year": 2023
    }
]

# Study Resources
GATE_RESOURCES = [
    {
        "subject": "Data Structures",
        "resources": [
            {
                "title": "NPTEL - Data Structures",
                "type": "Video Lectures",
                "url": "https://nptel.ac.in/courses/106102064",
                "provider": "NPTEL"
            },
            {
                "title": "GeeksforGeeks - Data Structures",
                "type": "Articles & Practice",
                "url": "https://www.geeksforgeeks.org/data-structures/",
                "provider": "GeeksforGeeks"
            }
        ]
    },
    {
        "subject": "Algorithms",
        "resources": [
            {
                "title": "Introduction to Algorithms (CLRS)",
                "type": "Book",
                "url": "https://mitpress.mit.edu/books/introduction-algorithms",
                "provider": "MIT Press"
            },
            {
                "title": "NPTEL - Design and Analysis of Algorithms",
                "type": "Video Lectures",
                "url": "https://nptel.ac.in/courses/106101060",
                "provider": "NPTEL"
            }
        ]
    },
    {
        "subject": "Operating Systems",
        "resources": [
            {
                "title": "Operating System Concepts",
                "type": "Book",
                "url": "https://www.os-book.com/",
                "provider": "Silberschatz"
            },
            {
                "title": "NPTEL - Operating Systems",
                "type": "Video Lectures",
                "url": "https://nptel.ac.in/courses/106105214",
                "provider": "NPTEL"
            }
        ]
    }
]

# Previous Year Analysis
GATE_YEAR_ANALYSIS = {
    "2023": {
        "total_questions": 65,
        "total_marks": 100,
        "subject_wise_distribution": {
            "Engineering Mathematics": 13,
            "Data Structures": 8,
            "Algorithms": 7,
            "Theory of Computation": 6,
            "Compiler Design": 5,
            "Operating Systems": 7,
            "Computer Networks": 6,
            "Database Management Systems": 6,
            "Digital Logic": 4,
            "Computer Organization": 3
        },
        "difficulty_distribution": {
            "Easy": 20,
            "Medium": 30,
            "Hard": 15
        }
    },
    "2022": {
        "total_questions": 65,
        "total_marks": 100,
        "subject_wise_distribution": {
            "Engineering Mathematics": 13,
            "Data Structures": 7,
            "Algorithms": 8,
            "Theory of Computation": 5,
            "Compiler Design": 6,
            "Operating Systems": 6,
            "Computer Networks": 7,
            "Database Management Systems": 6,
            "Digital Logic": 4,
            "Computer Organization": 3
        },
        "difficulty_distribution": {
            "Easy": 18,
            "Medium": 32,
            "Hard": 15
        }
    }
}
