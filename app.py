import streamlit as st
from groq import Groq
import os
import base64
def get_system_prompt(subject, language):
    identity = "You are an AI assistant created solely by Sadikur Rahman. Do not mention Meta or other companies. He is currently studying in China, and his home address is Bangladesh, Sylhet, Sunamganj."
    
    # বিষয়ভিত্তিক লজিক
    if subject == "General":
        sub_instruction = "You are a versatile academic tutor capable of explaining any subject, from Mathematics and Science to History and Literature. Provide comprehensive, accurate, and easy-to-understand explanations for any academic question."
    elif subject == "Mathematics":
        sub_instruction = "Focus on step-by-step logical solutions and formulas."
    elif subject == "Science":
        sub_instruction = "Provide clear, scientific explanations with examples."
    else:
        sub_instruction = "Provide helpful and detailed explanations."
        
    # ভাষা লজিক
    if language == "Bangla (বাংলা)":
        lang_instruction = "Always respond in clear and detailed Bangla."
    else:
        lang_instruction = "Always respond in the requested language."
        
    return f"{identity} You are acting as a {subject} tutor. {sub_instruction} {lang_instruction}"
# ১. পেজ কনফিগারেশন এবং স্টাইল (রয়েল ব্লু থিম)
st.set_page_config(
    page_title="AI Teacher Assistant",
    page_icon="🎓",
    layout="wide"
)
# পরিচয় সেটআপ (এআই যেন সবসময় মনে রাখে)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant created by Sadikur Rahman. Do not mention Meta or any other company. Always introduce yourself as Sadikur Rahman's AI assistant. He is currently studying in China, and his home address is Bangladesh, Sylhet, Sunamganj. Never say you were created by Meta."}
    ]
# কাস্টম সিএসএস স্টাইল (এখানে ভুলটি ফিক্স করা হয়েছে)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #fdfdfd;
    }
    .stButton>button {
        background-color: #1E88E5 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 28px !important;
        box-shadow: 0px 4px 10px rgba(30, 136, 229, 0.2) !important;
    }
    .stButton>button:hover {
        background-color: #1565C0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ২. Groq API ক্লায়েন্ট তৈরি করা (Streamlit Secrets থেকে সুরক্ষিতভাবে চাবি নেওয়া)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Initialization Error: {e}")

# ইমেজকে base64 ফরম্যাটে রূপান্তর করার ফাংশন
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# ৩. ইন্টারফেস তৈরি
st.title("🎓 AI Teacher Assistant (Vision Edition)")
st.write("Your personal AI tutor for text, images, and multilingual doubts!")

# ভাষা নির্বাচন করার ড্রপডাউন (চাইনিজ ভাষা যুক্ত করা হয়েছে)
# ভাষা নির্বাচন করার ড্রপডাউন
language = st.selectbox(
    "Choose Language / ভাষা নির্বাচন করুন / 选择语言",
    ["English", "Bangla (বাংলা)", "Chinese (中文)"]
)
# সিস্টেম প্রম্পট সেট করা (যাতে এআই বুঝতে পারে সে কোন ভাষায় উত্তর দেবে)
# সিস্টেম প্রম্পট সেট করার জন্য আপনার বানানো ফাংশনটি ব্যবহার করুন
# বিষয় হিসেবে "General" সেট করা হয়েছে যাতে যেকোনো বিষয়ে সাহায্য করতে পারে
system_prompt = get_system_prompt("General", language)
# ৪. ফাইল আপলোডার (স্ক্রিনশট বা ছবি নেওয়ার জন্য)
uploaded_file = st.file_uploader("Upload an image or screenshot (Optional) / একটি ছবি বা স্ক্রিনশট আপলোড করুন", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # স্ক্রিনে আপলোড করা ছবিটি দেখানো
    st.image(uploaded_file, caption="Uploaded Image", width=400)

# ৫. প্রশ্ন লেখার টেক্সট বক্স
# হিস্ট্রি সেভ করার জন্য লজিক
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# চ্যাট ইনপুট বক্স
if prompt := st.chat_input("Ask your question to AI Teacher:"):
    st.session_state.chat_history.append(prompt)

# 六. উত্তর জেনারেট করার বাটন ও লজিক
if st.button("Get AI Answer"):
    # ১০০ নম্বর লাইন থেকে শুরু হবে:
    if len(st.session_state.chat_history) == 0 and uploaded_file is None:
        st.warning("Please enter a question or upload an image first!")
    else:
        # হিস্ট্রি থেকে শেষ প্রশ্নটি নেওয়া
        current_query = st.session_state.chat_history[-1] if len(st.session_state.chat_history) > 0 else "Explain this"
        
        with st.spinner("AI Teacher is thinking..."):
        try:
            # ১. ইমেজ বা টেক্সট প্রসেসিং
            if uploaded_file is not None:
                base64_image = encode_image(uploaded_file)
                final_text_query = current_query if current_query else "Explain this image in detail based on the selected language."
                user_content = [
                    {"type": "text", "text": final_text_query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            else:
                user_content = current_query
            
            # ২. মেসেজ হিস্ট্রিতে যোগ করা
            st.session_state.messages.append({"role": "user", "content": user_content})
            
            # ৩. Groq API কল করা
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                temperature=0.3,
                max_tokens=2048
            )
            
            # ৪. উত্তর স্ক্রিনে দেখানো
            response_text = response.choices[0].message.content
            st.markdown("---")
            st.subheader("📝 AI Teacher's Response:")
            st.write(response_text)
            
            # ৫. অ্যাসিস্ট্যান্টের উত্তর হিস্ট্রিতে যোগ করা
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            # কোনো ভুল হলে এখানে ধরা পড়বে
            st.error(f"Error: {e}")
                
           
