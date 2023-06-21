from utils import poe_key
import poe


client = poe.Client(poe_key)


async def generate_message(prompt: str) -> str:
    chunk = None
    for chunk in client.send_message("StableAssistant", prompt):
        pass
    return chunk["text"]


async def clear_context() -> None:
    client.send_chat_break("StableAssistant")
