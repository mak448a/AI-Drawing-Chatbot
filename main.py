import logging
import asyncio
import os

from utils import bot_token, config, FakeCtx, generate_message

import discord
from discord.ext import commands
from discord import app_commands
from replit_detector import is_replit

if is_replit:
    from keep_alive import keep_alive


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def load():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()
    await bot.start(bot_token)


@bot.event
async def on_ready():
    if config["sync"]:
        logging.info("Syncing bot commands, please be patient!")
        await bot.tree.sync()
    else:
        logging.info("Not syncing bot commands")

    await bot.change_presence(activity=discord.Game(
        name="Type / to see commands"))
    logging.debug(f"{bot.user.name} has connected to Discord!")
    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(administrator=False),
        scopes=("bot", "applications.commands"))
    logging.info(f"Invite link: {invite_link}")


@bot.event
async def on_message(message):
    if str(bot.user.id) not in message.content:
        return
    if not config["chatbot"]:
        return
    if is_replit and config["model"] == "GPT4All":
        logging.error("You cannot use GPT4All with Replit.")
        return
    if message.author == bot.user:
        return

    cleaned_message = message.content.replace(f"<@{bot.user.id}>", "")

    async with message.channel.typing():
        msg = await generate_message(cleaned_message)

    msg1 = msg.split("<draw>")[0]

    # Check if the model wants to draw something
    if "<draw>" in msg:
        await message.channel.send(msg1)
    else:
        await message.channel.send(msg)

    if "<draw>" in msg and "</draw>" in msg:
        # Parse the draw tag
        prompt = msg.split("<draw>")[1].split("</draw>")[0]

        logging.debug(f"{message.author.mention} is generating ```{prompt}``` with "
                      f"{config['image_model']}!")

        await bot.get_cog("Horde").imagine_horde(  # Get cog Horde (cogs/horde.py) and then call imagine_horde
            FakeCtx(message),  # NOQA
            prompt=prompt,
            model=app_commands.Choice(name=config["image_model"], value=config["image_model"])
        )


if is_replit:
    keep_alive()

asyncio.run(main())
