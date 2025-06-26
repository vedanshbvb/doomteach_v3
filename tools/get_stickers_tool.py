from google.adk.tools import FunctionTool
import os
from generator.get_stickers import download_character_stickers
from typing import List

class GetStickersTool(FunctionTool):
    """
    ADK Tool for downloading character stickers given a list of character names.
    """
    def __init__(self):
        def get_stickers(characters: List[str]) -> dict:
            """
            Downloads stickers for the given characters and returns a dict of character->image path.

            Args:
                characters (List[str]): List of character names. Each character name must be a string. So characters is a list of strings.
            Returns:
                dict: Mapping of character name to image path (or None if not found).
            """
            return download_character_stickers(characters)
        
        super().__init__(func=get_stickers)



if __name__ == "__main__":
    # Example test input
    characters = ["Elon Musk", "Donald Trump"]
    
    # Instantiate and run the tool directly
    tool = GetStickersTool()
    result = tool.func(characters)  # .func gives you access to the actual wrapped function
    print(result)
