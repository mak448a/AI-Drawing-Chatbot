import discord
from discord import app_commands
from discord.ext import commands
import platform
import os
import time
import aiohttp

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# Load api key
try:
    with open("api_key.txt") as f:
        api_key = f.read()
except FileNotFoundError:
    api_key = "0000000000"
    print("No api key selected. Using anonymous account!")

async def download_image(image_url, save_as):
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
    with open(save_as, "wb") as f:
        f.write(response.content)

@bot.event
async def on_ready():
    print("Ready")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
    
@bot.tree.command(name="imagine")
@app_commands.describe(prompt="Write an amazing prompt for Stable Diffusion to generate")
async def imagine(interaction: discord.Interaction, prompt: str):
    sanitized = ""
    forbidden = ['"', "'", "`", "\\", "$"]

    for char in prompt:
        if char in forbidden:
            continue
        else:
            sanitized += char

    # Add ephemeral=True to make it only visible by you
    await interaction.response.send_message(f"{interaction.user.mention} is generating \"{sanitized}\"")

    # Generate image
    print(f"Generating {sanitized}")

    current_time = time.time()

    if platform.system() == "Windows":
        os.system(f"python AI-Horde-With-Cli/cli_request.py --prompt '{sanitized}'"
                  f" --api_key '{api_key}' -n 4 -f {current_time}.png")
    else:
        os.system(f"python3 AI-Horde-With-Cli/cli_request.py --prompt '{sanitized}'"
                  f" --api_key '{api_key}' -n 4 -f {current_time}.png")

    # Loop until image generates
    while True:
        if os.path.exists(f"0_{current_time}.png"):
            break
        else:
            continue

    for i in range(4):
        with open(f'{i}_{current_time}.png', 'rb') as file:
            picture = discord.File(file)
            await interaction.followup.send(file=picture)
        os.remove(f"{i}_{current_time}.png")


try:
    with open("bot_token.txt") as f:
        bot_token = f.read()
except FileNotFoundError:
    print("BOT TOKEN NOT FOUND! PUT YOUR BOT TOKEN IN `bot_token.txt`")

@bot.hybrid_command(name="dalleimagine", description="Generate image using DALLE")
async def images(ctx, *, prompt):
    url = "https://imagine.mishal0legit.repl.co"
    json_data = {"prompt": prompt}
    
    try:
        temp_message = await ctx.send("Sending post request to end point...")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get("image_url")
                    image_name = f"{prompt}.jpeg"
                    if image_url:
                        await download_image(image_url, image_name)
                        with open(image_name, 'rb') as file:
                            await temp_message.edit(content="Finished Image Generation")
                            await ctx.reply(file=discord.File(file))
                        os.remove(image_name)
                    else:
                        await temp_message.edit(content="An error occurred during image generation.")
                else:
                    await temp_message.edit(content="An error occurred with the server request.")
    except aiohttp.ClientError as e:
        await temp_message.edit(content=f"An error occurred while sending the request: {str(e)}")
    except Exception as e:
        await temp_message.edit(content=f"An error occurred: {str(e)}")

bot.run(bot_token)
