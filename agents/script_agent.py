from google.adk.agents import LlmAgent
from tools.script_generator_tool import ScriptGeneratorTool

script_generator_tool = ScriptGeneratorTool()

ScriptAgent = LlmAgent(
    name="script_agent",
    model="gemini-2.0-flash",  # You may want to make this configurable
    description="Agent that generates a JSON-formatted script for a social media reel based on a user prompt.",
    instruction="""
    You are a script-writing agent for social media reels. When given a user prompt, use the 'generate_script' tool to create a short, engaging script featuring two iconic characters. The script should be suitable for a 1-2 minute Instagram reel, with no more than 20 dialogues. One character should ask questions, the other should answer. Return the script as list[list[str]] i.e. a list of [speaker, line] lists.
    """,
    tools=[script_generator_tool],
)
