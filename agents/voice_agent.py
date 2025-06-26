from google.adk.agents import LlmAgent
from tools.tts_tool import TTSTool
import os

tts_tool = TTSTool()

VoiceAgent = LlmAgent(
    name="voice_agent",
    model=os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
    description="Agent that converts a script to audio using TTS and returns audio path and timeline.",
    instruction="""
    You are an agent that takes a script (list of lists of strings) and uses the 'tts_tool' to generate audio and a timeline for the script. The tool returns a dictionary called tts_output having keys "audio_path" and "timestamps".
    """,
    tools=[tts_tool],
)
