# 🔬 Deep Research AI Assistant  
### 🚀 Built by UV – Ubaid’s Vision | Agentic AI x Google x Gemini

> **An intelligent web research agent that thinks, searches, scrapes, summarizes, and writes complete reports — just like a human researcher, but faster and smarter.**

---

## 🧠 What Is This Project?

**Deep Research AI** is a cutting-edge multi-agent AI app that transforms **any topic** into a professional research report by:

✅ Understanding the user's research goal  
✅ Generating smart search queries using **Google Search (SerpAPI)**  
✅ Scraping trusted web sources like Wikipedia, Healthline, etc.  
✅ Summarizing key findings in plain language using **Gemini Pro via LiteLLM**  
✅ Deciding whether more research is needed (follow-up logic)  
✅ Finally, writing a full **markdown-formatted research report** with **TOC, sections, citations**, and references

📌 Everything happens **automatically** inside a beautiful **Streamlit GUI**.

---

## 🎯 Use Cases

- ✅ Students making reports or presentations
- ✅ Teachers researching class topics
- ✅ Bloggers, writers, and researchers
- ✅ Anyone curious about any topic (from AI to health to history)
- ✅ Even software engineers exploring technical research

---

## 🔥 Key Features (Everything This Project Does)

| 💡 Feature                        | ✅ What It Does                                                                 |
|----------------------------------|---------------------------------------------------------------------------------|
| Agentic AI Research              | Coordinates multiple agents like Query Generator, Summarizer, Writer            |
| 🔍 Google-Powered Search         | Uses **SerpAPI** to fetch the most relevant results from Google                 |
| 🌐 URL Scraper                   | Extracts and cleans up real-time web content with **BeautifulSoup**            |
| 🧼 Summarizer Agent              | Uses **Gemini Pro** to understand and explain complex web pages                |
| 📌 Follow-up Decision Agent      | Decides intelligently if more queries or sources are needed                     |
| 📝 Final Report Generator        | Auto-writes a beautiful report with structure, markdown, and references        |
| 🎨 Clean and Colorful Streamlit UI | Stylish frontend for easy interaction and presentation                        |
| 💯 Works in Low RAM              | Efficiently runs even on laptops with 2–4 GB RAM                               |

---

## 🖥️ Demo Screenshot

![screenshot](assets/screenshot.png)

---

## 🧪 How It Works (Workflow)


**Example:**  
User: *Tell me about "Is fluoride good for health?"*  
AI:  
✅ Breaks it into 3 queries  
✅ Scrapes 5 top-ranked pages  
✅ Summarizes everything  
✅ Decides: Follow-up needed?  
✅ Builds a final report in 60 seconds!

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/deep-research-ai.git
cd deep-research-ai
python -m venv .venv
source .venv/bin/activate     # macOS/Linux  
.venv\Scripts\activate        # Windows
SERPAPI_API_KEY=your_serpapi_key
GEMINI_API_KEY=your_gemini_key
