import streamlit as st
import base64
from groq import Groq

# API ক্লায়েন্ট সেটআপ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ইমেজ এনকোড করার ফাংশন
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# সিস্টেম প্রম্পট
system_prompt = """You are a highly intelligent and friendly AI Academic Teacher. 
Your goal is to help students learn by explaining complex topics clearly.
- If asked about your creator, simply say you are an AI assistant developed to help with education.
- Always be polite, professional, and encouraging.
- Handle both text and image queries with detailed explanations."""

# হিস্ট্রি ইনিশিয়ালাইজেশন
if "messages" not in st.session_state:
    st.session_state.messages = []

# মূল লজিক শুরু
with st.spinner("AI Teacher is thinking..."):
    try:
        # ইমেজ প্রসেসিং ও কনটেন্ট তৈরি
        if uploaded_file is not None:
            base64_image = encode_image(uploaded_file)
            user_content = [
                {"type": "text", "text": current_query if current_query else "Explain this image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        else:
            user_content = current_query if current_query else "Hello! How can I help you today?"

        # হিস্ট্রিতে যোগ করা
        st.session_state.messages.append({"role": "user", "content": user_content})

        # API কল
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
            temperature=0.3,
            max_tokens=2048
        )

        # উত্তর প্রদর্শন
        response_text = response.choices[0].message.content
        st.markdown("---")
        st.subheader("📝 AI Teacher's Response:")
        st.write(response_text)

        # হিস্ট্রিতে রাখা
        st.session_state.messages.append({"role": "assistant", "content": response_text})

    except Exception as e:
        st.error(f"Error: {e}")
