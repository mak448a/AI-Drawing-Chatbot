from dotenv import load_dotenv
from .replit_detector import is_replit
import json
import logging
import os

# If you're looking for logging config here, go to replit_detector.py!!!


if is_replit:
    bot_token: str = os.environ["BOT_TOKEN"]
    api_key: str = os.environ["API_KEY"]
    poe_key: str = os.environ["POE_TOKEN"]
else:
    # Load .env file
    load_dotenv(".env")
    bot_token: str = os.getenv("BOT_TOKEN")
    api_key: str = os.getenv("API_KEY")
    poe_key: str = os.getenv("POE_TOKEN")

if api_key == "0000000000":
    logging.warning("Default API key selected. Generating images will be slower. "
                    "Generated images will be sent to LAION to improve Stable Diffusion.")

# Load config
with open("config.json") as f:
    config = json.load(f)

# Line junk is some stuff that makes Discord hide links.
# See https://www.youtube.com/watch?v=9OgpQHSP5qE (by Ntts)

def line_junk():
    bars = '|' * 990
    underscores = ' _' * 6
    return bars + underscores

line_junk = line_junk()


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
    elif config["model"] == "gpt-3.5-turbo":
        from gpt_utils.vercel import generate_message, clear_context  # NOQA
    else:
        # Fallback on gpt-3.5-turbo
        logging.warning("Configured model improperly! Check config.json!")
        from gpt_utils.vercel import generate_message, clear_context  # NOQA
