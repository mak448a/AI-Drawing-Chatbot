import logging
import os

from discord.ext import commands
from discord import app_commands
from helper_utils.utils import line_junk, config
from helper_utils.image_generation_utils import generate_with_stable_horde

import discord
from helper_utils.image_generation_utils import upscale_image, generate_prodia
import random
import requests
import urllib.parse


class GenerativeImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="upscale", description="Upscale an image with imaginepy"
    )
    async def upscale(self, ctx, file: discord.Attachment):
        await ctx.defer()
        image_filename = await upscale_image(file)

        await ctx.send(file=discord.File(f"{image_filename}"))
        os.remove(image_filename)

    @commands.hybrid_group(
        invoke_without_command=False,
        name="imagine",
        description="Generative image related command group",
    )
    async def imagine(self, ctx) -> None:
        pass

    @imagine.hybrid_command(
        name="poly", description="Generate image using Pollinations"
    )
    async def imagine_poly(self, ctx, *, prompt: str):
        encoded_prompt = urllib.parse.quote(prompt)
        images = []

        reply = await ctx.send(
            f"{ctx.author.mention} is generating ```{prompt}``` with Pollinations! {line_junk}"
            f"{config['loading_gif']}"
        )

        # Generate four images with the given prompt
        i = 0
        while len(images) < 4:
            seed = random.randint(1, 100000)  # Generate a random seed
            image_url = (
                f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
            )
            response = requests.get(image_url)

            try:
                image_data = response.content

                # Generate a unique filename for each image
                filename = f"{ctx.author.id}_{ctx.message.id}_{i}.png"
                with open(filename, "wb") as f:
                    f.write(image_data)

                images.append(filename)
                i += 1
            except (requests.exceptions.RequestException, ValueError, KeyError) as e:
                print(f"Error generating image: {e}")

        if images:
            # Send all image files as attachments in a single message
            image_files = [discord.File(image) for image in images]
            await reply.edit(
                content=f"Here are the generated images for {ctx.author.mention}.\n- Prompt: ```{prompt}```\n- Model: `"
                f"Pollinations`",
                attachments=image_files,
            )

            # Delete the local image files
            for image in image_files:
                os.remove(image.filename)
        else:
            await reply.edit("Error generating images. Please try again later.")

    @imagine.hybrid_command(name="prodia", description="Generate an image with Prodia")
    @app_commands.choices(
        model=[app_commands.Choice(name="SDXL 1.0", value="SDXL 1.0")]
    )
    async def prodia(self, ctx, *, prompt, model: app_commands.Choice[str]):
        reply = await ctx.send(
            f"{ctx.message.author.mention} is generating ```{prompt}``` with "
            f"{model.name}! "
            f"{line_junk}{config['loading_gif']}"
        )

        filename = await generate_prodia(prompt)
        await reply.edit(
            content=f"Here are the generated images for {ctx.author.mention}.\n- Prompt: ```{prompt}```\n- Model: `"
            f"{model.name}`",
            attachments=[
                discord.File(filename),
            ],
        )

        os.remove(filename)

    @imagine.hybrid_command(
        name="horde", description="Generate an image with Stable Horde"
    )
    @app_commands.choices(
        model=[
            app_commands.Choice(name="SDXL 1.0", value="SDXL 1.0"),
            app_commands.Choice(name="Stable Diffusion", value="stable_diffusion_2.1"),
            app_commands.Choice(
                name="SDXL Beta (WILL BE SHARED FOR IMPROVEMENT OF THE MODELS)",
                value="SDXL_beta::stability.ai#6901",
            ),
            app_commands.Choice(name="Deliberate", value="Deliberate"),
            app_commands.Choice(name="Anything Diffusion", value="Anything Diffusion"),
            app_commands.Choice(name="Realistic Vision", value="Realistic Vision"),
            app_commands.Choice(name="Dreamshaper", value="Dreamshaper"),
            app_commands.Choice(name="Abyss OrangeMix", value="Abyss OrangeMix"),
            app_commands.Choice(
                name="OpenJourney Diffusion", value="OpenJourney Diffusion"
            ),
            app_commands.Choice(
                name="Original Stable Diffusion", value="stable_diffusion"
            ),
            app_commands.Choice(
                name="ICBINP - I Can't Believe It's Not Photography",
                value="ICBINP - I Can't Believe It's Not Photography",
            ),
        ]
    )
    async def imagine_horde(
        self, ctx, *, prompt: str, model: app_commands.Choice[str], negative: str = None
    ):
        reply = await ctx.send(
            f"{ctx.message.author.mention} is generating ```{prompt}``` with "
            f"{model.name}! "
            f"{line_junk}{config['loading_gif']}"
        )

        logging.debug(
            f"{ctx.message.author.mention} is generating ```{prompt}``` with "
            f"{model.name}!"
        )

        # `###` tells Stable Horde we want a negative prompt.
        image_files, images = await generate_with_stable_horde(
            f"{prompt}{'###' if negative else ''}{negative if negative else ''}",
            model.value,
        )

        if negative:
            negative_string = f"\n- Negative Prompt: ```{negative}```"
        else:
            negative_string = ""

        await reply.edit(
            content=f"Here are the generated images for {ctx.author.mention}.\n- Prompt: ```{prompt}```\n- Model: `"
            f"{model.name}`{negative_string}",
            attachments=image_files,
        )

        for image in images:
            os.remove(image)


async def setup(bot):
    await bot.add_cog(GenerativeImage(bot))