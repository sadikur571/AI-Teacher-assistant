# ১. সিস্টেম প্রম্পট (আপনার পরিচয় গোপন রেখে স্মার্ট টিচার হিসেবে সেট করা)
system_prompt = """You are a highly intelligent and friendly AI Academic Teacher. 
Your goal is to help students learn by explaining complex topics clearly.
- If asked about your creator, simply say you are an AI assistant developed to help with education.
- Always be polite, professional, and encouraging.
- Handle both text and image queries with detailed explanations."""

# ২. মূল লজিক (ইমেজ প্রসেসিং + হিস্ট্রি + এপিআই কল)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ইউজার ইনপুট ও ইমেজ প্রসেসিং
with st.spinner("AI Teacher is thinking..."):
    try:
        # ইমেজ প্রসেসিং ও ইউজার কনটেন্ট তৈরি
        if uploaded_file is not None:
            base64_image = encode_image(uploaded_file)
            user_content = [
                {"type": "text", "text": current_query if current_query else "Please explain this image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        else:
            user_content = current_query if current_query else "Hello! How can I help you with your studies?"

        # মেসেজ হিস্ট্রিতে যোগ করা
        st.session_state.messages.append({"role": "user", "content": user_content})

        # এপিআই কল
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

        # হিস্ট্রিতে অ্যাসিস্ট্যান্টের উত্তর রাখা (যাতে স্মৃতি থাকে)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

    except Exception as e:
        st.error(f"Error: {e}")
