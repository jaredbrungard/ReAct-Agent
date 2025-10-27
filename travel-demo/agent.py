from smolagents import ToolCallingAgent
import model_utils
from travel_agent.tools.web_tools import CityAttractionSearchTool, ScrapePageTool

def build_agent(verbose: int = 1) -> ToolCallingAgent:
    model = model_utils.google_build_reasoning_model()

    tools = [
        CityAttractionSearchTool(),
        ScrapePageTool(),
    ]

    agent = ToolCallingAgent(
        tools=tools,
        model=model,
        verbosity_level=verbose,
        stream_outputs=False,
        instructions="""You are an agent to help users plan two day excursions in a city of their choice.
        When the user gives you a city name, look up information on relevant attractions. Find information
        about those attractions. Make an itinerary with time estimates and summary of attractions.
        """
    )
    return agent


