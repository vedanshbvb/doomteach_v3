from google.adk.agents import LlmAgent
from tools.get_stickers_tool import GetStickersTool
from tools.video_editing_tool import VideoEditingTool
from tools.add_subtitles_tool import AddSubtitlesTool
import os

get_stickers_tool = GetStickersTool()
video_editing_tool = VideoEditingTool()
add_subtitles_tool = AddSubtitlesTool()

VideoAgent = LlmAgent(
    name="video_agent",
    model=os.environ.get("AGENT_MODEL", "gemini-2.5-flash"),
    description="Agent that creates a video with stickers and subtitles using the provided tools.",
    instruction="""
    You are an agent that creates a video for a social media reel. 
    The video will be composed of character stickers, audio generated from a script, and subtitles.
    The paths of the audio file must be : media/generated/audio/final_audio.mp3 and the background video must be media/bg_videos/vid1.mp4.
    


    STRICTLY use the tools in the following order:

    1. Use the 'get_stickers_tool' to fetch character stickers. You will receive a list of character names. Pass that list to this tool. This tool returns a dictionary mapping character names to their sticker image paths.       

    2. Use the 'video_editing_tool' to compose the video with stickers and audio. It requires the following parameters:
        - tts_output: The TTS output with timestamps.
        - character_img_paths: The dictionary mapping character names to their sticker image paths.
        - characters: The list of character names.
        - bg_video_path: The path to the background video (default is "media/bg_videos/vid1.mp4").
        - audio_path: The path to the audio file final_audio.mp3 
        
        This tool will create a video with the stickers overlay based on the TTS output and character images. It returns the path to the generated video file which will be media/generated/video/doom_video.mp4.
        


    3. Use the 'add_subtitles_tool' to overlay subtitles on the video. 
    It requires the following parameters:
        - video_path: The path to the video file created in the previous step. 
        This will be the output of the video_editing_tool and must be media/generated/video/doom_video.mp4.

        - output_path: The path where the subtitled video will be saved. The video should be saved to media/generated/video/doom_video_with_subs.mp4.
        
        This tool generates subtitles and overlays them on the given video, returning the final video path.                                               

    
    Accept all required parameters and return the final video path.
    """,
    tools=[get_stickers_tool, video_editing_tool, add_subtitles_tool],
)
