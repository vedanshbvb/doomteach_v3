from google.adk.tools import FunctionTool
import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List

load_dotenv()

class IdentifyCharactersTool(FunctionTool):
    """
    ADK Tool for identifying character names from a user prompt using the Shapes API.
    """
    def __init__(self):
        def identify_characters(user_prompt: str) -> List[str]:
            """
            Identifies the character names in a user prompt and returns them as a comma-separated string.

            Args:
                user_prompt (str): The prompt describing the script to generate.

            Returns:
                List[str]: List of comma-separated characters names.
            """
            shapes_client = OpenAI(
                api_key=os.environ.get("SHAPES_API_KEY"),
                base_url="https://api.shapes.inc/v1/",
            )
            model = "shapesinc/reelscripter"
            response = shapes_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Identify the characters in the following command and return their names. You should only return the names of the characters in a comma separated format. Do not return any other text or explanation.\nFor eg: 'Write a script for Obama and Trump where they discuss about Kubernetes' should return 'Barack Obama, Donald Trump'\n\nCommand: {user_prompt}\n                        """
                    }
                ]
            )
            content = response.choices[0].message.content
            if content is not None:
                return [name.strip() for name in content.strip().split(",") if name.strip()] 
            return []
        super().__init__(func=identify_characters)
