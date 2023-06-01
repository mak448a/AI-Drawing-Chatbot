from dotenv import load_dotenv
import asyncio
import os

# Load .env file
load_dotenv(".env")
bot_token: str = os.getenv("BOT_TOKEN")
api_key: str = os.getenv("API_KEY")
use_anything_diffusion: bool = bool(os.getenv("ANYTHING_DIFFUSION"))

if api_key == "0000000000":
    print("[WARNING] Default API key selected. Generating images will be slower. "
          "Generated images will be sent to LAION to improve Stable Diffusion.")


async def check_generated_images(gen_time: float):
    while True:
        if os.path.exists(f"0_{gen_time}.png"):
            return
        else:
            await asyncio.sleep(0.8)
            continue
