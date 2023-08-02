from InquirerPy import inquirer

token = inquirer.text(message="Bot Token:").execute()
key = inquirer.text(message="API Key for Stable Horde:").execute()
poe = inquirer.text(message="Poe Token:").execute()
model = inquirer.select(
    message="Choose model:",
    choices=["ChatGPT", "GPT4All"],
).execute()

print(token, model, key, poe)
