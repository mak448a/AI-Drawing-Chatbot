import discord
from discord import app_commands
from discord.ext import commands
import disnake
import platform
import os


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
intents = disnake.Intents.all()

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

@bot.slash_command(name="imagine")
async def imagine(inter: disnake.ApplicationCommandInteraction, prompt: str):
    sanitized = ""
    forbidden = ['"', "'", "`", "\\", "$"]

    for char in prompt:
        if char in forbidden:
            continue
        else:
            sanitized += char

    await inter.response.send_message(f"{inter.user.mention} is generating \"{sanitized}\"")

    print(f"Generating {sanitized}")

    if platform.system() == "Windows":
        os.system(f"python AI-Horde/cli_request.py --prompt '{sanitized}' --api_key '{api_key}' -n 4")
    else:
        os.system(f"python3 AI-Horde/cli_request.py --prompt '{sanitized}' --api_key '{api_key}' -n 4")

    while True:
        if os.path.exists("0_horde_generation.png"):
            break
        else:
            continue

    for i in range(4):
        with open(f'{i}_horde_generation.png', 'rb') as f:
            picture = disnake.File(f)
            await inter.followup.send(file=picture)
        os.remove(f"{i}_horde_generation.png")


try:
    with open("bot_token.txt") as f:
        bot_token = f.read()
except FileNotFoundError:
    print("BOT TOKEN NOT FOUND! PUT YOUR BOT TOKEN IN `bot_token.txt`")

bot.run(bot_token)
