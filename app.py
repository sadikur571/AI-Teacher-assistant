import streamlit as st
import base64
from groq import Groq

# পৃষ্ঠার টাইপ ও লেআউট সেটআপ
st.set_page_config(page_title="AI Academic Teacher Assistant", page_icon="🤖", layout="centered")

# API ক্লায়েন্ট সেটআপ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# সিস্টেম প্রম্পট (আপনার নাম এবং ভাষা নির্দেশাবলীসহ)
system_prompt = """You are a professional AI Teacher Assistant created by Sadikur Rahman. 
- If asked about your creator, always mention you were created by Sadikur Rahman.
- Always answer in the language the user asks in (if asked in Chinese, reply in Chinese).
- Always be polite, professional, and encouraging.
- Help students with academic questions and explain concepts clearly."""

# সাইডবারে সেটিংস ও হিস্ট্রি পরিষ্কার করার বাটন
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.info("Developed by Sadikur Rahman for Academic Support.")

# হিস্ট্রি বজায় রাখার জন্য ইনিশিয়ালাইজেশন
if "messages" not in st.session_state:
    st.session_state.messages = []

# শিরোনাম
st.title("🎓 AI Academic Teacher Assistant")
st.write("Ask questions via text, voice, or upload an image for explanation!")

# ইনপুট অপশনসমূহ: ছবি, ভয়েস এবং টেক্সট
uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

# ভয়েস ইনপুট নেওয়ার জন্য নতুন ফিচার (Streamlit Audio Input)
audio_file = st.audio_input("🎤 Or record your voice query:")

# সাধারণ লেখার চ্যাট ইনপুট
current_query = st.chat_input("Ask your question here...")

# কোন ইনপুটটি ব্যবহার করা হয়েছে তা নির্ধারণ করা
final_query = None

if current_query:
    final_query = current_query
elif audio_file is not None:
    with st.spinner("Transcribing your voice..."):
        try:
            # ভয়েস অডিও ফাইলটিকে Groq Whisper মডেল দিয়ে টেক্সটে রূপান্তর করা
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=("audio.wav", audio_file.read()),
                prompt="Translate or transcribe the audio accurately."
            )
            final_query = transcription.text
            st.info(f"🗣️ You said: {final_query}")
        except Exception as e:
            st.error(f"Voice Transcription Error: {e}")

# মূল লজিক (যখন কোনো টেক্সট বা ভয়েস পাওয়া যাবে)
if final_query:
    with st.spinner("AI Teacher is thinking..."):
        try:
            # ইমেজ প্রসেসিং
            if uploaded_file is not None:
                base64_image = encode_image(uploaded_file)
                user_content = [
                    {"type": "text", "text": final_query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            else:
                user_content = final_query
            
            # মেসেজ হিস্ট্রিতে যোগ করা
            st.session_state.messages.append({"role": "user", "content": user_content})
            
            # এপিআই কল (স্টেবল মডেল ব্যবহার করা হয়েছে যাতে এরর না আসে)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                temperature=0.3,
                max_tokens=2048
            )
            
            # উত্তর সংগ্রহ
            response_text = response.choices[0].message.content
            
            # হিস্ট্রিতে সহকারী উত্তর যোগ করা
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.error(f"Error: {e}")

# চ্যাট হিস্ট্রি সুন্দরভাবে স্ক্রিনে দেখানোর লজিক
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    with st.chat_message(role):
        if isinstance(content, str):
            st.write(content)
        elif isinstance(content, list):
            for item in content:
                if item["type"] == "text":
                    st.write(item["text"])
                elif item["type"] == "image_url":
                    st.image(item["image_url"]["url"], caption="Uploaded Image", width=300)l"], caption="Uploaded Image", width=300)t"])
