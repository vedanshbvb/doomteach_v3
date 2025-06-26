from google.adk.agents import LlmAgent
from tools.identify_characters_tool import IdentifyCharactersTool
import os

identify_characters_tool = IdentifyCharactersTool()

IdentifyCharactersAgent = LlmAgent(
    name="identify_characters_agent",
    model=os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
    description="Agent that identifies character names from a user prompt.",
    instruction="""
    You are an agent that extracts and returns the names of iconic characters mentioned in a user prompt. Use the 'identify_characters' tool to return a comma-separated list of character names, and do not include any extra text or explanation.
    """,
    tools=[identify_characters_tool],
)
