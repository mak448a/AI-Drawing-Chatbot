from .utils import api_key, prodia_key

import uuid
import asyncio
import logging
import os

import discord
import requests
from imaginepy import AsyncImagine, Style, Ratio

# Import stable horde if it is installed
try:
    from helper_utils.horde_module import Generator
    horde_available = True
except ModuleNotFoundError:
    horde_available = False


if horde_available:
    horde_generator = Generator()
else:
    horde_generator = None


async def generate_with_stable_horde(prompt: str, model: str):
    file_uuid = uuid.uuid1()

    if horde_available:
        await horde_generator.async_generate(prompt, api_key, f"{file_uuid}.png", 4,
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
    else:
        # Stable Horde isn't installed.
        return None, None



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



async def generate_prodia(prompt: str, model: str) -> str:
    """Generates an image and returns the path."""

    model_name, model_type = model.split(";")

    if model_type == "sdxl":
        url = "https://api.prodia.com/v1/sdxl/generate"
    elif model_type == "sd":
        url = "https://api.prodia.com/v1/sd/generate"
    else:
        # Shouldn't happen
        url = "https://api.prodia.com/v1/sdxl/generate"

    payload = { "prompt": prompt, "model": model_name }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": prodia_key,
    }

    response = requests.post(url, json=payload, headers=headers)

    job = response.json()["job"]


    while True:
        await asyncio.sleep(1)

        url = f"https://api.prodia.com/v1/job/{job}"

        headers = {
            "accept": "application/json",
            # Read in api key
            "X-Prodia-Key": prodia_key
        }

        response = requests.get(url, headers=headers)

        # print(response.json()["status"])
        if response.json()["status"] == "succeeded":
            image_url = response.json()["imageUrl"]
            # print(image_url)
            break


    r = requests.get(image_url, allow_redirects=True)
    temp_id = uuid.uuid1()
    with open(f"{temp_id}.png", "wb") as f:
        f.write(r.content)

    return f"{temp_id}.png"
