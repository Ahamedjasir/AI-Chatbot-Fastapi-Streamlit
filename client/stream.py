import streamlit as st
import requests
import os

# ---------------- CONFIG ----------------
BACKEND_URL = os.getenv("BACKEND_URL", "https://aichatbot-backend-production-5ad8.up.railway.app/")

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("AI Assistant")

# ---------------- SESSION ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- MODE ----------------
mode = st.selectbox(
    "Choose a function",
    ["Chat with AI", "Image Generation"],
    index=0
)

# ---------------- SHOW HISTORY ----------------
if mode == "Chat with AI":
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input(
    "Type your message..." if mode == "Chat with AI" else "Describe the image..."
)

# ---------------- HANDLE ----------------
if user_input:

    if mode == "Chat with AI":

        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        try:
            res = requests.post(
                f"{BACKEND_URL}/chat",
                json={"message": user_input},
                timeout=60
            )

            if res.status_code == 200:
                ai_reply = res.json().get("response", "")
            else:
                ai_reply = "Server error."

        except Exception as e:
            ai_reply = f"Connection failed: {e}"

        st.session_state.chat_history.append(
            {"role": "assistant", "content": ai_reply}
        )

        st.rerun()

    # ============ IMAGE ============
    else:
        try:
            res = requests.post(
                f"{BACKEND_URL}/image",
                json={"prompt": user_input},
                timeout=120
            )

            if res.status_code == 200:
                st.image(res.content, caption=user_input)

                st.download_button(
                    "⬇ Download Image",
                    data=res.content,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            else:
                st.error("Image generation failed.")

        except Exception as e:
            st.error(f"Connection failed: {e}")

# ---------------- RESET ----------------
if st.button("Reset Session"):
    st.session_state.chat_history = []
    st.rerun()
