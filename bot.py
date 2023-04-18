import discord
from discord import app_commands
from discord.ext import commands
import platform
import os


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


# Load api key

try:
    with open("api_key.txt") as f:
        api_key = f.read()
except FileNotFoundError:
    api_key = "0000000000"
    print("No api key selected. Using anonymous account!")


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
    
    if platform.system() == "Windows":
        os.system(f"python AI-Horde/cli_request.py --prompt '{sanitized}' --api_key '{api_key}' -n 4")
    else:
        os.system(f"python3 AI-Horde/cli_request.py --prompt '{sanitized}' --api_key '{api_key}' -n 4")

    # Loop until image generates
    while True:
        if os.path.exists("0_horde_generation.png"):
            break
        else:
            continue
    
    for i in range(4):
        with open(f'{i}_horde_generation.png', 'rb') as f:
            picture = discord.File(f)
            await interaction.followup.send(file=picture)
        os.remove(f"{i}_horde_generation.png")


try:
    with open("bot_token.txt") as f:
        bot_token = f.read()
except FileNotFoundError:
    print("BOT TOKEN NOT FOUND! PUT YOUR BOT TOKEN IN `bot_token.txt`")

bot.run(bot_token)
