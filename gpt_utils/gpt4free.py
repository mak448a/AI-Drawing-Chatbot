import g4f
import aiohttp



with open("gpt_utils/prompt.txt") as f:
    prompt = f.read()

messages = [{"role": "system", "content": prompt}]

async def generate_message(message: str) -> str:
    global prompt

    messages.append({"role": "user", "content": message})

    try:
        response = await g4f.ChatCompletion.create_async(
            model="meta-llama/Llama-2-70b-chat-hf",
            provider=g4f.Provider.HuggingChat,
            messages=messages,
            stream=False
        )
        messages.append({"role": "assistant", "content": response})
    except aiohttp.client_exceptions.ClientResponseError:
        response = await g4f.ChatCompletion.create_async(
            model="meta-llama/Llama-2-70b-chat-hf",
            provider=g4f.Provider.HuggingChat,
            messages=messages,
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
