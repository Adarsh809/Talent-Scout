# app.py
import streamlit as st

from llm_client import GroqLlamaClient
from prompt_builder import (
    build_system_message,
    build_hiring_context_message,
    contains_exit_keyword,
)
from storage import save_candidate

# -------- Streamlit page config --------
st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🧑‍💻")

st.title("🧑‍💻 TalentScout Hiring Assistant")
st.caption("LLM-powered initial screening assistant for tech candidates.")

# -------- Session state initialization --------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {
        "Full Name": None,
        "Email Address": None,
        "Phone Number": None,
        "Years of Experience": None,
        "Desired Position(s)": None,
        "Current Location": None,
        "Tech Stack": None,
    }
if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = True
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# -------- Helper to bind answers to fields --------
def update_candidate_state_from_text(user_text: str, last_assistant_text: str | None):
    """
    Map the user's reply to a specific field based on what the assistant asked last.
    Works best if your system prompt asks with phrases like:
    - "What is your FULL NAME?"
    - "What is your EMAIL ADDRESS?"
    etc.
    """
    if not last_assistant_text:
        return

    text = user_text.strip()
    c = st.session_state.candidate
    q = last_assistant_text.lower()

    if "full name" in q and not c["Full Name"]:
        c["Full Name"] = text
    elif "email address" in q and not c["Email Address"]:
        c["Email Address"] = text
    elif "phone number" in q and not c["Phone Number"]:
        c["Phone Number"] = text
    elif "years of experience" in q and not c["Years of Experience"]:
        c["Years of Experience"] = text
    elif "desired position" in q and not c["Desired Position(s)"]:
        c["Desired Position(s)"] = text
    elif "current location" in q and not c["Current Location"]:
        c["Current Location"] = text
    elif "tech stack" in q and not c["Tech Stack"]:
        c["Tech Stack"] = text

# -------- LLM client --------
try:
    llm = GroqLlamaClient()
except Exception:
    st.error(
        "LLM initialization failed. Make sure GROQ_API_KEY is set "
        "in your environment or .env file."
    )
    st.stop()

# -------- Greeting on first load --------
if not st.session_state.greeted:
    system_msg = build_system_message()
    greet_user_msg = {
        "role": "user",
        "content": "Greet the candidate and explain what you will do.",
    }
    messages = [system_msg, greet_user_msg]
    assistant_reply = llm.chat(messages)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.session_state.greeted = True

# -------- Display chat history --------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------- Chat input --------
if st.session_state.conversation_active:
    user_input = st.chat_input("Type your message here...")
else:
    user_input = None
    st.info("Conversation ended. Refresh the page to start a new session.")

if user_input:
    # Add user message to history and UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Find last assistant message to know what field was being asked
    last_assistant = None
    for msg in reversed(st.session_state.messages[:-1]):  # skip the latest user message
        if msg["role"] == "assistant":
            last_assistant = msg["content"]
            break

    # Update candidate snapshot from this answer
    update_candidate_state_from_text(user_input, last_assistant)

    # Exit keyword check
    if contains_exit_keyword(user_input):
        closing_system = {
            "role": "system",
            "content": (
                "User wants to end conversation. Thank them and describe next steps."
            ),
        }
        convo = [build_system_message(), closing_system]
        assistant_reply = llm.chat(convo, temperature=0.2)
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

        # Save candidate snapshot on exit
        save_candidate(st.session_state.candidate)
        st.session_state.conversation_active = False
        st.stop()

    # Build messages for LLM
    system_msg = build_system_message()
    context_msg = build_hiring_context_message(st.session_state.candidate)

    history_msgs = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
    messages = [system_msg, context_msg] + history_msgs

    # LLM response
    assistant_reply = llm.chat(messages, temperature=0.3)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

# -------- Sidebar: candidate info preview --------
with st.sidebar:
    st.header("Candidate Snapshot")
    for k, v in st.session_state.candidate.items():
        st.write(f"**{k}**: {v if v else 'Not provided yet'}")
    st.markdown("---")
    st.caption("Data stored locally in candidate_data.json (simulated DB).")
