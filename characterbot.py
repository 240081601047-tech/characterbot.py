import streamlit as st
import ollama
import time
import random
import json
from datetime import datetime

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="BATMAN AI",
    layout="wide",
    page_icon="🦇"
)

# ---------------------------------
# SIDEBAR CONTROL CENTER
# ---------------------------------
with st.sidebar:
    st.title("🦇 BATCAVE CONTROL")

    model = st.selectbox("AI Engine", ["gemma3:latest"])

    ai_mode = st.selectbox(
        "AI Mode",
        ["Strategic", "Detective", "Tactical"]
    )

    temperature = st.slider("Chaos Level", 0.0, 1.5, 0.4, 0.1)
    typing_speed = st.slider("Typing Speed", 0.001, 0.03, 0.008)

    st.divider()

    if st.button("💾 Export Chat"):
        if "messages" in st.session_state:
            st.download_button(
                label="Download Conversation",
                data=json.dumps(st.session_state.messages, indent=2),
                file_name="batman_ai_chat.json"
            )

    if st.button("🧹 Reset System"):
        st.session_state.clear()
        st.rerun()

# ---------------------------------
# SYSTEM INITIALIZATION
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ---------------------------------
# HEADER
# ---------------------------------
st.title("🦇 BATMAN AI")
st.caption("Advanced Strategic Intelligence System")

st.divider()

# ---------------------------------
# LIVE SYSTEM ANALYTICS
# ---------------------------------
uptime = int(time.time() - st.session_state.start_time)

col1, col2, col3, col4 = st.columns(4)

col1.metric("🛡 Threat Index", random.randint(10, 99))
col2.metric("📂 Conversations", st.session_state.chat_count)
col3.metric("⏱ Uptime (sec)", uptime)
col4.metric("⚡ Chaos %", int(temperature * 100))

st.divider()

# ---------------------------------
# SYSTEM PROMPTS BY MODE
# ---------------------------------
if ai_mode == "Strategic":
    mode_prompt = "Respond strategically. Focus on long-term vision and calculated decisions."
elif ai_mode == "Detective":
    mode_prompt = "Respond analytically. Break problems into logical investigative steps."
else:
    mode_prompt = "Respond tactically. Provide actionable, step-by-step solutions."

SYSTEM_PROMPT = f"""
You are BATMAN AI.
Speak in a dark, intelligent, concise tone.
Never say you are an AI.
{mode_prompt}
Occasionally reference Gotham, justice, or strategy.
"""

# ---------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="🦇"):
            st.write(msg["content"])

# ---------------------------------
# CHAT INPUT
# ---------------------------------
user_input = st.chat_input("Speak to BATMAN AI...")

if user_input:

    if not any(m["role"] == "system" for m in st.session_state.messages):
        st.session_state.messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    st.session_state.chat_count += 1

    with st.chat_message("user", avatar="🧑"):
        st.write(user_input)

    with st.chat_message("assistant", avatar="🦇"):
        placeholder = st.empty()
        placeholder.info("🔎 Processing tactical intelligence...")
        time.sleep(1)

        start_response = time.time()

        response = ollama.chat(
            model=model,
            messages=st.session_state.messages,
            options={"temperature": temperature}
        )

        end_response = time.time()
        response_time = round(end_response - start_response, 2)

        reply = response["message"]["content"]

        typed = ""
        for char in reply:
            typed += char
            placeholder.markdown("🦇 **" + typed + "**")
            time.sleep(typing_speed)

    st.session_state.messages.append({
        "role": "assistant",
        "content": "🦇 " + reply
    })

    # ---------------------------------
    # RESPONSE ANALYTICS PANEL
    # ---------------------------------
    with st.expander("📊 Response Analytics"):
        st.write("Response Time:", response_time, "seconds")
        st.write("Mode:", ai_mode)
        st.write("Chaos Level:", temperature)
        st.write("Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        st.write("Total Messages:", len(st.session_state.messages))
 