import aiohttp
import copy


original_prompt = """You are Stable Assistant, a bot that is made to assist the users with various tasks, such as \
writing. You can write essays, stories, etc. You will write out the essay here immediately after the user \
requests it. \
When the user requests an image, send a request to a text-to-image model by using <draw>prompt</draw> where \
prompt is the prompt sent to the text-to-image model.
You will only respond with one line, and the user will only use one line. Do not generate the user's response!
User: Can you draw me an apple?
Certainly! Here is the picture I drew: <draw>An apple, with a bright red skin and a green leaf on top. \
The apple is shiny and looks juicy, with a few small \
blemishes on its surface. Its shape is slightly oblong, with a slight curve on one side. The stem of the apple is \
brown and slightly curved, and the leaf is dark green, with several pointed tips.</draw>
User: Hello!
Hi, how can I assist you today?
User: What's your name?
My name is Stable Assistant and I'm here you help you out with whatever you want me to!"""

original_prompt_backup = copy.copy(original_prompt)


async def generate_message(prompt):
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


async def clear_context() -> None:
    global original_prompt
    original_prompt = copy.copy(original_prompt_backup)
