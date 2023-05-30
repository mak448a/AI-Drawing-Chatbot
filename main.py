import discord
from discord.ext import commands
import platform
import os
import time
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# Load api key
try:
    with open("api_key.txt") as f:
        api_key = f.read()
except FileNotFoundError:
    api_key = "0000000000"
    print("No API key selected. Using anonymous account.")

# Check if enable anything_diffusion_enable.txt.txt exists
if os.path.exists("anything_diffusion_enable.txt"):
    use_anything_diffusion = True
    print("Using Anything Diffusion")
else:
    print("Using Stable Diffusion")
    use_anything_diffusion = False


@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="Try /imagine"))
    print(f"{bot.user.name} has connected to Discord!")
    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(administrator=False),
        scopes=("bot", "applications.commands")
    )
    print(f"Invite link: {invite_link}")


@bot.hybrid_command(name="imagine", description="Generate an image with Stable Diffusion")
async def imagine(ctx, *, prompt: str):
    sanitized = ""
    forbidden = ['"', "'", "`", "\\", "$"]

    for char in prompt:
        if char in forbidden:
            continue
        else:
            sanitized += char

    await ctx.send(f"{ctx.message.author.mention} is generating \"{sanitized}\"")

    print(f"{ctx.message.author.name} is generating \"{sanitized}\"")

    current_time = time.time()

    os.system(f"python{'3' if platform.system() != 'Windows' else ''} "
              f"AI-Horde-With-Cli/cli_request.py --prompt '{sanitized}'"
              f" --api_key '{api_key}' -n 4 -f {current_time}.png {'--anything' if use_anything_diffusion else ''}")

    # Loop until image generates
    while True:
        if os.path.exists(f"0_{current_time}.png"):
            break
        else:
            await asyncio.sleep(0.8)
            continue

    for i in range(4):
        with open(f'{i}_{current_time}.png', 'rb') as file:
            picture = discord.File(file)
            await ctx.send(file=picture)
        os.remove(f"{i}_{current_time}.png")


try:
    with open("bot_token.txt") as f:
        bot_token = f.read()
except FileNotFoundError:
    print("BOT TOKEN NOT FOUND! PLACE YOUR BOT TOKEN IN `bot_token.txt`.")

bot.run(bot_token)
