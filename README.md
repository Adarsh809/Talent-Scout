# 🧑‍💻 TalentScout Hiring Assistant

An intelligent AI-powered chatbot designed to streamline the initial screening process for technology recruitment. Built using Streamlit and powered by Groq's LLaMA 3.3 70B model, this assistant conducts conversational interviews to gather candidate information and assess technical proficiency.

---

## Project Overview

TalentScout is a conversational hiring assistant chatbot that:

- **Greets candidates** and explains the screening process
- **Collects essential information** systematically (name, contact, experience, location, tech stack)
- **Generates tailored technical questions** based on the candidate's declared tech stack
- **Maintains conversation context** for natural, flowing interactions
- **Handles edge cases** with fallback mechanisms and exit keywords
- **Stores candidate data** securely in a simulated database (JSON file)

The chatbot uses advanced prompt engineering techniques to ensure coherent, context-aware conversations that feel natural while maintaining the structure needed for effective candidate screening.

---

## Key Capabilities

### Information Gathering
The assistant systematically collects seven essential fields:
1. Full Name
2. Email Address
3. Phone Number
4. Years of Experience
5. Desired Position(s)
6. Current Location
7. Tech Stack (languages, frameworks, databases, tools)

### Technical Assessment
- Dynamically generates 3-5 technical questions tailored to each candidate's tech stack
- Questions adapt based on experience level and declared technologies
- Maintains conversational flow while assessing proficiency

### Conversation Management
- Context-aware responses that reference previous answers
- Graceful handling of off-topic inputs
- Exit keyword detection (quit, exit, bye, goodbye, stop, end)
- Smooth conversation closure with next steps explanation

---

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com/))

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd talentscout-hiring-assistant
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

The required packages are:
- `streamlit` - Web UI framework
- `groq` - LLM API client
- `python-dotenv` - Environment variable management

### Step 4: Configure API Key
Create a `.env` file in the project root directory:
```bash
# .env
GROQ_API_KEY=your_groq_api_key_here
```

**Security Note:** Never commit your `.env` file to version control. Add it to `.gitignore`.

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will open automatically in your default browser at `http://localhost:8501`.

---

## Usage Guide

### Starting a Session
1. Launch the application using `streamlit run app.py`
2. The chatbot greets you and explains its purpose
3. Begin responding to the assistant's questions

### Conversation Flow
1. **Initial Greeting**: The assistant welcomes you and outlines the process
2. **Information Collection**: Answer questions one at a time as prompted
3. **Tech Stack Declaration**: Specify your programming languages, frameworks, and tools
4. **Technical Questions**: Receive and answer 3-5 tailored technical questions
5. **Conclusion**: Type any exit keyword to end the conversation gracefully

### Exit Keywords
Type any of these keywords to end the conversation:
- `quit`
- `exit`
- `bye`
- `goodbye`
- `stop`
- `end`

### Sidebar Features
The sidebar displays a real-time snapshot of collected candidate information:
- Shows all seven required fields
- Updates automatically as information is gathered
- Indicates which fields are still pending

### Example Interaction
```
Assistant: Hello! I'm TalentScout, your AI hiring assistant. I'll be collecting 
some basic information and asking technical questions based on your tech stack. 
Let's begin! What is your FULL NAME?

User: John Doe
```

## Technical Details

### Libraries & Frameworks

**Core Dependencies:**
- **Streamlit (latest)**: Frontend web framework for rapid UI development
  - Provides chat interface, session state management, and sidebar components
  - Handles real-time UI updates and user interactions
  
- **Groq (latest)**: High-performance LLM API client
  - Ultra-fast inference speeds (up to 500 tokens/second)
  - Provides access to LLaMA 3.3 70B model
  - Enterprise-grade reliability and scalability

- **python-dotenv (latest)**: Environment variable management
  - Securely loads API keys from .env file
  - Prevents accidental exposure of credentials

### Model Details

**LLaMA 3.3 70B Versatile** (via Groq)
- **Parameters**: 70 billion
- **Context Window**: 128K tokens
- **Strengths**: 
  - Excellent instruction following
  - Strong reasoning capabilities
  - Conversational coherence
  - Low latency responses via Groq infrastructure
- **Temperature Settings**:
  - Greeting: 0.2 (more focused and consistent)
  - Conversation: 0.3 (balanced creativity and coherence)
  - Closing: 0.2 (professional and consistent sign-off)

### Data Flow

1. **User Input** → Streamlit chat interface
2. **State Management** → Session state tracks conversation and candidate data
3. **Context Building** → System prompts + conversation history
4. **LLM Processing** → Groq API generates contextual responses
5. **State Update** → Candidate snapshot updated based on response
6. **UI Rendering** → Response displayed in chat + sidebar updated
7. **Data Persistence** → On conversation end, data saved to JSON

### Key Design Decisions

**1. Modular Architecture**
- Separating concerns (UI, LLM client, prompts, storage) makes the codebase maintainable and testable
- Each module has a single, well-defined responsibility

**2. Groq for LLM Inference**
- Chosen for exceptional speed (critical for real-time chat UX)
- Cost-effective compared to OpenAI GPT-4
- LLaMA 3.3 70B provides excellent quality-to-cost ratio

**3. Session State for Context**
- Streamlit's session state provides reliable state management across reruns
- Enables seamless multi-turn conversations
- Tracks both conversation history and candidate data snapshot

**4. JSON File Storage**
- Simple, file-based "database" suitable for prototype/assignment
- Easy to inspect and debug
- Timestamped records for audit trail
- Production version would use proper database (PostgreSQL, MongoDB)

**5. Explicit Field Labeling in Prompts**
- System prompt instructs model to use CAPS for field names (e.g., "What is your FULL NAME?")
- Enables simple regex-based field detection in `update_candidate_state_from_text()`
- Trade-off: simplicity vs. more sophisticated NLP-based extraction

---

## Prompt Design

### System Prompt Strategy

The system prompt (in `prompt_builder.py`) serves as the foundation for all assistant behavior:

```python
BASE_SYSTEM_PROMPT = """
You are TalentScout, an AI hiring assistant chatbot for a tech recruitment agency.

Your goals:
1. Greet the candidate and explain you will collect basic details and ask tech questions.
2. Ask for these fields ONE BY ONE in this exact order, clearly labeling them:
   (a) Full Name
   (b) Email Address
   (c) Phone Number
   (d) Years of Experience
   (e) Desired Position(s)
   (f) Current Location
   (g) Tech Stack (languages, frameworks, databases, tools)
...
"""
```

### Prompt Engineering Techniques

**1. Role Definition**
- Clearly defines the assistant as "TalentScout" with specific purpose
- Sets professional tone and establishes expectations

**2. Structured Task Breakdown**
- Numbered goals provide clear hierarchy
- Sub-steps (a, b, c...) ensure systematic information gathering

**3. Explicit Field Labeling**
- Instructs model to include field names in CAPS
- Example: "What is your FULL NAME?"
- Enables downstream parsing and state management

**4. Sequential Processing**
- "ONE BY ONE" instruction prevents information overload
- Maintains natural conversation flow
- Allows for clarifications and follow-ups

**5. Context Injection**
- Dynamic context message shows what's been collected:
```python
def build_hiring_context_message(candidate_state: dict):
    """Add helper message describing collected info"""
    summary = "\n".join(f"{key}: {val}" for key, val in candidate_state.items() if val)
    helper = f"Here is the candidate information collected so far:\n{summary}\n..."
    return {"role": "system", "content": helper}
```
- Prevents redundant questions
- Guides model to ask for missing info or proceed to technical questions

**6. Behavioral Guardrails**
- "If input is off-topic, politely steer back"
- "Never ask for extremely sensitive data"
- Ensures focused, professional conversations

**7. Exit Handling**
- Explicit instructions for graceful conversation closure
- Detection of keywords: quit, exit, bye, goodbye, stop, end

### Technical Question Generation

Once tech stack is known, the system prompt instructs:
```
"Once you know the tech stack, generate 3-5 tailored technical questions
over the course of the conversation (not all at once)."
```

**Adaptive Questioning:**
- Questions tailored to specific technologies mentioned
- Example: Python + Django → questions about decorators, ORM, middleware
- Example: React + TypeScript → questions about hooks, type inference, state management

**Progressive Difficulty:**
- Model naturally varies difficulty based on years of experience
- Junior candidates get foundational questions
- Senior candidates get architecture and design questions

---


## Challenges & Solutions

### Challenge 1: Context Management Across Turns

**Problem**: Streamlit reruns the entire script on each interaction, making stateful conversation difficult.

**Solution**: 
- Leveraged Streamlit's `st.session_state` to persist:
  - Conversation history (`messages`)
  - Candidate data snapshot (`candidate`)
  - Conversation status (`conversation_active`, `greeted`)
- Each message exchanged is appended to session state
- Full conversation history sent to LLM on each turn for context

### Challenge 2: Mapping User Responses to Specific Fields

**Problem**: Open-ended conversation makes it hard to know which field a user's response corresponds to.

**Solution**:
- System prompt instructs model to use explicit field labels (CAPS)
- `update_candidate_state_from_text()` function checks last assistant message for field keywords
- Simple pattern matching: if "full name" in question → store answer in "Full Name" field
- Trade-off accepted: works reliably for structured flow, may need NLP for more complex scenarios

### Challenge 3: Preventing Redundant Questions

**Problem**: Without proper context, LLM might re-ask already-answered questions.

**Solution**:
- Implemented `build_hiring_context_message()` that injects current candidate state into system context
- Before each LLM call, model sees summary of collected information
- Model intelligently skips already-filled fields and proceeds to next missing field

### Challenge 4: Graceful Exit Handling

**Problem**: Users expect to end conversation naturally, but need confirmation and data saving.

**Solution**:
- Implemented keyword detection (`contains_exit_keyword()`)
- When exit keyword detected:
  1. Send special system message to LLM for closing remarks
  2. Save candidate data to JSON
  3. Set `conversation_active = False`
  4. Display closure message and disable chat input
- User can refresh to start new session

### Challenge 5: Technical Question Quality

**Problem**: Generic technical questions aren't useful for assessment.

**Solution**:
- System prompt emphasizes: "generate 3-5 tailored technical questions based on the TECH STACK"
- Model naturally leverages its training on technical content
- Questions adapt to:
  - Specific technologies mentioned
  - Experience level (inferred from years of experience)
- Questions distributed across conversation (not all at once)

### Challenge 6: API Key Security

**Problem**: API keys shouldn't be hardcoded or committed to version control.

**Solution**:
- Used `python-dotenv` for environment variable management
- `.env` file stores `GROQ_API_KEY`
- `.gitignore` prevents `.env` from being committed
- `llm_client.py` reads key from environment with fallback error handling

### Challenge 7: UI/UX for Real-Time Updates

**Problem**: Users need to see what information has been collected.

**Solution**:
- Implemented sidebar display showing candidate snapshot
- Updates automatically after each interaction
- Shows "Not provided yet" for missing fields
- Provides transparency and reduces user confusion

---

## Data Privacy & Compliance

### Data Handling Practices

1. **Local Storage**: All candidate data stored locally in `candidate_data.json`
2. **No Cloud Database**: Avoids third-party data storage concerns
3. **Simulated Environment**: Uses anonymized/test data for development
4. **Timestamp Tracking**: Each record includes UTC timestamp for audit trail

### GDPR Considerations

- **Data Minimization**: Only collects necessary fields for hiring assessment
- **Purpose Limitation**: Data used solely for recruitment screening
- **Transparency**: Candidate informed of data collection purpose
- **No Sensitive Data**: Deliberately avoids SSN, government IDs, passwords, etc.

### Production Recommendations

For production deployment, implement:
- Encrypted database storage (e.g., PostgreSQL with encryption at rest)
- HTTPS for all communications
- User consent mechanisms
- Data retention policies
- Right to deletion (GDPR Article 17)
- Access controls and authentication
- Audit logging

---

## Future Enhancements

### Planned Features
- [ ] **Multi-language Support**: Internationalization for global recruitment
- [ ] **Sentiment Analysis**: Detect candidate engagement and emotions
- [ ] **Resume Upload & Parsing**: Extract information from PDF/DOCX resumes
- [ ] **Video Interview Integration**: Connect with platforms like Zoom/Teams
- [ ] **Advanced Analytics**: Dashboard for recruiter insights
- [ ] **Email Notifications**: Automated follow-ups and scheduling
- [ ] **Database Migration**: Move from JSON to PostgreSQL/MongoDB
- [ ] **Authentication**: Recruiter login system
- [ ] **A/B Testing**: Different prompt strategies for optimization

### Technical Improvements
- [ ] **Caching**: Redis for conversation state (multi-user scalability)
- [ ] **Async Processing**: Non-blocking LLM calls
- [ ] **Error Recovery**: Retry logic for API failures
- [ ] **Monitoring**: Logging and observability (e.g., Datadog, Sentry)
- [ ] **Unit Tests**: Comprehensive test coverage
- [ ] **CI/CD Pipeline**: Automated testing and deployment

---

**Built with ❤️ using Streamlit, Groq, and LLaMA 3.3 70B**
