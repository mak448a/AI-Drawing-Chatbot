from gpt4all import GPT4All
import copy

llm = GPT4All("ggml-gpt4all-j-v1.3-groovy")

with open("gpt_utils/prompt.txt") as f:
    prompt = f.read()

remove_text = copy.copy(prompt)
original_prompt = copy.copy(prompt)


async def generate_message(user_input):
    global prompt, remove_text
    constructed = f"\nHuman: {user_input}\nStable Assistant: "
    prompt += constructed

    output_of_text = llm.generate(prompt)

    if "Human: " in output_of_text:
        print("Uh oh, generated extraneous text. Removing and sending cleaned output.")
        output_of_text = (
            output_of_text.split("Human: ")[1]
            + "\n NOTE: This may be the model generating"
            " an output for the user instead of itself."
        )

    # Solution taken from: https://groups.google.com/g/comp.lang.python/c/Rq40dmwLfMQ?pli=1
    if len(prompt) > 1000:
        print("Removing first two lines of context to avoid context explosion...")
        prompt = "\n".join(prompt.split("\n")[2:])
        remove_text = "\n".join(remove_text.split("\n")[2:])
    return output_of_text


async def clear_context():
    global prompt, remove_text
    prompt = copy.copy(original_prompt)
    remove_text = copy.copy(original_prompt)
