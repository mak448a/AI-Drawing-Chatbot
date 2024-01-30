from dotenv import load_dotenv
from .replit_detector import is_replit
import json
import logging
import os

# If you're looking for logging config here, go to replit_detector.py!!!


if is_replit:
    bot_token: str = os.environ["BOT_TOKEN"]
    api_key: str = os.environ["API_KEY"]
    prodia_key: str = os.environ["PRODIA_KEY"]
else:
    # Load .env file
    load_dotenv(".env")
    bot_token: str = os.getenv("BOT_TOKEN")
    api_key: str = os.getenv("API_KEY")
    prodia_key: str = os.getenv("PRODIA_KEY")

if api_key == "0000000000":
    logging.warning("Default API key selected. Generating images will be slower. "
                    "Generated images will be sent to LAION to improve Stable Diffusion.")

# Load config
with open("config.json") as f:
    config = json.load(f)

# Line junk is some stuff that makes Discord hide links.
# See https://www.youtube.com/watch?v=9OgpQHSP5qE (by Ntts)

line_junk = """||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _"""


class FakeCtx:
    def __init__(self, message):
        self.author = message.author
        self.message = message

    async def send(self, content, file=None):
        return await self.message.channel.send(content, file=file)


# Import functions for use in other files
if config["chatbot"]:
    # Figure out which model the user specified
    if config["model"] == "GPT4All":
        # GPT4All
        from gpt_utils.gpt4all import generate_message, clear_context  # NOQA
    elif config["model"] == "gpt4free":
        # GPT4All
        from gpt_utils.gpt4free import generate_message, clear_context  # NOQA
    else:
        # Fallback
        logging.warning("Configured model improperly! Check config.json!")
        from gpt_utils.gpt4free import generate_message, clear_context  # NOQA
else:
    # Create a dummy function so that we don't error out when importing them
    def fake_function():
        pass

    generate_message, clear_context = fake_function, fake_function
