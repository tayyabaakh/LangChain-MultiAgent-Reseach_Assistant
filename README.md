🔬 # LangChain Multi-Agent Research Assistant

An AI-powered Multi-Agent Research Assistant built with LangChain, Streamlit, Tavily, and web-scraping tools.

The system divides the research workflow into specialized agents. Instead of asking a single LLM to perform the entire task, each agent focuses on a specific responsibility:

## Search → Read → Write → Critic

This project is designed to demonstrate an agentic AI architecture where multiple specialized components collaborate to produce a more structured research report.


## 📥 Report Download

Allows the generated research report to be downloaded as a Markdown file.

## 🏗️ Architecture

<img width="1067" height="393" alt="image" src="https://github.com/user-attachments/assets/740222b5-747f-4c2d-bf41-30f6213f26ef" />


## 🧠 How It Works

### 1. Search Agent

The user provides a research topic.

For example:

Latest advancements in Agentic AI

The Search Agent receives the topic and searches for recent and reliable information.

The search results are passed to the next stage.

### 2. Reader Agent

The Reader Agent receives the search results and determines which resource is most useful.

It then uses the project's web-scraping functionality to extract deeper content from the selected webpage.

Search Results
      ↓
Relevant URL
      ↓
Web Scraper
      ↓
Detailed Content

This gives the Writer more context than the search snippets alone.

### 3. Writer

The Writer receives both:

SEARCH RESULTS
+
DETAILED SCRAPED CONTENT

These are combined into a research context and passed to the writer chain.

research_combined = (
    f"SEARCH RESULTS:\n{search_results}\n\n"
    f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
)

report = writer_chain.invoke({
    "topic": topic,
    "research": research_combined
})

The result is the generated research report.

### 4. Critic

The Critic receives the generated report and evaluates it.

The feedback can be used to identify weaknesses, missing information, or areas that could be improved.

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| Python | Core programming language |
| LangChain | Agent and LLM orchestration |
| LangGraph / LangChain Agents | Agentic workflow components |
| Groq / LLM Provider | Language model inference |
| Tavily | Web search |
| Requests | HTTP requests |
| BeautifulSoup | HTML parsing |
| Readability | Extracting readable webpage content |
| Trafilatura | Web content extraction |
| python-dotenv | Environment variable management |
| Streamlit | Web interface |

▶️ Running the Application

Start the Streamlit application:

streamlit run app.py

Then open:

http://localhost:8501

🖥️ Using the Application

Open the Streamlit application.

Enter a research topic.

Click Start Research.

The Search Agent finds relevant sources.

The Reader Agent selects and scrapes a useful source.

The Writer generates the research report.

The Critic reviews the generated report.

Review the results using the different tabs.

Download the final report as Markdown.


## 👩‍💻 Author

Tayyaba Akhter
