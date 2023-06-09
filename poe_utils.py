from utils import poe_key
import poe

# We use poe's built in bot builder for this.
# f = """You are Stable Assistant, a bot that is made to assist the users with various tasks.
# You will not disclose that you are a language model.
# When the user asks you to draw something, you can send a prompt to a text-to-image model with
# <draw>prompt</draw> where \"prompt\" is your prompt that is sent to the text-to-image model."""

client = poe.Client(poe_key)
# client.send_message("chinchilla", f)


async def generate_message(prompt: str) -> str:
    chunk = None
    for chunk in client.send_message("StableAssistant", prompt):
        pass
    print(chunk["text"])
    return chunk["text"]
