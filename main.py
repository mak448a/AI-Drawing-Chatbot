from utils import bot_token, config, line_junk, FakeCtx

# Figure out which model the user specified
if config["model"] == "GPT4All":
    # GPT4All
    from gpt_utils import generate_message
elif config["model"] == "ChatGPT":
    # ChatGPT
    from poe_utils import generate_message
else:
    # Fallback on ChatGPT
    from poe_utils import generate_message

from replit_detector import is_replit

if is_replit:
    from keep_alive import keep_alive

from image_generation_utils import generate_with_stable_horde, generate_image_with_imaginepy, upscale_image

import discord
from discord.ext import commands
from discord import app_commands

import urllib.parse
import requests

import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    # await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(
        name="Type / to see commands"))
    print(f"{bot.user.name} has connected to Discord!")
    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(administrator=False),
        scopes=("bot", "applications.commands"))
    print(f"Invite link: {invite_link}")


@bot.event
async def on_message(message):
    if str(bot.user.id) not in message.content:
        return

    if message.author == bot.user:
        return

    if is_replit and config["model"] == "GPT4All":
        print("You cannot use GPT4All with Replit.")
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
        # print(prompt)
        await imaginepy(
            FakeCtx(message),
            prompt,
            # app_commands.Choice(name="Realistic", value="REALISTIC"),  # NOQA
            app_commands.Choice(name="Imagine V4 Beta", value="IMAGINE_V4_Beta"),
            app_commands.Choice(name="1x1", value="RATIO_1X1"))


@bot.hybrid_command(name="imagine", description="Generate an image with Stable Diffusion")
@app_commands.choices(model=[
    app_commands.Choice(name="Stable Diffusion", value="stable_diffusion"),
    app_commands.Choice(name="Anything Diffusion", value="anything_diffusion")
])
async def imagine(ctx, *, prompt: str, model: app_commands.Choice[str]):
    model_name = 'Anything Diffusion' if model.value == 'anything_diffusion' else 'Stable Diffusion'

    temp_message = await ctx.send(
        f"{ctx.message.author.mention} is generating ```{prompt}``` with "
        f"{model_name}! "
        f"{line_junk}{config['loading_gif']}")

    print(f"{ctx.message.author.mention} is generating ```{prompt}``` with "
          f"{model_name}!")

    if model.value == "stable_diffusion":
        image_files, file_uuid = await generate_with_stable_horde(
            prompt, False, ctx)
    elif model.value == "anything_diffusion":
        image_files, file_uuid = await generate_with_stable_horde(
            prompt, True, ctx)
    else:
        print("This shouldn't happen, why did this happen?")
        return

    # await ctx.send(files=image_files)
    await ctx.send(
        f"Here are the generated images for {ctx.author.mention}.\n- Prompt: ```{prompt}```\n- Model: `"
        f"{model_name}`",
        files=image_files)

    # Cleanup
    await temp_message.delete()

    for i in range(4):
        os.remove(f"{i}_{file_uuid}.png")


@bot.hybrid_command(name="imaginepoly", description="Generate image using pollinations")
async def imaginepoly(ctx, *, prompt: str):
    encoded_prompt = urllib.parse.quote(prompt)
    images = []

    temp_message = await ctx.send(
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

    # Delete the temporary message
    await temp_message.delete()

    if images:
        # Send all image files as attachments in a single message
        image_files = [discord.File(image) for image in images]
        await ctx.send(
            content=f"Here are the generated images for {ctx.author.mention}.\n- Prompt: ```{prompt}```\n- Model: `"
            f"Pollinations`", files=image_files)

        # Delete the local image files
        for image in image_files:
            os.remove(image.filename)
    else:
        await ctx.send("Error generating images. Please try again later.")


@bot.hybrid_command(name="imaginepy", description="Generate image with imaginepy")
@app_commands.choices(style=[
    app_commands.Choice(name="Imagine V4 Beta", value="IMAGINE_V4_Beta"),
    app_commands.Choice(name="Realistic", value="REALISTIC"),
    app_commands.Choice(name="Anime", value="ANIME_V2"),
    app_commands.Choice(name="Disney", value="DISNEY"),
    app_commands.Choice(name="Studio Ghibli", value="STUDIO_GHIBLI"),
    app_commands.Choice(name="Graffiti", value="GRAFFITI"),
    app_commands.Choice(name="Medieval", value="MEDIEVAL"),
    app_commands.Choice(name="Fantasy", value="FANTASY"),
    app_commands.Choice(name="Neon", value="NEON"),
    app_commands.Choice(name="Cyberpunk", value="CYBERPUNK"),
    app_commands.Choice(name="Landscape", value="LANDSCAPE"),
    app_commands.Choice(name="Japanese Art", value="JAPANESE_ART"),
    app_commands.Choice(name="Steampunk", value="STEAMPUNK"),
    app_commands.Choice(name="Sketch", value="SKETCH"),
    app_commands.Choice(name="Comic Book", value="COMIC_BOOK"),
    app_commands.Choice(name="Imagine V4 creative", value="V4_CREATIVE"),
    app_commands.Choice(name="Imagine V3", value="IMAGINE_V3"),
    app_commands.Choice(name="Cosmic", value="COMIC_V2"),
    app_commands.Choice(name="Logo", value="LOGO"),
    app_commands.Choice(name="Pixel art", value="PIXEL_ART"),
    app_commands.Choice(name="Interior", value="INTERIOR"),
    app_commands.Choice(name="Mystical", value="MYSTICAL"),
    app_commands.Choice(name="Super realism", value="SURREALISM"),
    app_commands.Choice(name="Minecraft", value="MINECRAFT"),
    app_commands.Choice(name="Dystopian", value="DYSTOPIAN")
])
@app_commands.choices(ratio=[
    app_commands.Choice(name="1x1", value="RATIO_1X1"),
    app_commands.Choice(name="9x16", value="RATIO_9X16"),
    app_commands.Choice(name="16x9", value="RATIO_16X9"),
    app_commands.Choice(name="4x3", value="RATIO_4X3"),
    app_commands.Choice(name="3x2", value="RATIO_3X2")
])
async def imaginepy(ctx, prompt: str, style: app_commands.Choice[str],
                    ratio: app_commands.Choice[str]):
    temp_message = await ctx.send(
        f"{ctx.author.mention} is generating ```{prompt}``` with `Imaginepy`! {line_junk}"
        f"{config['loading_gif']}")
    filename = await generate_image_with_imaginepy(prompt, style.value,
                                                   ratio.value)
    await ctx.send(
        content=
        f"Here is the generated image for {ctx.author.mention}.\n- Prompt: ```{prompt}```\n- Style: `"
        f"{style.name}`",
        file=discord.File(filename))
    os.remove(filename)
    await temp_message.edit(content=f"Finished image generation!")
    await temp_message.delete()


@bot.hybrid_command(name="upscale", description="Upscale an image with imaginepy")
async def upscale(ctx, file: discord.Attachment):
    await ctx.defer()
    image_filename = await upscale_image(file)

    await ctx.send(file=discord.File(f"{image_filename}"))
    os.remove(image_filename)


@bot.hybrid_command(name="sync", description="Sync commands")
async def sync(ctx):
    await ctx.defer()
    await bot.tree.sync()
    await ctx.send("Successfully synced commands!")


if is_replit:
    keep_alive()

bot.run(bot_token)
