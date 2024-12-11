// Define la clase del chatbot
class CVChatbot {
    constructor() {
    this.context = {
    lastTopic: null,
    conversationHistory: [],
    followUpQuestions: {}
    };
   
    this.responses = {
    greeting: "👋 Hello! I am your CV assistant. How can I help you today?",
    help: {
    main: `I can assist you with the following topics:\n
    • CV/Resume Creation and Formatting
    • Cover Letter Writing
    • Skills Assessment and Optimization
    • Work Experience Documentation
    • Education and Qualifications
    • Personal Information Management
    • Job Search Strategy
    • Interview Preparation\n
    Just ask me about any of these topics for more details.`,
    followUp: ['Which topic interests you the most?', 'Would you like specific examples for any of these areas?']
    },
    greetings: {
    english: [
    "Hi there! How can I assist you with your CV today?",
    "Welcome! Ready to work on your CV?",
    "Hello! Let's make your CV stand out!",
    "Greetings! How may I help you with your resume?"
    ]
    },
    farewells: {
    english: [
    "Goodbye! Good luck with your CV!",
    "Take care! Feel free to return if you need more CV help!",
    "Farewell! Wishing you success with your job search!",
    "Bye! Come back anytime for more CV assistance!"
    ]
    },
    help: {
    main: `I can assist you with the following topics:\n
    • CV/Resume Creation and Formatting
    • Cover Letter Writing
    • Skills Assessment and Optimization
    • Work Experience Documentation
    • Education and Qualifications
    • Personal Information Management
    • Job Search Strategy
    • Interview Preparation\n
    Just ask me about any of these topics for more details.`,
    followUp: ['Which topic interests you the most?', 'Would you like specific examples for any of these areas?']
    },
   
    cv: {
    main: `Here are key strategies for an effective CV:\n
    1. Strategic Customization:
    • Tailor your CV for each specific position
    • Mirror the language from the job description
    • Prioritize relevant achievements\n
    2. Professional Presentation:
    • Maintain consistent formatting
    • Use clear, readable fonts (Arial, Calibri)
    • Include white space for readability\n
    3. Content Organization:
    • Place most important information first
    • Use bullet points for clarity
    • Keep to 1-2 pages maximum\n
    4. Achievement Focus:
    • Quantify results where possible
    • Use action verbs
    • Highlight specific contributions\n
    5. Technical Optimization:
    • Include industry-relevant keywords
    • Use ATS-friendly formatting
    • Save in requested file format`,
    followUp: ['Would you like specific examples of action verbs?', 'Do you need help with any particular section?']
    },
   
    experience: {
    main: `Optimize your work experience section with these strategies:\n
    1. Structure and Format:
    • Use consistent format: [Job Title] - [Company] - [Dates]
    • List positions in reverse chronological order
    • Include location when relevant\n
    2. Achievement Description:
    • Lead with strong action verbs
    • Focus on measurable results
    • Use format: Action → Task → Result\n
    3. Quantification:
    • Include specific metrics
    • Add percentages of improvement
    • Mention team sizes managed\n
    4. Relevancy:
    • Highlight transferable skills
    • Focus on achievements relevant to target role
    • Adjust description length based on relevance`,
    followUp: ['Would you like examples of quantified achievements?', 'Need help describing a specific role?']
    },
   
    skills: {
    main: `Create an impactful skills section with these guidelines:\n
    1. Technical Skills:
    • List relevant software and tools
    • Include proficiency levels
    • Group by category\n
    2. Soft Skills:
    • Focus on leadership and communication
    • Include problem-solving abilities
    • Highlight team collaboration\n
    3. Industry-Specific:
    • Add relevant certifications
    • Include specialized training
    • List industry tools mastery\n
    4. Organization:
    • Prioritize most relevant skills
    • Use clear categorization
    • Update regularly`,
    followUp: ['Would you like examples of how to rate your proficiency?', 'Need help organizing your skills by category?']
    },
   
    education: {
    main: `Structure your education section effectively:\n
    1. Core Information:
    • Degree and major
    • Institution name and location
    • Graduation date (or expected)
    • GPA if above 3.5\n
    2. Additional Elements:
    • Relevant coursework
    • Academic honors
    • Research projects
    • Study abroad experience\n
    3. Professional Development:
    • Certifications
    • Online courses
    • Workshops and seminars
    • Professional licenses`,
    followUp: ['Would you like help formatting your educational achievements?', 'Need advice on which courses to include?']
    },
   
    'personal information': {
    main: `Guidelines for personal information section:\n
    1. Essential Elements:
    • Full name (in larger font)
    • Professional email address
    • Phone number
    • Location (city and state/country)\n
    2. Optional Elements:
    • LinkedIn profile
    • Professional portfolio
    • Personal website
    • GitHub (for tech roles)\n
    3. Privacy Considerations:
    • Exclude age, marital status
    • Omit personal photos unless required
    • Use professional email format
    • Consider privacy when listing address`,
    followUp: ['Would you like help creating a professional email address?', 'Need guidance on social media profiles to include?']
    },
   
    'default': {
    main: `I'm not sure how to help with that query. Try asking about:\n• CV\n• Work experience\n• Skills\n• Education\n• Personal information\n\nOr type 'help' to see the available topics.`,
    followUp: ['Would you like to see the list of topics I can help with?', 'Can you rephrase your question?']
    },
    farewell: "It was great chatting with you! Feel free to reach out anytime if you have more questions. Have a wonderful day!"
    };
   
    this.keywords = {
    cv: ['cv', 'resumé', 'curriculum', 'vitae', 'resume', 'document', 'format', 'layout'],
    experience: ['experience', 'work', 'job', 'employment', 'position', 'career', 'history'],
    education: ['education', 'studies', 'degrees', 'training', 'qualifications', 'academic'],
    skills: ['skills', 'competencies', 'abilities', 'expertise', 'proficiencies', 'capabilities'],
    'personal information': ['personal', 'information', 'details', 'contact', 'data', 'profile'],
    };
    }
   
    getRandomResponse(responses) {
    return responses[Math.floor(Math.random() * responses.length)];
    }
   
    analyzeIntent(message) {
    message = message.toLowerCase().trim();
   
    if (message === 'help') {
    return 'help';
    }
   
    if (this.context.lastTopic && this.isFollowUpQuestion(message)) {
    return `${this.context.lastTopic}_followup`;
    }
   
    if (['hello', 'hi', 'hey', 'greetings'].includes(message)) {
    return 'greeting';
    }
   
   
    if (['bye', 'goodbye', 'farewell', 'see you'].includes(message)) {
    return 'farewell';
    }
   
    for (const [key, synonyms] of Object.entries(this.keywords)) {
    for (const synonym of synonyms) {
    const regex = new RegExp(`\\b${synonym}\\b`, 'i');
    if (regex.test(message)) {
    return key;
    }
    }
    }
   
    return 'default';
    }
   
    
   
    isFollowUpQuestion(message) {
    const followUpPatterns = [
    'how', 'what', 'can you', 'could you', 'would', 'example',
    'more', 'specific', 'tell me', 'explain'
    ];
    return followUpPatterns.some(pattern => message.includes(pattern));
    }
   
    getFollowUpResponse(topic) {
    const topicBase = topic.replace('_followup', '');
    const followUps = this.responses[topicBase]?.followUp || [];
    return followUps[Math.floor(Math.random() * followUps.length)];
    }
   
    getBotResponse(message) {
    this.context.conversationHistory.push({
    type: 'user',
    message: message,
    timestamp: new Date()
    });
   
    const intent = this.analyzeIntent(message);
    let response;
   
    if (intent === 'greeting') {
    response = this.getRandomResponse(this.responses.greetings.english);
    } else if (intent === 'farewell') {
    response = this.getRandomResponse(this.responses.farewells.english);
    } else if (intent.endsWith('_followup')) {
    response = this.getFollowUpResponse(intent);
    } else {
    response = this.responses[intent]?.main || this.responses['default'].main;
    this.context.lastTopic = intent;
    }
   
    this.context.conversationHistory.push({
    type: 'bot',
    message: response,
    timestamp: new Date()
    });
    return response;
    }
   }
   
   // Inicialización del chat
   document.addEventListener('DOMContentLoaded', function() {
    const chatButton = document.getElementById('chat-button');
    const chatWindow = document.getElementById('chat-window');
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const closeButton = document.getElementById('close-chat');
   
    // Instancia del chatbot
    const cvBot = new CVChatbot();
   
    // Mensaje inicial
    addBotMessage("👋 Hello! I am your CV assistant. I can help you with:");
    addBotMessage(`• CV/Resume tips and format\n• Cover letter advice\n• Skills optimization\n• Work experience documentation\n• Education section guidance\n• Type 'help' for all options`)
    
    // Event Listeners
    chatButton.addEventListener('click', function() {
    chatWindow.style.display = 'block';
    chatButton.style.display = 'none';
    chatInput.focus();
    });
   
    closeButton.addEventListener('click', function() {
    chatWindow.style.display = 'none';
    chatButton.style.display = 'block';
    });
   
    chatForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const message = chatInput.value.trim();
    
    if (message) {
    addUserMessage(message);
    chatInput.value = '';
   
    // Simular tiempo de respuesta
    setTimeout(() => {
    const response = cvBot.getBotResponse(message);
    addBotMessage(response);
    }, 500);
    }
    });
   
    // Funciones auxiliares
    function addUserMessage(message) {
    const div = document.createElement('div');
    div.className = 'message user-message';
    div.textContent = message;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    }
   
    function addBotMessage(message) {
    const div = document.createElement('div');
    div.className = 'message bot-message';
    // Reemplazar los saltos de línea con <br> para mantener el formato
    div.innerHTML = message.replace(/\n/g, '<br>');
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    }
   });