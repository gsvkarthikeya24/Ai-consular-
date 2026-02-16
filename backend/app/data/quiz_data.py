"""
Branch Selection Quiz Data
Contains 10 questions designed to help students choose an engineering branch.
"""

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What excites you more when you see a new gadget like a smartphone?",
        "options": [
            {"id": "a", "text": "The apps, user interface, and software features.", "points": {"CSE": 3, "ECE": 1}},
            {"id": "b", "text": "The circuit design, processor speed, and hardware components.", "points": {"ECE": 3, "EEE": 2}},
            {"id": "c", "text": "The physical build quality, hinge mechanism, or cooling system.", "points": {"ME": 3, "Civil": 1}},
            {"id": "d", "text": "The battery technology and power management.", "points": {"EEE": 3, "ECE": 1}}
        ],
        "mentor_guidance": "Think about whether you enjoy the digital experience or the physical engineering more."
    },
    {
        "id": 2,
        "question": "Which of these school subjects did you enjoy the most?",
        "options": [
            {"id": "a", "text": "Logic and Computer Science.", "points": {"CSE": 3}},
            {"id": "b", "text": "Physics (Electricity and Magnetism).", "points": {"EEE": 3, "ECE": 2}},
            {"id": "c", "text": "Mathematics and Geometry.", "points": {"Civil": 3, "CSE": 1}},
            {"id": "d", "text": "Physics (Mechanics and Thermodynamics).", "points": {"ME": 3}}
        ],
        "mentor_guidance": "Your favorite subjects often point toward your natural engineering inclination."
    },
    {
        "id": 3,
        "question": "If you were to build a robot, which part would you want to work on?",
        "options": [
            {"id": "a", "text": "Writing the code to make it think and move autonomously.", "points": {"CSE": 3}},
            {"id": "b", "text": "Designing its brain (the microcontrollers and circuit boards).", "points": {"ECE": 3, "EEE": 1}},
            {"id": "c", "text": "Building its physical frame, gears, and motors.", "points": {"ME": 3}},
            {"id": "d", "text": "Connecting the sensors and ensuring stable power supply.", "points": {"EEE": 3, "ECE": 1}}
        ],
        "mentor_guidance": "Robotics is a mix of all branches, but your preferred role defines your speciality."
    },
    {
        "id": 4,
        "question": "How do you prefer to solve a complex problem?",
        "options": [
            {"id": "a", "text": "Breaking it down into logical steps and algorithms.", "points": {"CSE": 3}},
            {"id": "b", "text": "Understanding the underlying signals and connectivity.", "points": {"ECE": 3}},
            {"id": "c", "text": "Visualizing the physical structure and forces involved.", "points": {"Civil": 3, "ME": 2}},
            {"id": "d", "text": "Analyzing the energy flow and power efficiency.", "points": {"EEE": 3}}
        ],
        "mentor_guidance": "Computational logic vs physical visualization is a key differentiator between branches."
    },
    {
        "id": 5,
        "question": "Which of these legendary figures inspires you more?",
        "options": [
            {"id": "a", "text": "Mark Zuckerberg or Alan Turing.", "points": {"CSE": 3}},
            {"id": "b", "text": "Nikola Tesla.", "points": {"EEE": 3, "ECE": 1}},
            {"id": "c", "text": "Henry Ford or Elon Musk (SpaceX hardware).", "points": {"ME": 3}},
            {"id": "d", "text": "E. Sreedharan (The Metro Man).", "points": {"Civil": 3}}
        ],
        "mentor_guidance": "Heroes often reflect our own aspirations and professional interests."
    },
    {
        "id": 6,
        "question": "When you think of a 'Smart City', what is the most important component?",
        "options": [
            {"id": "a", "text": "The AI that manages traffic and urban services.", "points": {"CSE": 3}},
            {"id": "b", "text": "The high-speed 5G connectivity and sensors everywhere.", "points": {"ECE": 3}},
            {"id": "c", "text": "The sustainable buildings and efficient transport infrastructure.", "points": {"Civil": 3}},
            {"id": "d", "text": "The 24/7 renewable power grid and energy storage.", "points": {"EEE": 3}}
        ],
        "mentor_guidance": "Smart cities are integrated systems where every branch plays a role."
    },
    {
        "id": 7,
        "question": "What kind of 'puzzles' do you enjoy solving?",
        "options": [
            {"id": "a", "text": "Logical puzzles and riddles.", "points": {"CSE": 3}},
            {"id": "b", "text": "Fixing broken electronics or gadgets.", "points": {"ECE": 3, "EEE": 1}},
            {"id": "c", "text": "Assembling LEGO or IKEA furniture.", "points": {"ME": 3, "Civil": 2}},
            {"id": "d", "text": "Optimizing a process to make it more efficient.", "points": {"ME": 2, "EEE": 2}}
        ],
        "mentor_guidance": "The way you engage with physical or logical puzzles reveals your strengths."
    },
    {
        "id": 8,
        "question": "What is your idea of a perfect work environment?",
        "options": [
            {"id": "a", "text": "Sitting with a powerful computer, coding from anywhere.", "points": {"CSE": 3}},
            {"id": "b", "text": "A high-tech lab with oscilloscopes and circuit testing kits.", "points": {"ECE": 3, "EEE": 1}},
            {"id": "c", "text": "A manufacturing shop floor with heavy machinery.", "points": {"ME": 3}},
            {"id": "d", "text": "Out on a construction site, seeing structures rise.", "points": {"Civil": 3}}
        ],
        "mentor_guidance": "Your comfort zone—office vs field vs lab—is crucial for long-term happiness."
    },
    {
        "id": 9,
        "question": "How important is 'Visual Impact' in your work?",
        "options": [
            {"id": "a", "text": "I care about how the information is presented digitally.", "points": {"CSE": 3}},
            {"id": "b", "text": "I care about making things smaller and more efficient.", "points": {"ECE": 3}},
            {"id": "c", "text": "I care about how a physical product looks and feels.", "points": {"ME": 3}},
            {"id": "d", "text": "I care about the scale and aesthetic of a structure.", "points": {"Civil": 3}}
        ],
        "mentor_guidance": "Engineering beauty ranges from clean code to massive bridges."
    },
    {
        "id": 10,
        "question": "In a movie like 'Iron Man', what interests you most?",
        "options": [
            {"id": "a", "text": "Jarvis - the AI system.", "points": {"CSE": 3}},
            {"id": "b", "text": "The HUD and the communication systems.", "points": {"ECE": 3}},
            {"id": "c", "text": "The suit's flight mechanics and armor design.", "points": {"ME": 3}},
            {"id": "d", "text": "The Arc Reactor - the clean energy source.", "points": {"EEE": 3}}
        ],
        "mentor_guidance": "Pop culture often mirrors real engineering disciplines."
    }
]

BRANCH_DESCRIPTIONS = {
    "CSE": "Computer Science & Engineering: Focuses on software, algorithms, AI, and digital systems. Best for logical thinkers who love coding.",
    "ECE": "Electronics & Communication Engineering: Deals with electronics, signal processing, and telecommunications. Best for those who love both hardware and software.",
    "EEE": "Electrical & Electronics Engineering: Focuses on power systems, electrical machines, and energy. Best for those interested in energy and electricity.",
    "ME": "Mechanical Engineering: Deals with machines, manufacturing, and thermodynamics. Best for those who love physical products and machinery.",
    "Civil": "Civil Engineering: Focuses on infrastructure, buildings, and construction. Best for those who want to build the physical world around them."
}
