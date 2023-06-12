from utils import poe_key
import poe

# We use poe's built in bot builder for this.

client = poe.Client(poe_key)
# client.send_message("chinchilla", f)


async def generate_message(prompt: str) -> str:
    chunk = None
    for chunk in client.send_message("StableAssistant", prompt):
        pass
    print(chunk["text"])
    return chunk["text"]
