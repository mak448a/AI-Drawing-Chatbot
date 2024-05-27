import g4f
import aiohttp
from helper_utils.utils import chatgpt_key



with open("gpt_utils/prompt.txt") as f:
    prompt = f.read()

messages = [{"role": "system", "content": prompt}]

async def generate_message(message: str) -> str:
    global prompt

    messages.append({"role": "user", "content": message})

    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_35_turbo,
            provider=g4f.Provider.OpenaiChat,
            messages=messages,
            access_token=chatgpt_key,
            stream=False
        )
        messages.append({"role": "assistant", "content": response})
    except aiohttp.client_exceptions.ClientResponseError:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_35_turbo,
            provider=g4f.Provider.OpenaiChat,
            messages=messages,
            access_token=chatgpt_key,
            stream=False
        )
        messages.append({"role": "assistant", "content": response})
    print(response)
    return response


async def clear_context() -> None:
    global prompt, messages
    with open("gpt_utils/prompt.txt") as file:
        prompt = file.read()
    messages = [{"role": "system", "content": prompt}]
