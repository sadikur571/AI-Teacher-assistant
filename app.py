import streamlit as st
from groq import Groq
import os
import base64

# ১. পেজ কনফিগারেশন এবং স্টাইল (রয়েল ব্লু থিম)
st.set_page_config(
    page_title="AI Teacher Assistant",
    page_icon="🎓",
    layout="wide"
)
# পরিচয় সেটআপ (এআই যেন সবসময় মনে রাখে)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant created by Sadikur Rahman. Sadikur Rahman is currently studying in China. His home address is Bangladesh, Sylhet, Sunamganj. Always introduce yourself as Sadikur Rahman's AI assistant."}
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
language = st.selectbox(
    "Choose Language / ভাষা নির্বাচন করুন / 选择语言",
    ["English", "Bangla (বাংলা)", "Chinese (中文)"]
)

# সিস্টেম প্রম্পট সেট করা (যাতে এআই বুঝতে পারে সে কোন ভাষায় উত্তর দেবে)
if language == "Bangla (বাংলা)":
    system_prompt = "You are an expert AI Teacher. Always reply in clear and detailed Bangla. If user uploads an image, analyze it thoroughly and explain it in Bangla."
elif language == "Chinese (中文)":
    system_prompt = "You are an expert AI Teacher. Always reply in fluent and natural Chinese (Simplified). If user uploads an image, analyze it thoroughly and explain it in Chinese."
else:
    system_prompt = "You are an expert AI Teacher. Always reply in detailed English. If user uploads an image, analyze it thoroughly and explain it in English."

# ৪. ফাইল আপলোডার (স্ক্রিনশট বা ছবি নেওয়ার জন্য)
uploaded_file = st.file_uploader("Upload an image or screenshot (Optional) / একটি ছবি বা স্ক্রিনশট আপলোড করুন", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # স্ক্রিনে আপলোড করা ছবিটি দেখানো
    st.image(uploaded_file, caption="Uploaded Image", width=400)

# ৫. প্রশ্ন লেখার টেক্সট বক্স
user_query = st.text_area("Ask your question to AI Teacher: / আপনার প্রশ্নটি লিখুন:", height=100)

# 六. উত্তর জেনারেট করার বাটন ও লজিক
if st.button("Get AI Answer"):
    if not user_query and uploaded_file is None:
        st.warning("Please enter a question or upload an image first! / দয়া করে একটি প্রশ্ন লিখুন অথবা ছবি আপলোড করুন!")
    else:
        with st.spinner("AI Teacher is thinking..."):
            try:
                # মেসেজ লিস্ট তৈরি
                messages = [
                    {"role": "system", "content": system_prompt}
                ]
                
                # যদি ইউজার ছবি আপলোড করে থাকে
                if uploaded_file is not None:
                    base64_image = encode_image(uploaded_file)
                    
                    # প্রম্পট যদি খালি থাকে তবে ডিফল্ট প্রশ্ন দেওয়া
                    final_text_query = user_query if user_query else "Explain this image in detail based on the selected language."
                    
                    # ভিশন মডেলের জন্য মেসেজ ফরম্যাট
                    user_content = [
                        {"type": "text", "text": final_text_query},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                else:
                    # যদি শুধু টেক্সট প্রশ্ন হয়
                    user_content = user_query
                
                messages.append({"role": "user", "content": user_content})
                
                # Groq API কল করা (Llama 3.2 Vision Model)
                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=2048
                )
                
                # উত্তর স্ক্রিনে দেখানো
                st.markdown("---")
                st.subheader("📝 AI Teacher's Response:")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error generating response: {e}")
