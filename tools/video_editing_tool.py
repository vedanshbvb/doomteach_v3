from google.adk.tools import FunctionTool
import os
from generator.video_editing import create_video_with_stickers
from typing import List, Optional

def log_line(line):
    log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "run_pipeline.log")
    with open(log_file, "a") as f:
        f.write(line + "\n")

class VideoEditingTool(FunctionTool):
    """
    ADK Tool for creating a video with stickers overlay.
    """
    def __init__(self):
        def video_editing_tool(tts_output: dict, character_img_paths: dict, characters: List[str], bg_video_path: str = "media/bg_videos/vid1.mp4", audio_path: Optional[str] = None, output_dir: str = "media/generated/video") -> str:
            """
            Creates a video with stickers overlay using the given parameters.

            Args:
                tts_output (dict): TTS output with timestamps.

                tts_output looks like this:
                {
                    "audio_path": "path/to/final_audio.mp3",
                    "timestamps": [
                        {"speaker": "Donald Trump", "start": 0, "duration": 10, "filename": "donald_trump_1.mp3"},
                        {"speaker": "Elon Musk", "start": 10, "duration": 10, "filename": "elon_musk_2.mp3"}
                    ]
                }    


                character_img_paths (dict): Mapping of character names to image paths.
                characters (List[str]): List of character names.
                bg_video_path (str): Path to background video (default: media/bg_videos/vid1.mp4).
                audio_path (Optional[str]): Path to audio file.
                output_dir (str): Output directory for the video.

            Returns:
                str: Path to the generated video file.
            """
            log_line(f"Editing video with parameters: {tts_output}, {character_img_paths}, {characters}, {bg_video_path}, {audio_path}, {output_dir}")

            # Ensure we use the correct default background video path
            if not bg_video_path or bg_video_path == "media/background/pixel_city.mp4":
                bg_video_path = "media/bg_videos/vid1.mp4"

            log_line(f"tts_output in FILE video_editing_tool.py: {tts_output}")
            
            return create_video_with_stickers(tts_output, character_img_paths, characters, bg_video_path, audio_path, output_dir)
        super().__init__(func=video_editing_tool)
