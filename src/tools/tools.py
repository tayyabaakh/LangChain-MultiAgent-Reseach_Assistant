from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()
tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Tool 1
@tool
def web_search(query:str)->str:
    """Search the web for recent and reliable information on a topic.

    Args:
        query (str): The search query or topic to retrieve information for.

    Returns:
        str: A formatted string containing the titles, URLs, and summaries 
             or content of the top search results.
    """
    results=tavily.search(query=query,max_results=5)
    # print(results)
    out=[]
    for r in results['results']:
        out.append(
            f"Title {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    return "\n----\n".join(out)     

# Tool 2
@tool
def scrape_webpage(url: str) -> str:
    """Scrape and extract the main readable content from a webpage.Uses multiple extraction strategires for better reliabilty

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        str: Cleaned text content extracted from the webpage.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
                "Accept-Language":"en-US,en;=0.9",
                "Referer":"https://www.google.com/"
            
        }

        # Fetch webpage
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        # Make sure we received HTML
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return f"Unable to scrape {url}: URL does not contain HTML."

        html = response.text

        # --------------------------------------------------
        # Method 1: Trafilatura - preferred extraction method
        # --------------------------------------------------
        text = trafilatura.extract(
            html,
            include_links=False,
            include_images=False,
            include_tables=True,
            favor_precision=True
        )

        # --------------------------------------------------
        # Method 2: Readability fallback
        # --------------------------------------------------
        if not text:
            doc = Document(html)
            cleaned_html = doc.summary()

            soup = BeautifulSoup(cleaned_html, "html.parser")

            # Remove unwanted elements
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            text = soup.get_text(separator="\n")

        # --------------------------------------------------
        # Method 3: BeautifulSoup fallback
        # --------------------------------------------------
        if not text:
            soup = BeautifulSoup(html, "html.parser")

            for tag in soup([
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
                "aside",
                "form"
            ]):
                tag.decompose()

            text = soup.get_text(separator="\n")

        # --------------------------------------------------
        # Clean extracted text
        # --------------------------------------------------

        # Remove excessive whitespace
        text = re.sub(r"[ \t]+", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        # Remove leading/trailing whitespace
        text = text.strip()

        # Limit extremely large pages
        max_chars = 15000

        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n[Content truncated...]"

        if not text:
            return f"No readable content could be extracted from {url}"

        return f"Source: {url}\n\n{text}"

    except requests.exceptions.Timeout:
        return f"Scraping failed: request timed out for {url}"

    except requests.exceptions.HTTPError as e:
        return f"Scraping failed: HTTP error for {url} - {e}"

    except requests.exceptions.RequestException as e:
        return f"Scraping failed: network error for {url} - {e}"

    except Exception as e:
        return f"Scraping failed for {url}: {str(e)}"

    