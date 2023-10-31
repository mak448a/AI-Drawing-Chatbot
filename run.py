from InquirerPy import inquirer
import logging
import json
import os
from helper_utils import replit_detector


logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(message)s")


def configure():
    print("For all options, choose the first option if unsure.")
    model = inquirer.select(
        message="Choose model:",
        choices=["gpt-3.5-turbo", "GPT4All", "None"],
    ).execute()
    sync_commands = inquirer.select(
        message="Bot command syncing:",
        choices=["On", "Off"],
    ).execute()
    loading_gif = inquirer.text(
        message="Paste gif link: (press enter to use default)"
    ).execute()

    # Error checking for loading GIF
    if "https://" in loading_gif.lower():
        # A loading gif was found
        pass
    elif loading_gif:
        logging.log(logging.WARNING, "Invalid input!!! Using default link.")
        loading_gif = ""
    else:
        # Use default one
        loading_gif = ""

    # Define default config values
    default_config = {
        "chatbot": True,
        "model": "gpt-3.5-turbo",
        "loading_gif": "https://tenor.com/view/loading-gif-9212724",
        "sync": True,
        "image_model": "stable_diffusion_2.1"
    }
    # Set a variable to store new config
    config = default_config  # add .copy() if you want it to be separate
    # Models
    if model == "None":
        config["chatbot"] = False
    elif model == "GPT4All":
        config["model"] = "GPT4All"
    else:
        config["model"] = "gpt-3.5-turbo"
    # GIF
    if loading_gif:
        config["loading_gif"] = loading_gif
    # Syncing
    if sync_commands == "On":
        config["sync"] = True
    else:
        config["sync"] = False

    # Write our config to the config file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def get_credentials():
    if replit_detector.is_replit:
        print("On replit, add credentials normally")
        return
    while True:
        token = inquirer.text(message="Bot Token:").execute()
        key = inquirer.text(message="API Key for Stable Horde:").execute()
        poe = inquirer.text(message="Poe Token:").execute()
        lines = f"""\
BOT_TOKEN={token}
POE_TOKEN={poe}
API_KEY={key}"""
        if token == "" or key == "" or poe == "":
            print("Enter valid input.")
            continue
        else:
            break

    with open(".env", "w") as f:
        f.writelines(lines)


while True:
    if not os.path.exists(".env"):
        get_credentials()
        configure()
        print("Launching program...")
        import main  # NOQA
    else:
        option = inquirer.select(
            message="Select Option:",
            choices=["Run", "Configure", "Add Credentials"],
        ).execute()
        if option == "Run":
            print("Launching program...")
            import main  # NOQA
        elif option == "Configure":
            configure()
        elif option == "Add Credentials":
            get_credentials()
