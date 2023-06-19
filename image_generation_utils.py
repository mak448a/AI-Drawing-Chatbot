from horde_module import Generator
from utils import api_key

import uuid
import asyncio
import logging
import os

import discord
from imaginepy import AsyncImagine, Style, Ratio

horde_generator = Generator()


async def generate_with_stable_horde(prompt: str, model: str):
    file_uuid = uuid.uuid1()

    await horde_generator.generate(prompt, api_key, f"{file_uuid}.png", 4,
                                   f"{model}")

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

    return image_files, images


# Imaginepy function
async def generate_image_with_imaginepy(image_prompt, style_value, ratio_value):
    async_imagine = AsyncImagine()

    filenames = []
    images = []

    style_enum = Style[style_value]
    ratio_enum = Ratio[ratio_value]

    for _ in range(4):
        filenames.append(str(uuid.uuid4()) + ".png")
        img_data = await async_imagine.sdprem(
            prompt=image_prompt,
            style=style_enum,
            ratio=ratio_enum
        )
        images.append(img_data)

    for i in images:
        if i is None:
            logging.error("An error occurred while generating the images.")
            return
    for index, filename in enumerate(filenames):
        try:
            with open(filename, mode="wb") as img_file:
                img_file.write(images[index])
        except Exception as e:
            logging.error(f"An error occurred while writing the image to file: {e}")
            return None

    await async_imagine.close()

    image_files = [discord.File(file) for file in filenames]

    return image_files


async def upscale_image(image):
    temp_id = uuid.uuid1()
    await image.save(f"{temp_id}.png")
    async_imagine = AsyncImagine()
    original_image = open(f"{temp_id}.png", "rb").read()
    upscaled_image = await async_imagine.upscale(original_image)

    with open(f"{temp_id}.png", "wb") as f:
        f.write(upscaled_image)
    return f"{temp_id}.png"
