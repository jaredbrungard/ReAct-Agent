from smolagents import Tool, DuckDuckGoSearchTool
from bs4 import BeautifulSoup
import requests

class CityAttractionSearchTool(Tool):
    name = "city_attraction_search"
    description = "Given the name of a city, this tool will return top attractions in that location."
    inputs = {
        "city": {"type": "string", "description": "The city to search in."},
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self._ddgs = DuckDuckGoSearchTool()

    def forward(self, city: str) -> str:
        query = f"top cultural attractions in {city}?"
        return self._ddgs(query)

class ScrapePageTool(Tool):
    name = "scrape_page"
    description = "Fetch a web page and return a cleaned text summary (title + first ~500 characters)."
    inputs = {"url": {"type":"string","description":"HTTP/HTTPS URL to fetch"}}
    output_type = "string"

    def forward(self, url: str) -> str:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            return f"Request failed: {e}"
        soup = BeautifulSoup(resp.text, "html.parser")
        title = (soup.title.string.strip() if soup.title and soup.title.string else url)
        # crude extract of visible text
        for tag in soup(["script","style","noscript"]):
            tag.decompose()
        text = " ".join(t.get_text(" ", strip=True) for t in soup.find_all(["p","li","h1","h2","h3"]))
        text = " ".join(text.split())
        snippet = text[:500] + ("…" if len(text) > 500 else "")
        return f"{title}\n{snippet}"

