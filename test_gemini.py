
from src.tools.tools import web_search,scrape_webpage

# output=web_search("Latest news on AI research")
# result = scrape_webpage.invoke({"url":" https://ai.google/research"})
# print(output)

# print(result)

from src.pipeline.pipeline import run_research_pipeline
topic="The impact of AI on the job market in 2026"
run_research_pipeline(topic)

