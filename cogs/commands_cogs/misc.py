import os

from discord.ext import commands
import discord
from discord import app_commands
from helper_utils.image_generation_utils import upscale_image, generate_prodia
from helper_utils.utils import clear_context, line_junk, config


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="upscale", description="Upscale an image with imaginepy")
    async def upscale(self, ctx, file: discord.Attachment):
        await ctx.defer()
        image_filename = await upscale_image(file)

        await ctx.send(file=discord.File(f"{image_filename}"))
        os.remove(image_filename)
    
    @commands.hybrid_command(name="imagine_prodia", description="Generate an image with Prodia")
    @app_commands.choices(model=[
        app_commands.Choice(name="SDXL 1.0",
                            value="SDXL 1.0")
    ])
    async def prodia(self, ctx, *, prompt, model: app_commands.Choice[str]):
        reply = await ctx.send(
            f"{ctx.message.author.mention} is generating ```{prompt}``` with "
            f"{model.name}! "
            f"{line_junk}{config['loading_gif']}")
        
        filename = await generate_prodia(prompt)
        await reply.edit(
            content=f"Here are the generated images for {ctx.author.mention}.\n- Prompt: ```{prompt}```\n- Model: `"
                    f"{model.name}`",
            attachments=[discord.File(filename),])
        
        os.remove(filename)

    @commands.hybrid_command(name="clear_context", description="Clear the chat context")
    async def clear(self, ctx):
        await ctx.defer()
        await clear_context()
        await ctx.send("Cleared the chat context!")


async def setup(bot):
    await bot.add_cog(Misc(bot))
