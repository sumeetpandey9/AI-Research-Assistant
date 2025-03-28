import os
import nltk
import streamlit as st
from numpy.f2py.crackfortran import quiet
from transformers import pipeline
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import PyPDF2
import ssl
import warnings
from streamlit_chat import message
from dotenv import load_dotenv
import google.generativeai as genai
from login import auth
from login import auth, save_chat_history, load_chat_history


# Suppress FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# Check if SSL certificate can be verified
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


# Download NLTK data
def download_nltk_data():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("NLTK data downloaded successfully.")
    except Exception as e:
        print(f"An error occurred while downloading NLTK data: {e}")

nltk.data.path.append(os.path.join(os.path.expanduser("~"), "nltk_data"))

# Load environment variables from .env file
load_dotenv()

# Get the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("⚠️ **Error:** GEMINI_API_KEY is missing. Please set it in a .env file.")
    st.stop()

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

def get_response(user_query, context):
    """Fetch AI-generated response using Gemini API."""
    prompt = f"""
    You are an AI research assistant. Answer based on the given research paper.
    Document Context: {context}
    User Query: {user_query}
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text if response else "⚠️ No response generated."
    except Exception as e:
        return f"⚠️ API Error: {e}"

# PDF Processing Functions
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text
    return text if text else "⚠️ No extractable text found in the PDF."

def preprocess_text(text):
    return ' '.join(text.split())

def summarize_text(text, max_length=150, min_length=50):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    max_chunk_length = 1024
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = [summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return ' '.join(summaries)

def extract_key_takeaways(text, num_takeaways=5):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(words)
    sentence_scores = {sentence: sum(word_freq.get(word, 0) for word in word_tokenize(sentence.lower())) for sentence in sentences}
    return sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_takeaways]

# Footer Function
def add_footer():
    st.markdown(
        """
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #0E1117;
                color: white;
                text-align: center;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
        </style>
        <div class="footer">
            Created by <b>SUMEET PANDEY</b> with ❤️
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    download_nltk_data()
    if not auth():
        return  
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
        
    if "username" not in st.session_state:
        st.error("❌ User not authenticated!")
        return

    username = st.session_state.username  # Get logged-in username

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_chat_history(username)  # Load chat history

    # Chat Interface
    st.subheader("💬 AI Chat Assistant")
    '''Chat history of the user is saved here'''
    
    # Display chat history
    for chat in st.session_state.chat_history:
        message(chat["content"], is_user=chat["role"] == "user")

   
    
        if user_input.strip():
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get AI response
            response = get_response(user_input, "Summarized research paper content")
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Save chat history
            save_chat_history(username, st.session_state.chat_history)

            # Rerun UI to display updated chat
            st.rerun()
    
    if st.session_state.page == "welcome":
        st.title("Welcome to AI Research Assistant 🧠")
        st.write("""
            AI Research Assistant is your go-to tool for summarizing academic papers and extracting key insights with ease.
            
            ### 🚀 Features:
            - 📄 **Upload PDFs** and get instant summaries
            - 🔍 **Extract key takeaways** from research papers
            - 💬 **Interactive chat** for querying document content
            - 🎯 **Simplified research workflow** to save your time
            
            **Created by SUMEET PANDEY with ❤️**
        """)
        
        st.markdown(
    """
    <style>
    .highlight-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #FF4B4B !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        transition: 0.3s ease-in-out !important;
        border: none !important;
        cursor: pointer !important;
    }
    .stButton>button:hover {
        background-color: #FF1F1F !important;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

        if st.button("Get Started"):
            st.session_state.page = "main"
            st.rerun()
    
    elif st.session_state.page == "main":
        st.title("AI Research Assistant 🧠")

        tab1, tab2 = st.tabs(["📄 PDF Extraction Tool", "💬 AI Chat"])

        with tab1:
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

            if uploaded_file is not None:
                with st.spinner("Processing the PDF..."):
                    raw_text = extract_text_from_pdf(uploaded_file)
                    
                    if "⚠️" in raw_text:
                        st.error(raw_text)
                        return
                    
                    processed_text = preprocess_text(raw_text)
                    summary = summarize_text(processed_text)
                    key_takeaways = extract_key_takeaways(processed_text)

                st.subheader("Summary")
                st.write(summary)

                st.subheader("Key Takeaways")
                for i, takeaway in enumerate(key_takeaways, 1):
                    st.write(f"{i}. {takeaway}")

                if st.checkbox("Show full text"):
                    st.subheader("Full Text")
                    st.text_area("", processed_text, height=300)

                st.session_state["paper_text"] = processed_text

        with tab2:
            st.subheader("Chat with AI Research Assistant")
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for i, msg in enumerate(st.session_state.messages):
                message(msg["content"], is_user=msg["is_user"], key=str(i))

            user_input = st.text_input("Ask something about the paper:")

            if user_input:
                context = st.session_state.get("paper_text", "")
                bot_response = get_response(user_input, context)

                st.session_state.messages.append({"content": user_input, "is_user": True})
                st.session_state.messages.append({"content": bot_response, "is_user": False})

                message(user_input, is_user=True)
                message(bot_response, is_user=False)
    
    add_footer()

if __name__ == "__main__":
    main()
