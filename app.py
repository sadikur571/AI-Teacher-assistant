import streamlit as st
from groq import Groq

# ১. ওয়েবসাইটের পেইজ সেটআপ (টাইটেল এবং আইকন)
st.set_page_config(page_title="AI Teacher Assistant", page_icon="🎓", layout="centered")
# --- কাস্টম সিএসএস (UI/UX ডিজাইন আপডেট) ---
st.markdown("""
    <style>
    /* ১. পুরো অ্যাপের ব্যাকগ্রাউন্ড হালকা উন্নত করা */
    [data-testid="stAppViewContainer"] {
        background-color: #fdfdfd;
    }
    
    /* ২. "Get AI Answer" বাটনের চেহারা সুন্দর করা */
    .stButton>button {
        background-color: #1E88E5 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 28px !important;
        box-shadow: 0px 4px 10px rgba(30, 136, 229, 0.2) !important;
        transition: all 0.3s ease;
    }
    
    /* ৩. বাটনের ওপর মাউস নিলে সুন্দর ইংরেজি ও অ্যানিমেশন */
    .stButton>button:hover {
        background-color: #1565C0 !important;
        box-shadow: 0px 6px 15px rgba(21, 101, 192, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* ৪. টেক্সট ইনপুট বক্সটি সুন্দর করা */
    .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #E0E0E0 !important;
        font-size: 15px !important;
    }
    
    /* ৫. এআই রেসপন্স সেকশনের টাইটেল সুন্দর করা */
    h2, h3 {
        color: #0D47A1 !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)
# ২. Groq ক্লায়েন্ট সেটআপ
# ⚠️ মনে করে নিচে আপনার Groq-এর আসল API Key (gsk_...) বসিয়ে দিন
try:
    client = Groq(api_key="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")
except Exception as e:
    st.error(f"Initialization Error: {e}")

# ৩. ইন্টারফেসের ভাষা অনুযায়ী টেক্সট ডাটা
content = {
    "English": {
        "title": "🎓 AI Teacher Assistant",
        "subtitle": "Your personal AI tutor for coding, language, and doubts!",
        "label": "Ask your question to AI Teacher:",
        "btn": "Get AI Answer",
        "loading": "Thinking...",
        "out": "📝 AI Teacher's Response:"
    },
    "Bangla": {
        "title": "🎓 এআই শিক্ষক সহকারী",
        "subtitle": "কোডিং, ভাষা শিক্ষা বা যেকোনো পড়াশোনার জন্য আপনার ব্যক্তিগত টিউটর!",
        "label": "এআই শিক্ষককে আপনার প্রশ্নটি জিজ্ঞেস করুন:",
        "btn": "উত্তর জানুন",
        "loading": "ভাবছি...",
        "out": "📝 এআই শিক্ষকের উত্তর:"
    },
    "French": {
        "title": "🎓 Assistant Enseignant IA",
        "subtitle": "Votre tuteur IA personnel pour le codage, les langues et les doutes!",
        "label": "Posez votre question à l'enseignant IA:",
        "btn": "Obtenir la réponse",
        "loading": "En réflexion...",
        "out": "📝 Réponse de l'enseignant IA:"
    }
}

# ⁴. সাইডবারে ভাষা সিলেক্ট করার ড্রপডাউন
selected_lang = st.sidebar.selectbox("🌐 Choose Language / ভাষা নির্বাচন করুন", list(content.keys()))
lang_data = content[selected_lang]

# ⁵. ওয়েবসাইটের মূল অংশ ডিজাইন
st.title(lang_data["title"])
st.write(lang_data["subtitle"])
st.markdown("---")

# ইনপুট বক্স
user_query = st.text_area(lang_data["label"], value="What is Artificial Intelligence?", height=100)

# অ্যাকশন বাটন
if st.button(lang_data["btn"]):
    if not user_query.strip():
        st.warning("Please enter a question! / দয়া করে একটি প্রশ্ন লিখুন!")
    else:
        with st.spinner(lang_data["loading"]):
            try:
                # প্রম্পট তৈরি করা
                full_prompt = f"Respond in {selected_lang} language. Question: {user_query}"
                
                # Groq Llama 3.3 মডেল কল করা
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": full_prompt}],
                    temperature=0.7,
                    max_tokens=2048
                )
                
                # উত্তর স্ক্রিনে দেখানো
                result = completion.choices[0].message.content
                st.markdown("---")
                st.subheader(lang_data["out"])
                st.write(result)
                
            except Exception as e:
                st.error(f"Error: {str(e)}\n\nPlease check your VPN connection! (চায়না থেকে ব্যবহারের জন্য ভিপিএন অন রাখুন)")
