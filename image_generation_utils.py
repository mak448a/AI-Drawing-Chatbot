from horde_module import Generator
from utils import api_key
import uuid
import asyncio
import os
import discord
from imaginepy import AsyncImagine, Style, Ratio

horde_generator = Generator()


async def generate_with_stable_horde(prompt, use_anything_diffusion, ctx):
    file_uuid = uuid.uuid1()
    await horde_generator.generate(prompt, api_key, f"{file_uuid}.png", 4,
                                   f"{'Anything Diffusion' if use_anything_diffusion else 'stable_diffusion_2.1'}")

    # Loop until the images generate. We check for the fourth image.
    while True:
        if os.path.exists(f"3_{file_uuid}.png"):
            break
        await asyncio.sleep(0.8)

    images = []

    # Grab all the filenames
    for i in range(4):
        images.append(f"{i}_{file_uuid}.png")

    image_files = [discord.File(image) for image in images]

    return image_files, file_uuid


# Imaginepy function
async def generate_image_with_imaginepy(image_prompt, style_value, ratio_value):
    async_imagine = AsyncImagine()
    filename = str(uuid.uuid4()) + ".png"
    style_enum = Style[style_value]
    ratio_enum = Ratio[ratio_value]
    img_data = await async_imagine.sdprem(
        prompt=image_prompt,
        style=style_enum,
        ratio=ratio_enum
    )
    if img_data is None:
        print("An error occurred while generating the image.")
        return

    try:
        with open(filename, mode="wb") as img_file:
            img_file.write(img_data)
    except Exception as e:
        print(f"An error occurred while writing the image to file: {e}")
        return None

    await async_imagine.close()

    return filename


async def upscale_image(image):
    temp_id = uuid.uuid1()
    await image.save(f"{temp_id}.png")
    async_imagine = AsyncImagine()
    original_image = open(f"{temp_id}.png", "rb").read()
    upscaled_image = await async_imagine.upscale(original_image)

    with open(f"{temp_id}.png", "wb") as f:
        f.write(upscaled_image)
    return f"{temp_id}.png"
