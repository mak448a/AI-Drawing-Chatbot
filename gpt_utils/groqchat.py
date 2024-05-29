from openai import AsyncOpenAI


client = AsyncOpenAI(base_url="https://api.groq.com/openai/v1", api_key="")

with open("gpt_utils/prompt.txt") as f:
    prompt = f.read()

messages = [{"role": "system", "content": prompt}]


async def generate_message(message: str) -> str:
    global messages

    messages.append({"role": "user", "content": message})
    response = await client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7,
        stream=False
    )

    return response.choices[0].message.content


async def clear_context() -> None:
    global prompt, messages
    with open("gpt_utils/prompt.txt") as file:
        prompt = file.read()
    messages = [{"role": "system", "content": prompt}]


if __name__ == "__main__":
    import asyncio
    print(asyncio.run(generate_message(input("You: "))))
