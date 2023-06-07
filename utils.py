from dotenv import load_dotenv
import json
import os

# Load .env file
load_dotenv(".env")
bot_token: str = os.getenv("BOT_TOKEN")
api_key: str = os.getenv("API_KEY")

if api_key == "0000000000":
    print("[WARNING] Default API key selected. Generating images will be slower. "
          "Generated images will be sent to LAION to improve Stable Diffusion.")

# Load config
with open("config.json") as f:
    config = json.load(f)
