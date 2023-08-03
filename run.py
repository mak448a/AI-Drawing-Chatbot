from InquirerPy import inquirer
import os
import logging


if not os.path.exists(".env"):
    token = inquirer.text(message="Bot Token:").execute()
    key = inquirer.text(message="API Key for Stable Horde:").execute()
    poe = inquirer.text(message="Poe Token:").execute()
    model = inquirer.select(
        message="Choose model:",
        choices=["ChatGPT", "GPT4All"],
    ).execute()
    print("Launching program...")
    import main  # NOQA
else:
    option = inquirer.select(
        message="Select Option:",
        choices=["Run", "Configure"],
    ).execute()
    if option == "Run":
        print("Launching program...")
        import main  # NOQA
    elif option == "Configure":
        model = inquirer.select(
            message="Choose model:",
            choices=["ChatGPT (default)", "GPT4All"],
        ).execute()
        loading_gif = inquirer.text(
            message="Paste gif (press enter to leave empty)"
        ).execute()
        if "https://" in loading_gif.lower():
            print("They have a loading gif!")
        elif loading_gif:
            logging.log(logging.WARNING, "Invalid input!!!")
        else:
            # Use default one
            pass
        print(model)
        print("Launching program...")
        import main  # NOQA
