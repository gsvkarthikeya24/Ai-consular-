// ============================================
// ENGINEERING CAREER GUIDANCE - JAVASCRIPT
// Interactive functionality and quiz logic
// ============================================

// Navigation scroll effect
const navbar = document.getElementById('navbar');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navLinks = document.getElementById('navLinks');

window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// Mobile menu toggle
mobileMenuToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('active');
  });
});

// ============================================
// SCROLL ANIMATIONS
// ============================================
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, observerOptions);

// Observe all fade-in elements
document.querySelectorAll('.fade-in').forEach(el => {
  observer.observe(el);
});

// ============================================
// CAREER OUTCOMES ACCORDION
// ============================================
document.querySelectorAll('.outcome-header').forEach(header => {
  header.addEventListener('click', () => {
    const card = header.parentElement;
    const isExpanded = card.classList.contains('expanded');

    // Close all cards
    document.querySelectorAll('.outcome-card').forEach(c => {
      c.classList.remove('expanded');
    });

    // Toggle current card
    if (!isExpanded) {
      card.classList.add('expanded');
    }
  });
});

// ============================================
// QUIZ FUNCTIONALITY
// ============================================

const quizData = {
  questions: [
    {
      id: 1,
      question: "What excites you the most?",
      options: [
        { text: "Designing buildings and infrastructure", branches: ["civil"] },
        { text: "Writing code and creating software", branches: ["cse"] },
        { text: "Protecting systems from cyber threats", branches: ["cyber"] },
        { text: "Working with machines and engines", branches: ["mechanical"] },
        { text: "Power systems and renewable energy", branches: ["eee"] },
        { text: "Electronics and communication devices", branches: ["ece"] },
        { text: "Chemical processes and materials", branches: ["chemical"] },
        { text: "Aircraft, spacecraft, and aviation", branches: ["aerospace"] }
      ]
    },
    {
      id: 2,
      question: "What type of problems do you enjoy solving?",
      options: [
        { text: "Structural and design challenges", branches: ["civil"] },
        { text: "Logic puzzles and algorithms", branches: ["cse", "cyber"] },
        { text: "Security and protection issues", branches: ["cyber"] },
        { text: "Mechanical and motion problems", branches: ["mechanical"] },
        { text: "Energy and power distribution", branches: ["eee"] },
        { text: "Circuit design and signals", branches: ["ece"] },
        { text: "Material transformation processes", branches: ["chemical"] },
        { text: "Aerodynamics and flight mechanics", branches: ["aerospace", "mechanical"] }
      ]
    },
    {
      id: 3,
      question: "Which activities interest you?",
      options: [
        { text: "Visiting construction sites and understanding infrastructure", branches: ["civil"] },
        { text: "Building websites, apps, or AI projects", branches: ["cse"] },
        { text: "Learning about hacking and network security", branches: ["cyber"] },
        { text: "Tinkering with machines and automobiles", branches: ["mechanical"] },
        { text: "Experimenting with electrical circuits", branches: ["eee", "ece"] },
        { text: "Working with IoT and embedded systems", branches: ["ece"] },
        { text: "Conducting chemistry experiments", branches: ["chemical"] },
        { text: "Exploring aviation, rockets, and space technology", branches: ["aerospace"] }
      ]
    },
    {
      id: 4,
      question: "What's your dream work environment?",
      options: [
        { text: "On-site at construction projects", branches: ["civil"] },
        { text: "Tech company or startup office", branches: ["cse", "cyber"] },
        { text: "Security operations center (SOC)", branches: ["cyber"] },
        { text: "Manufacturing plant or R&D lab", branches: ["mechanical", "chemical"] },
        { text: "Power plants or energy companies", branches: ["eee"] },
        { text: "Electronics design lab or telecom company", branches: ["ece"] },
        { text: "Chemical plant or pharmaceutical company", branches: ["chemical"] },
        { text: "Aerospace company, ISRO, or aircraft hangar", branches: ["aerospace"] }
      ]
    },
    {
      id: 5,
      question: "Which skills do you want to develop?",
      options: [
        { text: "CAD design and project management", branches: ["civil"] },
        { text: "Programming and software development", branches: ["cse"] },
        { text: "Ethical hacking and penetration testing", branches: ["cyber"] },
        { text: "Mechanical design and robotics", branches: ["mechanical"] },
        { text: "Power systems and renewable energy", branches: ["eee"] },
        { text: "VLSI design and communication systems", branches: ["ece"] },
        { text: "Process engineering and quality control", branches: ["chemical"] },
        { text: "Aircraft design and propulsion systems", branches: ["aerospace"] }
      ]
    }
  ]
};

const branchInfo = {
  civil: {
    name: "Civil Engineering",
    description: "Designing and building infrastructure like roads, bridges, buildings, and dams.",
    icon: "🏗️"
  },
  cse: {
    name: "Computer Science Engineering",
    description: "Developing software, applications, AI systems, and digital solutions.",
    icon: "💻"
  },
  cyber: {
    name: "Cyber Security Engineering",
    description: "Protecting digital systems, networks, and data from cyber threats.",
    icon: "🔐"
  },
  mechanical: {
    name: "Mechanical Engineering",
    description: "Designing and maintaining machines, engines, and mechanical systems.",
    icon: "⚙️"
  },
  eee: {
    name: "Electrical & Electronics Engineering",
    description: "Working with power generation, electrical systems, and renewable energy.",
    icon: "⚡"
  },
  ece: {
    name: "Electronics & Communication Engineering",
    description: "Designing electronic devices, communication systems, and IoT solutions.",
    icon: "📡"
  },
  chemical: {
    name: "Chemical Engineering",
    description: "Managing industrial chemical processes and material production.",
    icon: "🧪"
  },
  aerospace: {
    name: "Aerospace Engineering",
    description: "Designing aircraft, spacecraft, satellites, and defense systems.",
    icon: "✈️"
  }
};

let currentQuestion = 0;
let answers = [];

const quizModal = document.getElementById('quizModal');
const startQuizBtn = document.getElementById('startQuizBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const quizContainer = document.getElementById('quizContainer');

// Start quiz
startQuizBtn.addEventListener('click', () => {
  quizModal.classList.add('active');
  currentQuestion = 0;
  answers = [];
  renderQuestion();
});

// Close modal
closeModalBtn.addEventListener('click', () => {
  quizModal.classList.remove('active');
});

// Close modal when clicking outside
quizModal.addEventListener('click', (e) => {
  if (e.target === quizModal) {
    quizModal.classList.remove('active');
  }
});

// Render current question
function renderQuestion() {
  const question = quizData.questions[currentQuestion];

  const html = `
    <div class="quiz-question">
      <h3>Question ${currentQuestion + 1} of ${quizData.questions.length}</h3>
      <p style="font-size: 1.25rem; color: var(--gray-700); margin-bottom: 1.5rem;">
        ${question.question}
      </p>
      <div class="quiz-options">
        ${question.options.map((option, index) => `
          <div class="quiz-option" data-index="${index}">
            ${option.text}
          </div>
        `).join('')}
      </div>
    </div>
    <div class="quiz-navigation">
      <button class="quiz-nav-button" id="prevBtn" ${currentQuestion === 0 ? 'disabled' : ''}>
        Previous
      </button>
      <button class="quiz-nav-button" id="nextBtn" disabled>
        ${currentQuestion === quizData.questions.length - 1 ? 'Show Results' : 'Next'}
      </button>
    </div>
  `;

  quizContainer.innerHTML = html;

  // Add event listeners to options
  document.querySelectorAll('.quiz-option').forEach(option => {
    option.addEventListener('click', () => {
      // Remove selected class from all options
      document.querySelectorAll('.quiz-option').forEach(opt => {
        opt.classList.remove('selected');
      });

      // Add selected class to clicked option
      option.classList.add('selected');

      // Store answer
      const optionIndex = parseInt(option.dataset.index);
      answers[currentQuestion] = question.options[optionIndex];

      // Enable next button
      document.getElementById('nextBtn').disabled = false;
    });
  });

  // Navigation buttons
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentQuestion > 0) {
        currentQuestion--;
        renderQuestion();
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentQuestion < quizData.questions.length - 1) {
        currentQuestion++;
        renderQuestion();
      } else {
        showResults();
      }
    });
  }

  // Pre-select answer if it exists
  if (answers[currentQuestion]) {
    const selectedIndex = question.options.indexOf(answers[currentQuestion]);
    if (selectedIndex !== -1) {
      document.querySelectorAll('.quiz-option')[selectedIndex].classList.add('selected');
      document.getElementById('nextBtn').disabled = false;
    }
  }
}

// Calculate and show results
function showResults() {
  const branchScores = {};

  // Initialize scores
  Object.keys(branchInfo).forEach(branch => {
    branchScores[branch] = 0;
  });

  // Calculate scores
  answers.forEach(answer => {
    answer.branches.forEach(branch => {
      branchScores[branch]++;
    });
  });

  // Sort branches by score
  const sortedBranches = Object.entries(branchScores)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3); // Get top 3

  const totalQuestions = quizData.questions.length;

  const resultsHtml = `
    <div class="quiz-results">
      <h3>Your Recommended Engineering Branches</h3>
      <p style="color: var(--gray-600); margin-bottom: 2rem;">
        Based on your interests and preferences, here are the top engineering branches for you:
      </p>
      <div class="recommended-branches">
        ${sortedBranches.map(([branch, score], index) => {
    const percentage = Math.round((score / totalQuestions) * 100);
    const info = branchInfo[branch];
    return `
            <div class="recommended-branch">
              <span class="match-score">${percentage}% Match</span>
              <h4>${index === 0 ? '🏆 ' : ''}${info.icon} ${info.name}</h4>
              <p style="color: var(--gray-600); margin: 0.5rem 0 0 0;">
                ${info.description}
              </p>
            </div>
          `;
  }).join('')}
      </div>
      <button class="quiz-nav-button" style="margin-top: 2rem;" onclick="location.reload()">
        Take Quiz Again
      </button>
    </div>
  `;

  quizContainer.innerHTML = resultsHtml;
}

// ============================================
// SMOOTH SCROLL FOR ALL LINKS
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// ============================================
// INITIALIZE ON LOAD
// ============================================
window.addEventListener('load', () => {
  // Trigger initial animations
  setTimeout(() => {
    document.querySelectorAll('.fade-in').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight) {
        el.classList.add('visible');
      }
    });
  }, 100);
});
