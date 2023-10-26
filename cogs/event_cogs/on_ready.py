import discord
from discord.ext import commands
import logging
from helper_utils.utils import config

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if config["sync"]:
            logging.info("Syncing bot commands, please be patient!")
            await self.bot.tree.sync()
        else:
            logging.info("Not syncing bot commands")

        await self.bot.change_presence(activity=discord.Game(
            name="Type / to see commands"))
        logging.debug(f"{bot.user.name} has connected to Discord!")
        invite_link = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=discord.Permissions(administrator=False),
            scopes=("bot", "applications.commands"))
        logging.info(f"Invite link: {invite_link}")

async def setup(bot):
    await bot.add_cog(OnReady(bot))
