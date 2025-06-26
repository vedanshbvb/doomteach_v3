from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
import os

from agents.script_agent import ScriptAgent
from agents.identify_characters_agent import IdentifyCharactersAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from agents.publish_agent import PublishAgent
from agents.analytics_agent import AnalyticsAgent

RootAgent = LlmAgent(
    name="root_agent",
    model=os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
    description="Coordinator agent that orchestrates the full video generation and publishing pipeline.",
    instruction="""
    You are the coordinator agent for a multi-step video generation pipeline. For each user prompt, you must do the following steps STRICTLY in the order given below:


    1. STRICTLY Use the ScriptAgent to generate a script. This agent will take the user prompt and generate a script for a social media reel. The script should be concise and suitable for a short video format. The output will be a script (list[list[str]]): List of (speaker, line) lists.

    2. STRICTLY Use the IdentifyCharactersAgent to extract character names. Ths will take the user prompt and return a comma-separated list of character names. This is essential for the next steps. 

    Once above steps are complete, then you MUST go to VoiceAgent and VideoAgent in the order:

    3. STRICTLY Use the VoiceAgent to generate audio and timeline from the script and characters. THis takes the script and returns tts_output, a dictionary with keys "audio_path" and "timestamps".

    For example, if the script is:
    [["Donald Trump", "line1"], ["Elon Musk", "line2"]]

    then tts_output will be:
    {
        "audio_path": "path/to/final_audio.mp3",
        "timestamps": [
            {"speaker": "Donald Trump", "start": 0, "duration": 10, "filename": "donald_trump_1.mp3"},
            {"speaker": "Elon Musk", "start": 10, "duration": 10, "filename": "elon_musk_2.mp3"}
        ]
    }    
    


    4. STRICTLY Use the VideoAgent to fetch stickers, compose the video, and add subtitles. This agent will take the tts_output, character names, and background video path (default is "media/bg_videos/vid1.mp4") to create a video with stickers overlay based on the TTS output and character images. 
    The VideoAgent will also add subtitles to the video using the audio timestamps from tts_output and return the final video path which will be media/generated/video/doom_video_with_subs.mp4.






    5. Optionally use the PublishAgent to publish the video.
    6. Optionally use the AnalyticsAgent to fetch analytics for published videos.
    Always reason about which agent/tool to call next, and pass outputs as needed. Return the final video path or analytics as appropriate.
    """,
    tools=[
        AgentTool(agent=ScriptAgent),
        AgentTool(agent=IdentifyCharactersAgent),
        AgentTool(agent=VoiceAgent),
        AgentTool(agent=VideoAgent),
        AgentTool(agent=PublishAgent),
        AgentTool(agent=AnalyticsAgent),
    ],
)
