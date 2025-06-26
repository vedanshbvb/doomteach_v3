from google.adk.agents import LlmAgent
from tools.fetch_analytics_tool import FetchAnalyticsTool
import os

fetch_analytics_tool = FetchAnalyticsTool()

AnalyticsAgent = LlmAgent(
    name="analytics_agent",
    model=os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
    description="Agent that fetches analytics for published videos.",
    instruction="""
    You are an agent that fetches analytics for published videos. Use the 'fetch_analytics_tool' to retrieve analytics data and return it to the user.
    """,
    tools=[fetch_analytics_tool],
)
