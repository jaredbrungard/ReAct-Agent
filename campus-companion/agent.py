from smolagents import ToolCallingAgent
import model_utils
from campus_agent.tools.web_tools import UniversitySearchTool, ScrapePageTool, EventSearchTool

def build_agent(verbose: int = 1) -> ToolCallingAgent:
    model = model_utils.google_build_reasoning_model()

    tools = [UniversitySearchTool(), ScrapePageTool(), EventSearchTool(),]

    agent = ToolCallingAgent(
        tools=tools,
        model=model,
        verbosity_level=verbose,
        stream_outputs=False,
        instructions="""You are the 'Campus Companion,' an AI agent for Utah Tech University.
Your job is to answer questions from a user.
You must use your tools to find the most current and relevant information.
- Use 'event_search' for any questions about schedules, workshops, colloquiums, or what's happening on campus.
    - IMPORTANT: When searching for a specific date, try to use the 'YYYY-MM-DD' format (e.g., "2025-10-14") or a partial match like "10-14".
- Use 'university_search' for general questions about academics, sports, departments, or other university facts.
- Use 'scrape_page' to get detailed information from a URL provided by the 'university_search' tool.
- Synthesize the information from your tools to provide a complete and helpful answer.
"""
    )
    return agent


