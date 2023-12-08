# Unmaintained, since vercel-llm-api seems to be broken.


# import vercel_ai
# import curl_cffi.requests.errors


# client = vercel_ai.Client()


# with open("gpt_utils/prompt.txt") as f:
#     prompt = f.read()


# async def generate_message(message: str) -> str:
#     global prompt

#     # Code from https://github.com/ading2210/vercel-llm-api/issues/12
#     retry, max_retries = 0, 15
#     prompt += f"{message}\n"

#     while retry < max_retries:
#         try:
#             result = ""
#             for chunk in client.generate("openai:gpt-3.5-turbo", prompt):
#                 # print(chunk, end="", flush=True)
#                 result += chunk

#             prompt += result + "\n"
#             # print(prompt)

#             return result
#         except curl_cffi.requests.errors.RequestsError:
#             retry += 1
#             # print(f"Retrying {retry}/{max_retries}...")
#             if retry == max_retries:
#                 raise Exception("Could not connect. Max retries exceeded.")
#             continue


# async def clear_context() -> None:
#     global prompt
#     with open("gpt_utils/prompt.txt") as file:
#         prompt = file.read()
