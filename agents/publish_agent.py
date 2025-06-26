from google.adk.agents import LlmAgent
from tools.publish_video_tool import PublishVideoTool
import os

publish_video_tool = PublishVideoTool()

PublishAgent = LlmAgent(
    name="publish_agent",
    model=os.environ.get("AGENT_MODEL", "gemini-2.0-flash"),
    description="Agent that publishes the final video to a social media platform.",
    instruction="""
    You are an agent that publishes a completed video to a social media platform. Use the 'publish_video_tool' to perform the upload and return the result.
    """,
    tools=[publish_video_tool],
)
