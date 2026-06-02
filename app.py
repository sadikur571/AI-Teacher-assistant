import streamlit as st
import base64
from groq import Groq

# API এবং ফাংশন সেটআপ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# সিস্টেম প্রম্পট (আপনার নাম এবং ভাষা নির্দেশাবলীসহ)
system_prompt = """You are a professional AI Teacher Assistant created by Sadikur Rahman. 
- If asked about your creator, mention you were created by Sadikur Rahman.
- Always answer in the language the user asks in (if asked in Chinese, reply in Chinese).
- Always be polite, professional, and encouraging.
- Help students with academic questions and explain concepts clearly."""

# হিস্ট্রি বজায় রাখার জন্য ইনিশিয়ালাইজেশন
if "messages" not in st.session_state:
    st.session_state.messages = []

# ইনপুট নেওয়ার জায়গা
uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
current_query = st.chat_input("Ask your question here:")

# মূল লজিক
if current_query:
    with st.spinner("AI Teacher is thinking..."):
        try:
            # ইমেজ প্রসেসিং
            if uploaded_file is not None:
                base64_image = encode_image(uploaded_file)
                user_content = [
                    {"type": "text", "text": current_query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            else:
                user_content = current_query
            
            # মেসেজ হিস্ট্রিতে যোগ করা
            st.session_state.messages.append({"role": "user", "content": user_content})
            
            # এপিআই কল
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                temperature=0.3,
                max_tokens=2048
            )
            
            # উত্তর প্রদর্শন ও হিস্ট্রিতে সেভ করা
            response_text = response.choices[0].message.content
            
            st.markdown("---")
            st.subheader("📝 AI Teacher's Response:")
            st.write(response_text)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.error(f"Error: {e}")

# আগের সব মেসেজ দেখানো (হিস্ট্রি দেখানোর জন্য)
for message in st.session_state.messages:
    if isinstance(message["content"], str):
        with st.chat_message(message["role"]):
            st.write(message["content"])
