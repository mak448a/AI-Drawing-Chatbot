import discord
from discord import app_commands
from discord.ext import commands
import platform
import os


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
intents = discord.Intents.all()

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

@bot.command(name="imagine")
async def imagine(ctx: commands.Context, *, prompt: str):
    sanitized = ""
    forbidden = ['"', "'", "`", "\\", "$"]

    for char in prompt:
        if char in forbidden:
            continue
        else:
            sanitized += char

    loading_message = await ctx.send(f"{ctx.author.mention} is generating \"{sanitized}\"")
    print(f"Generating {sanitized}")

    for i in range(10):
        await asyncio.sleep(0.3)
        await loading_message.edit(content=f"{ctx.author.mention} is generating \"{sanitized}\"{'.' * (i % 4)}")

    if platform.system() == "Windows":
        os.system(f"python AI-Horde/cli_request.py --prompt '{sanitized}' --api_key _QqEQbyCxoNXiuhN1Rlqlw -n 4")
    else:
        os.system(f"python3 AI-Horde/cli_request.py --prompt '{sanitized}' --api_key _QqEQbyCxoNXiuhN1Rlqlw -n 4")

    while True:
        if os.path.exists("0_horde_generation.png"):
            break
        else:
            continue

    for i in range(4):
        with open(f'{i}_horde_generation.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
        os.remove(f"{i}_horde_generation.png")

    await loading_message.edit(content=f"{ctx.author.mention} has generated \"{sanitized}\"")


try:
    with open("bot_token.txt") as f:
        bot_token = f.read()
except FileNotFoundError:
    print("BOT TOKEN NOT FOUND! PUT YOUR BOT TOKEN IN `bot_token.txt`")

bot.run(bot_token)
