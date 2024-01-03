import logging
import os

from discord.ext import commands
from discord import app_commands
from helper_utils.utils import line_junk, config
from helper_utils.image_generation_utils import generate_with_stable_horde


class Horde(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="imagine_horde", description="Generate an image with Stable Horde")
    @app_commands.choices(model=[
        app_commands.Choice(name="SDXL 1.0",
                            value="SDXL 1.0"),
        app_commands.Choice(name="Stable Diffusion", value="stable_diffusion_2.1"),
        app_commands.Choice(name="SDXL Beta (WILL BE SHARED FOR IMPROVEMENT OF THE MODELS)",
                            value="SDXL_beta::stability.ai#6901"),
        app_commands.Choice(name="Deliberate", value="Deliberate"),
        app_commands.Choice(name="Anything Diffusion", value="Anything Diffusion"),
        app_commands.Choice(name="Realistic Vision", value="Realistic Vision"),
        app_commands.Choice(name="Dreamshaper", value="Dreamshaper"),
        app_commands.Choice(name="Abyss OrangeMix", value="Abyss OrangeMix"),
        app_commands.Choice(name="OpenJourney Diffusion", value="OpenJourney Diffusion"),
        app_commands.Choice(name="Original Stable Diffusion", value="stable_diffusion"),
        app_commands.Choice(name="ICBINP - I Can't Believe It's Not Photography",
                            value="ICBINP - I Can't Believe It's Not Photography"),
    ])
    
    async def imagine_horde(self, ctx, *, prompt: str, model: app_commands.Choice[str], negative: str = None):
        reply = await ctx.send(
            f"{ctx.message.author.mention} is generating ```{prompt}``` with "
            f"{model.name}! "
            f"{line_junk}{config['loading_gif']}")

        logging.debug(f"{ctx.message.author.mention} is generating ```{prompt}``` with "
                      f"{model.name}!")

        # `###` tells Stable Horde we want a negative prompt.
        image_files, images = await generate_with_stable_horde(
            f"{prompt}{'###' if negative else ''}{negative if negative else ''}", model.value)

        if negative:
            negative_string = f"\n- Negative Prompt: ```{negative}```"
        else:
            negative_string = ""

        await reply.edit(
            content=f"Here are the generated images for {ctx.author.mention}.\n- Prompt: ```{prompt}```\n- Model: `"
                    f"{model.name}`{negative_string}",
            attachments=image_files)

        for image in images:
            os.remove(image)


async def setup(bot):
    await bot.add_cog(Horde(bot))
