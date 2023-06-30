from gpt4all import GPT4All
import copy

llm = GPT4All("ggml-gpt4all-j-v1.3-groovy")


prompt = """You are Stable Assistant, a bot that is made to assist the users with various tasks, such as \
writing. You can write essays, stories, etc. You will write out the essay here immediately after the user \
requests it. \
When the user requests an image, send a request to a text-to-image model by using <draw>prompt</draw> where \
prompt is the prompt sent to the text-to-image model.
You will only respond with one line, and the user will only use one line. Do not generate the user's response!
User: Can you draw me an apple?
Stable Assistant: Certainly! Here is the picture I drew: <draw>An apple, with a bright red skin and a green leaf on top. \
The apple is shiny and looks juicy, with a few small \
blemishes on its surface. Its shape is slightly oblong, with a slight curve on one side. The stem of the apple is \
brown and slightly curved, and the leaf is dark green, with several pointed tips.</draw>
User: Hello!
Stable Assistant: Hi, how can I assist you today?
User: What's your name?
Stable Assistant: My name is Stable Assistant and I'm here you help you out with whatever you want me to!"""

remove_text = copy.copy(prompt)
original_prompt = copy.copy(prompt)


async def generate_message(user_input):
    global prompt, remove_text
    constructed = f"\nHuman: {user_input}\nStable Assistant: "
    prompt += constructed

    output_of_text = llm.generate(prompt)

    if "Human: " in output_of_text:
        print("Uh oh, generated extraneous text. Removing and sending cleaned output.")
        output_of_text = output_of_text.split("Human: ")[1] + "\n NOTE: This may be the model generating" \
                                                              " an output for the user instead of itself."

    # Solution taken from: https://groups.google.com/g/comp.lang.python/c/Rq40dmwLfMQ?pli=1
    if len(prompt) > 1000:
        print("Removing first two lines of context to avoid context explosion...")
        prompt = "\n".join(prompt.split('\n')[2:])
        remove_text = "\n".join(remove_text.split('\n')[2:])
    return output_of_text


async def clear_context():
    global prompt, remove_text
    prompt = copy.copy(original_prompt)
    remove_text = copy.copy(original_prompt)
