import asyncio
import os


# Load api key
try:
    with open("api_key.txt") as f:
        api_key = f.read()
except FileNotFoundError:
    api_key = "0000000000"
    print("[WARNING] No API key selected. Generating images will be slower. Using anonymous account.")

# Check if anything_diffusion_enable.txt exists
if os.path.exists("anything_diffusion_enable.txt"):
    use_anything_diffusion = True
    print("Using Anything Diffusion")
else:
    print("Using Stable Diffusion")
    use_anything_diffusion = False


async def check_generated_images(gen_time: float):
    while True:
        if os.path.exists(f"0_{gen_time}.png"):
            return
        else:
            await asyncio.sleep(0.8)
            continue

try:
    with open("bot_token.txt") as f:
        bot_token = f.read()
except FileNotFoundError:
    print("BOT TOKEN NOT FOUND! PLACE YOUR BOT TOKEN IN `bot_token.txt`.")
