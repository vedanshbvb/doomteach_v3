from google.adk.tools import FunctionTool
import os
from generator.add_subtitles import generate_subtitles, overlay_subtitles_on_video
from moviepy.editor import VideoFileClip

class AddSubtitlesTool(FunctionTool):
    """
    ADK Tool for generating subtitles and overlaying them on a video.
    """
    def __init__(self):
        def add_subtitles_tool(video_path: str, output_path: str) -> str:
            """
            Generates subtitles and overlays them on the given video.

            Args:
                video_path (str): Path to the video file.
                output_path (str): Path to save the subtitled video.
            Returns:
                str: Path to the final video with subtitles.
            """
            subtitle_chunks = generate_subtitles()
            video_clip = VideoFileClip(video_path)
            final_video_path = overlay_subtitles_on_video(video_clip, subtitle_chunks, output_path)
            return final_video_path
        super().__init__(func=add_subtitles_tool)
