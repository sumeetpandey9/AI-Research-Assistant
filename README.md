# 📚 AI Research Assistant  
🚀 **Summarization & Conversational AI for Research Papers**  

## 🌟 Overview  
AI Research Assistant is a **Streamlit-based** web application that helps researchers quickly extract **summaries, insights, and key information** from academic papers. It supports **natural language queries** using the **Gemini API**, making research faster and more efficient.  

## ✨ Features  
✔️ **PDF Upload & Processing** – Extracts **text, tables, and images** from research papers.  
✔️ **AI-Powered Summarization** – Generates structured summaries using **Gemini API**.  
✔️ **Conversational Chatbot** – Allows **natural language interaction** with research documents.  
✔️ **Reference Highlighting** – Links chatbot responses to **specific sections** in the PDF.  
✔️ **User Authentication (Planned)** – Save previous queries and uploaded documents.  

---

## 🛠️ Tech Stack  

| Category | Technologies Used |
|----------|------------------|
| **Framework** | Streamlit |
| **PDF Processing** | PyPDF2, pdfplumber, pymupdf |
| **AI & NLP** | Gemini API, transformers, torch, nltk, sentence-transformers, spacy |
| **Language & Utility** | Langchain, tqdm, requests, numpy |
| **Environment Management** | python-dotenv |

---

## 👥 Installation & Setup  

### 1️⃣ **Clone the Repository**  
```sh
git clone https://github.com/sumeetpandey9/AI-Research-Assistant
cd AI-Research-Assistant
```

### 2️⃣ **Set Up a Virtual Environment (Recommended)**  
```sh
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**  
```sh
pip install -r requirements.txt
```

### 4️⃣ **Configure API Keys**  
Create a `.env` file in the root directory and add:  
```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## ▶️ Running the Application  
```sh
streamlit run app.py
```
The application should be accessible at **`http://localhost:8501/`**.

---

## 📌 How to Use  
1️⃣ **Upload a research paper (PDF).**  
2️⃣ **Get an AI-generated summary.**  
3️⃣ **Interact with the chatbot for contextual queries.**  

---

## 🤝 Contributing  
Contributions are welcome! To contribute:  
1. **Fork** the repository.  
2. **Create a new branch** (`feature/your-feature`).  
3. **Commit changes** and push to your fork.  
4. **Submit a Pull Request.**  

---

## 🏆 Credits  
Developed by **SUMEET PANDEY**  

---

## 🐜 License  
This project is **not licensed** at the moment.


