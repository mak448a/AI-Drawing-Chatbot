from discord.ext import commands
from helper_utils.utils import clear_context


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="clear_context", description="Clear the chat context")
    async def clear(self, ctx):
        await ctx.defer()
        await clear_context()
        await ctx.send("Cleared the chat context!")


async def setup(bot):
    await bot.add_cog(Misc(bot))
