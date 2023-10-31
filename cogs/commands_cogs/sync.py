from discord.ext import commands


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def sync(self, ctx):
        await ctx.defer()
        await self.bot.tree.sync()
        await ctx.send("Successfully synced commands!")
        print("Synced commands!")


async def setup(bot):
    await bot.add_cog(Sync(bot))
