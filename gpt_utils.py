from gpt4all import GPT4All
import copy

llm = GPT4All("ggml-gpt4all-j-v1.3-groovy")

# prompt = """\
# System: You are Assistant, who was created to assist the user. You can draw pictures for the user with \
# <draw>"prompt"<draw> where "prompt" is your prompt to the text to image ai.
# Human: Draw me a picture of an apple.
# Assistant: Here's my attempt at drawing an apple: <draw>"apple"<draw>
# Human: Hi!
# Assistant: Hello!"""
prompt = """\
System: You are Assistant, who was created to assist the user.
Human: Hey
Assistant: Hello! What can I assist you with today?"""


remove_text = copy.copy(prompt)


def generate_message(user_input, first_time=True):
    global prompt, remove_text
    if first_time:
        constructed = f"\nHuman: {user_input}\nAssistant: "
        prompt += constructed

    output_of_text = llm.generate(prompt)

    if "Human: " in output_of_text:
        print("Uh oh, generated human response. Retrying...")
        return generate_message(user_input, first_time=False)

    # Solution taken from: https://groups.google.com/g/comp.lang.python/c/Rq40dmwLfMQ?pli=1
    if len(prompt) > 1000:
        print("Removing first two lines of context to avoid context explosion...")
        prompt = "\n".join(prompt.split('\n')[2:])
        remove_text = "\n".join(remove_text.split('\n')[2:])
    return output_of_text
