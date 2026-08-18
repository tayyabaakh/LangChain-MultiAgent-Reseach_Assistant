from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search,scrape_webpage
from dotenv import load_dotenv
import os
load_dotenv()

# Model Initialization
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


response = llm.invoke("Hello!")
print(response.content)

# Agent 1 : Search Agent
def build_search_agent():
    return create_agent(

        model=llm,
        tools=[web_search]
    )
# Agent 2 : Reader Agent
def build_reader_agent():
    return create_agent( 
        model=llm,
        tools=[scrape_webpage],
         system_prompt="""
You are a research reader agent.

Your job is to read search results and extract deeper information from
the most relevant webpage.

Follow these steps:

1. Examine the search results.
2. Identify ONE relevant URL.
3. Call the scrape_webpage tool using the complete URL.
4. Analyze the scraped content.
5. Return the important factual information you found.

Do not perform web searches.
Do not invent URLs.
Always use scrape_webpage when a valid URL is available.
"""
    )

#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()

