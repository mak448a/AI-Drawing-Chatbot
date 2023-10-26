import os
import random
import requests
from discord.ext import commands
from utils import line_junk, config
import discord
import urllib.parse


class Pollinations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="imagine_poly", description="Generate image using Pollinations")
    async def imagine_poly(self, ctx, *, prompt: str):
        encoded_prompt = urllib.parse.quote(prompt)
        images = []

        reply = await ctx.send(
            f"{ctx.author.mention} is generating ```{prompt}``` with Pollinations! {line_junk}"
            f"{config['loading_gif']}")

        # Generate four images with the given prompt
        i = 0
        while len(images) < 4:
            seed = random.randint(1, 100000)  # Generate a random seed
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}{seed}"
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
                        f"Pollinations`", attachments=image_files)

            # Delete the local image files
            for image in image_files:
                os.remove(image.filename)
        else:
            await reply.edit("Error generating images. Please try again later.")


async def setup(bot):
    await bot.add_cog(Pollinations(bot))
