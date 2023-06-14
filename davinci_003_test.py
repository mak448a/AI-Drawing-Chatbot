from utils import bot_token
import discord
import aiohttp
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


original_prompt = """You are Stable Assistant, a bot that is made to assist the users with various tasks, such as \
writing and drawing. You can write essays, stories, etc. You will write out the essay here immediately after the user \
requests it. \
You will only respond with one line, and the user will only use one line. Do not generate the user's response!
User: Hello!
Hi, how can I assist you today?
User: What's your name?
My name is Stable Assistant and I'm here you help you out with whatever you want me to!"""


async def generate_response(prompt):
    global original_prompt
    base_url = "http://chat.darkflow.top/api/openai/"
    error_base_url = "https://a.z-pt.com/api/openai/"
    arguments = "/v1/engines/text-davinci-003/completions"
    endpoint = base_url + arguments

    headers = {
        "Content-Type": "application/json",
    }

    # Get rid of new lines
    prompt = prompt.replace("\n", " ")

    original_prompt = original_prompt + "\nUser: " + prompt + "\n"
    prompt = original_prompt
    data = {
        "prompt": prompt,
        "max_tokens": 800,
        "temperature": 0.8
    }

    print(data)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=data) as response:
                response_data = await response.json()
                original_prompt += response_data["choices"][0]["text"]
                return response_data["choices"][0]["text"]
    except aiohttp.ClientError:
        print("Error making the request retrying with fallback model")
        endpoint = error_base_url + arguments
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=data) as response:
                response_data = await response.json()
                original_prompt += response_data["choices"][0]["text"]
                return response_data["choices"][0]["text"]


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print("Generating from API...")
    async with message.channel.typing():
        await message.channel.send(await generate_response(message.content))


bot.run(bot_token)
