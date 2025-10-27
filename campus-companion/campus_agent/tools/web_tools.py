from smolagents import Tool, DuckDuckGoSearchTool
from bs4 import BeautifulSoup
import requests
import csv
import os


# Add this class to campus-companion/campus_agent/tools/web_tools.py
class EventSearchTool(Tool):
    name = "event_search"
    description = "Searches the Utah Tech University events.csv file for upcoming events. Use this for any questions about campus events, workshops, or schedules."
    inputs = {
        "query": {"type": "string", "description": "The search query to filter events (e.g., 'colloquium', 'athletics', 'workshop')."},
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        # Build the path to events.csv, which is one level up from the 'campus-companion' dir
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.csv_path = os.path.join(base_dir, 'events.csv')
        self.events = []
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.events.append(row)
        except Exception as e:
            self.events = [{"error": f"Failed to load events.csv: {e}"}]

    def forward(self, query: str) -> str:
        if "error" in self.events[0]:
            return str(self.events[0]["error"])

        query = query.lower()
        results = []
        for event in self.events:
            # Check if the query is in the title, description, or category
            if (query in event.get('title', '').lower() or
                query in event.get('description', '').lower() or
                query in event.get('category', '').lower()):
                results.append(event)

        if not results:
            return "No events found matching that query."

        # Format the results as a string
        return "\n".join([f"Event: {r.get('title')}, Date: {r.get('date')}, Time: {r.get('start_time')}, Location: {r.get('location')}, Description: {r.get('description')}" for r in results])

class UniversitySearchTool(Tool):
    name = "university_search"
    description = "Searches the web for information about Utah Tech University. Use this for questions about courses, sports, departments, or general university facts."
    inputs = {
        "query": {"type": "string", "description": "The specific question to search for (e.g., 'biology courses', 'football team schedule')."},
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self._ddgs = DuckDuckGoSearchTool()

    def forward(self, query: str) -> str:
        # Force the query to be about Utah Tech
        forced_query = f"Utah Tech University {query}"
        return self._ddgs(forced_query)

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

