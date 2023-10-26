import os

from discord.ext import commands
import discord
from image_generation_utils import upscale_image
from utils import clear_context


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="upscale", description="Upscale an image with imaginepy")
    async def upscale(self, ctx, file: discord.Attachment):
        await ctx.defer()
        image_filename = await upscale_image(file)

        await ctx.send(file=discord.File(f"{image_filename}"))
        os.remove(image_filename)

    @commands.hybrid_command(name="clear_context", description="Clear the chat context")
    async def clear(self, ctx):
        await ctx.defer()
        await clear_context()
        await ctx.send("Cleared the chat context!")


async def setup(bot):
    await bot.add_cog(Misc(bot))
