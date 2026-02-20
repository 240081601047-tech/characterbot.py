import streamlit as st
import ollama
import time
import random
import json

# -----------------------------
# CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="FOOTBALL JARGON AI",
    layout="wide",
    page_icon="⚽"
)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("⚽ Football Jargon AI Control Panel")
    
    model = st.selectbox(
        "Select Local Model",
        ["gemma3:latest", "llama3:8b", "mixtral:8x7b"]
    )
    
    mode = st.selectbox(
        "Football Jargon Mode",
        ["Tactical", "Historical", "Analytical", "Player Stats"]
    )
    
    temperature = st.slider("Chaos Level", 0.0, 1.5, 0.4)
    typing_speed = st.slider("Typing Speed", 0.001, 0.03, 0.008)
    show_thinking = st.checkbox("Show Thinking Process", True)
    
    st.divider()
    if st.button("💾 Export Chat"):
        if "messages" in st.session_state:
            st.download_button(
                label="Download Chat",
                data=json.dumps(st.session_state.messages, indent=2),
                file_name="football_jargon_ai_chat.json"
            )
    
    if st.button("🧹 Reset Chat"):
        st.session_state.clear()
        st.rerun()

# -----------------------------
# SESSION INIT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "counter" not in st.session_state:
    st.session_state.counter = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# -----------------------------
# HEADER
# -----------------------------
st.title("⚽ FOOTBALL JARGON AI")
st.caption("Simulated Thinking • 4-Word Jargon Responses")
st.divider()

# -----------------------------
# DASHBOARD METRICS
# -----------------------------
uptime = int(time.time() - st.session_state.start_time)
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Match Focus", random.randint(10, 99))
col2.metric("📂 Total Queries", st.session_state.counter)
col3.metric("⏱ Uptime (sec)", uptime)
col4.metric("⚡ Chaos Energy", int(temperature*100))
st.divider()

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
mode_prompts = {
    "Tactical": "Respond in football tactical jargon, formations, strategies.",
    "Historical": "Respond using historical football facts and terminology.",
    "Analytical": "Respond using statistical football analytics jargon.",
    "Player Stats": "Respond using player performance and football metrics jargon."
}

SYSTEM_PROMPT = f"""
You are FOOTBALL JARGON AI.
Simulate deep football reasoning.
Reply ONLY with EXACTLY four words.
Use dense football jargon.
No explanations.
{mode_prompts[mode]}
"""

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
user_input = st.chat_input("Enter your football query...")

if user_input:
    st.session_state.counter += 1

    if not any(m["role"] == "system" for m in st.session_state.messages):
        st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # -----------------------------
    # THINKING PROCESS
    # -----------------------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        thinking_steps = [
            "Analyzing team formations...",
            "Evaluating player performance...",
            "Calculating tactical probabilities...",
            "Assessing opponent strategies..."
        ]
        if show_thinking:
            for step in thinking_steps:
                placeholder.info(step)
                time.sleep(0.6)

        # -----------------------------
        # CALL LOCAL MODEL WITH ERROR HANDLING
        # -----------------------------
        try:
            start_time = time.time()
            response = ollama.chat(
                model=model,
                messages=st.session_state.messages,
                options={"temperature": temperature}
            )
            end_time = time.time()
            raw_reply = response["message"]["content"].strip()
        except Exception as e:
            end_time = time.time()
            raw_reply = "Error contacting model."
            placeholder.error(raw_reply)
            print("Ollama error:", e)

        # -----------------------------
        # STRICT 4-WORD OUTPUT
        # -----------------------------
        words = raw_reply.split()
        if len(words) >= 4:
            final_reply = " ".join(words[:4])
        else:
            final_reply = raw_reply + " ..."

        # -----------------------------
        # TYPING ANIMATION
        # -----------------------------
        typed = ""
        for char in final_reply:
            typed += char
            placeholder.text(f"⚽ {typed}")
            time.sleep(typing_speed)

    st.session_state.messages.append({"role": "assistant", "content": final_reply})

    # -----------------------------
    # FOOTBALL STATS PANEL
    # -----------------------------
    with st.expander("📊 Football Match Stats"):
        # Simulated football stats (replace with real parsing if available)
        goals_scored = random.randint(0, 5)
        penalties = random.randint(0, 2)
        freekicks = random.randint(0, 3)
        trophies = random.randint(0, 10)
        player_ratings = round(random.uniform(5.0, 10.0), 1)

        st.write("⚽ Goals Scored:", goals_scored)
        st.write("⚖️ Penalties:", penalties)
        st.write("🟡 Free-kicks:", freekicks)
        st.write("🏆 Trophies Won:", trophies)
        st.write("⭐ Player Ratings:", player_ratings)
