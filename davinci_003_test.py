from utils import bot_token
import discord
import aiohttp
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def generate_response(prompt):
    base_url = "http://chat.darkflow.top/api/openai/"
    error_base_url = "https://a.z-pt.com/api/openai/"
    arguments = "/v1/engines/text-davinci-003/completions"
    endpoint = base_url + arguments

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "prompt": prompt,
        "max_tokens": 800,
        "temperature": 0.8
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=data) as response:
                response_data = await response.json()
                return response_data["choices"][0]["text"]
    except aiohttp.ClientError:
        print("Error making the request retrying with fallback model")
        endpoint = error_base_url + arguments
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=data) as response:
                response_data = await response.json()
                return response_data["choices"][0]["text"]


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print("Generating from API...")
    async with message.channel.typing():
        await message.channel.send(await generate_response(message.content))


bot.run(bot_token)
