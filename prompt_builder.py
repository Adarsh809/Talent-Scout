# prompt_builder.py

EXIT_KEYWORDS = ["quit", "exit", "bye", "goodbye", "stop", "end"]


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

When asking, always include the field name in CAPS in the question like:
- "What is your FULL NAME?"
- "What is your EMAIL ADDRESS?"
- "What is your PHONE NUMBER?" etc.

3. After all fields are collected, confirm them back to the candidate and then move on to
   generating 3-5 technical questions tailored to the TECH STACK.
4. Maintain conversation context, ask follow-ups if needed.
5. If input is off-topic, politely steer back.
6. If the user types quit/exit/bye/stop/end, gracefully close the conversation and describe next steps.
7. Never ask for extremely sensitive data (government IDs, passwords, etc.).

Respond conversationally and only ask for one field or one technical question at a time.
"""

def build_system_message() -> dict:
    return {"role": "system", "content": BASE_SYSTEM_PROMPT}

def build_hiring_context_message(candidate_state: dict) -> dict:
    """
    Add a hidden helper message describing what we already know
    so model can ask for missing info or move to technical questions.
    """
    summary_lines = []
    for key, val in candidate_state.items():
        if val:
            summary_lines.append(f"{key}: {val}")
    summary = "\n".join(summary_lines) if summary_lines else "No candidate info yet."

    helper = f"""
Here is the candidate information collected so far:

{summary}

If required details are missing, ask for them.
Once you know the tech stack, generate 3-5 tailored technical questions
over the course of the conversation (not all at once).
"""
    return {"role": "system", "content": helper}

def contains_exit_keyword(text: str) -> bool:
    text_lower = text.lower()
    return any(k in text_lower for k in EXIT_KEYWORDS)
