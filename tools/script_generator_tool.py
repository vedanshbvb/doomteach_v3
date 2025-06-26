from google.adk.tools import FunctionTool
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

def log_line(line):
    log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "run_pipeline.log")
    with open(log_file, "a") as f:
        f.write(line + "\n")

class ScriptGeneratorTool(FunctionTool):
    """
    ADK Tool for generating a script for a social media reel using the Shapes API.
    """
    def __init__(self):
        def generate_script(user_prompt: str) -> list[list[str]]:   
            """
            Generates a JSON-formatted script for a social media reel based on a user prompt.

            Args:
                user_prompt (str): The prompt describing the script to generate.

            Returns:
                script (list[list[str]]): List of (speaker, line) lists.
            """
            log_line("STATUS: Starting script generation...")
            
            shapes_client = OpenAI(
                api_key=os.environ.get("SHAPES_API_KEY"),
                base_url="https://api.shapes.inc/v1/",
            )
            log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "generator", "script_generator.log")
            
            with open(log_file, "a") as f:
                f.write(f"User prompt: {user_prompt}\n")
            
            response = shapes_client.chat.completions.create(
                model="shapesinc/jsonbot",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        You are a script writer for a social media reel and you possess great knowledge of popular culture and iconic characters and also are a very skilled tech enthusiast.
                        User will give you a command for writing a short, engaging script for a reel featuring two iconic characters which will be given to you in the command. The theme of the reel is a discussion about some topic which will be given to you in the command. The script should be full of knowledge about the topic and be suitable for a quick, entertaining video format, around 1 to 2 minutes. There should not be more than 20 dialogues in any condition. The script should be a short one meant for instagram reels. One of the characters should be asking questions and the other should be answering them. 
                        The speaker of the dialogue should be in double quotes and the dialogue should come after a colon. The dialogue should also be in double quotess. The output should be a json object. Make sure the script starts with curly brackets and also ends with curly brackets. For example :

                    
                        {{
                        "Stewie": "How are you?",
                        "Peter": "I am fine, thank you!",
                        "Stewie": "Awesome!"
                        }}


                        Command: {user_prompt}
                        Output a json object starting and ending with curly brackets.
                        """
                    }

                ],
            temperature=0.7,
            max_tokens=1000
            )
            
            # Check for None response
            script_content = None
            try:
                script_content = response.choices[0].message.content if response and response.choices and response.choices[0].message and response.choices[0].message.content else None
            except Exception as e:
                log_line(f"ERROR: Failed to get script content from response: {e}")
                script_content = None

            if script_content is None:
                log_line("ERROR: Script content is None. Returning empty script.")
                return []

            script = script_content.strip()
            
            # Fix: If script does not end with '}', add it
            if not script.endswith("}"):
                script += "}"
            if not script.startswith("{"):
                script = "{" + script
            if script.startswith("{") and script.endswith("}"):
                pass
                
            log_line(f"Generated script: {script}")
            log_line("\n\n\nscript done")

            parsed_script = []
            try:
                if isinstance(script, str):
                    # Use object_pairs_hook to preserve order in dict
                    script_pairs = json.loads(script, object_pairs_hook=list)
                    if isinstance(script_pairs, list):
                        parsed_script = [[k, v.strip().rstrip(":")] for k, v in script_pairs if isinstance(k, str) and isinstance(v, str)]
                elif isinstance(script, dict):
                    parsed_script = [[k, v.strip().rstrip(":")] for k, v in script.items()]
                elif isinstance(script, list) and all(isinstance(item, (list, tuple)) and len(item) == 2 for item in script):
                    parsed_script = [[item[0], item[1].strip().rstrip(":")] for item in script]
            except Exception as e:
                log_line(f"ERROR: Failed to parse script JSON: {e}")
                parsed_script = []

            log_line(f"Parsed script: {parsed_script}")

            return parsed_script

        super().__init__(func=generate_script)
