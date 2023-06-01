from utils import api_key, use_anything_diffusion, bot_token
from gpt_utils import generate_message
import discord
from discord.ext import commands
import platform
from replit_detector import is_replit
import time
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


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


@bot.event
async def on_message(message):
    if not is_replit:
        if message.author == bot.user:
            return
        try:
            async with message.channel.typing():
                msg = generate_message(message.content)
                print("Assistant said:", msg)
                await message.channel.send(msg)
        except:  # NOQA
            await message.channel.send("I had an error.")


@bot.hybrid_command(name="imagine", description="Generate an image")
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

    for i in range(4):
        with open(f'{i}_{current_time}.png', 'rb') as file:
            picture = discord.File(file)
            await ctx.send(file=picture)
        os.remove(f"{i}_{current_time}.png")


bot.run(bot_token)
