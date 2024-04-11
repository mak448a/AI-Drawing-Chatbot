import logging
import asyncio
import os

from helper_utils.utils import bot_token, config, FakeCtx, generate_message

import discord
from discord.ext import commands
from discord import app_commands
from cogs import COMMANDS, EVENT_HANDLERS



class CogBOT(commands.Bot):
    def __init__(self, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        for cog in COMMANDS:
            cog_name = cog.split('.')[-1]
            discord.client._log.info(f"Loaded Command {cog_name}")
            await self.load_extension(f"{cog}")
        for cog in EVENT_HANDLERS:
            cog_name = cog.split('.')[-1]
            discord.client._log.info(f"Loaded Event Handler {cog_name}")
            await self.load_extension(f"{cog}")


intents = discord.Intents.default()
intents.message_content = True
bot = CogBOT(command_prefix="/", intents=intents)

bot.run(bot_token, reconnect=True)
