# streamlit_deep_research_ai.py
import os
import time
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import streamlit as st
from bs4 import BeautifulSoup
import requests
from serpapi import GoogleSearch
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

# ---------------------- Load Environment ----------------------
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini/gemini-2.0-flash"

# ---------------------- Google Search Tool ----------------------
def google_search(query: str, retries: int = 3, delay: float = 2.0) -> List[dict]:
    if not SERPAPI_API_KEY:
        raise RuntimeError("SERPAPI_API_KEY is not set in .env")
    for attempt in range(retries):
        try:
            search = GoogleSearch({
                "q": query,
                "location": "United States",
                "num": 5,
                "api_key": SERPAPI_API_KEY
            })
            results = search.get_dict()
            return results.get("organic_results", [])
        except Exception as ex:
            st.warning(f"[Search Error] Attempt {attempt+1}: {str(ex)}")
            time.sleep(delay)
    return []

# ---------------------- URL Scraper Tool ----------------------
@function_tool
def url_scrape(url: str) -> str:
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(["script", "style"]): tag.extract()
        text = soup.get_text(separator=' ', strip=True)
        return text[:5000]
    except Exception as e:
        return f"Failed to scrape: {str(e)}"

# ---------------------- Agent Schemas ----------------------
class QueryResponse(BaseModel):
    queries: List[str]
    thoughts: str

class FollowUpDecisionResponse(BaseModel):
    should_follow_up: bool
    reasoning: str
    queries: List[str]

class SearchResult(BaseModel):
    title: str
    url: str
    summary: str

# ---------------------- Prompts ----------------------
QUERY_AGENT_PROMPT = """You are a helpful assistant that can generate search queries for research.\nThink, explain strategy, and generate 3 diverse high-quality queries."""
FOLLOWUP_PROMPT = """You are a researcher that decides if follow-up queries are needed based on findings."""
SYNTHESIS_PROMPT = """You are a research report writer. Given a query and summaries, write a full markdown report with headings, TOC, and citations."""
SEARCH_PROMPT = """You are a summarizer. Summarize the main points of a webpage in 2-3 paragraphs, no fluff."""

# ---------------------- Agents ----------------------
query_agent = Agent("Query Agent", QUERY_AGENT_PROMPT, output_type=QueryResponse, model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY))
followup_agent = Agent("Follow-up Agent", FOLLOWUP_PROMPT, output_type=FollowUpDecisionResponse, model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY))
synthesis_agent = Agent("Synthesis Agent", SYNTHESIS_PROMPT, model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY))
search_agent = Agent("Search Agent", SEARCH_PROMPT, tools=[url_scrape], model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY))

# ---------------------- Research Coordinator ----------------------
class ResearchCoordinator:
    def __init__(self, query):
        self.query = query
        self.search_results: List[SearchResult] = []
        self.iteration = 1

    async def research(self):
        query_response = await Runner.run(query_agent, input=self.query)
        st.markdown("""<h4 style='color:#1E90FF;'>💭 <b>Query Agent Thoughts</b></h4>""", unsafe_allow_html=True)
        st.info(query_response.final_output.thoughts)

        for _ in range(3):
            await self.perform_search(query_response.final_output.queries)
            decision = await self.evaluate_followup()
            if not decision.should_follow_up:
                break
            self.iteration += 1
            query_response.final_output.queries = decision.queries

        report = await self.synthesize_report()
        return report

    async def perform_search(self, queries: List[str]):
        for query in queries:
            st.markdown(f"<h5 style='color:#FF8C00;'>🔍 Searching: {query}</h5>", unsafe_allow_html=True)
            results = google_search(query)
            for result in results:
                title = result.get("title")
                url = result.get("link")
                if not title or not url:
                    continue
                st.markdown(f"**🌐 {title}**")
                st.markdown(f"🔗 [Visit Website]({url})")
                analysis = await Runner.run(search_agent, input=f"Title: {title}\nURL: {url}")
                summary = analysis.final_output
                self.search_results.append(SearchResult(title=title, url=url, summary=summary))
                with st.expander("📝 Summary Preview"):
                    st.write(summary[:300] + ("..." if len(summary) > 300 else ""))

    async def evaluate_followup(self):
        findings = f"Query: {self.query}\n\n"
        for r in self.search_results:
            findings += f"Title: {r.title}\nURL: {r.url}\nSummary: {r.summary}\n\n"
        response = await Runner.run(followup_agent, input=findings)
        st.markdown("""📌 <span style='color:#20B2AA; font-size:18px'><b>Follow-up Evaluation</b></span>""", unsafe_allow_html=True)
        st.markdown(f"**Decision:** {'🔁 <span style=\"color:#FF8C00\"><b>Continue</b></span>' if response.final_output.should_follow_up else '✅ <span style=\"color:green\"><b>Complete</b></span>'}", unsafe_allow_html=True)
        st.markdown(f"<b>Reasoning:</b> {response.final_output.reasoning}", unsafe_allow_html=True)
        if response.final_output.should_follow_up:
            st.markdown("**Next Queries:**")
            for q in response.final_output.queries:
                st.markdown(f"- {q}")
        return response.final_output

    async def synthesize_report(self):
        st.markdown("""<h4 style='color:#800080;'>🧠 Synthesizing Final Report</h4>""", unsafe_allow_html=True)
        full_text = f"Query: {self.query}\n\n"
        for r in self.search_results:
            full_text += f"Title: {r.title}\nURL: {r.url}\nSummary: {r.summary}\n\n"
        result = await Runner.run(synthesis_agent, input=full_text)
        return result.final_output

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="🧠 Deep Research AI Tool", layout="wide")
st.markdown("""
    <h1 style='text-align: center; color: #4A90E2;'>🔍 Deep Research AI Assistant</h1>
    <h4 style='text-align: center; color: gray;'>Agentic Research Powered by Google + Gemini</h4>
    <hr style='border-top: 2px solid #bbb;'>
""", unsafe_allow_html=True)

query = st.text_input("**Enter your research topic:**", placeholder="e.g. Is fluoride good for health?")

if st.button("🚀 Start Research") and query.strip():
    with st.spinner("🤖 Thinking and gathering knowledge from the web..."):
        coordinator = ResearchCoordinator(query)
        final_report = asyncio.run(coordinator.research())
        st.success("✅ Research Complete!")
        st.markdown("""<h3 style='color:#4682B4;'>📋 Final Research Report</h3>""", unsafe_allow_html=True)
        st.markdown(final_report, unsafe_allow_html=True)
