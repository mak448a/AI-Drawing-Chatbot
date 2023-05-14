# Stable Diffusion Bot

This is a stable diffusion Bot written in Python. It uses Stable Horde to generate the images.
As a result, all generated images will be sent back to LAION to train Stable Diffusion. If you don't want this, get an api key from [here](https://stablehorde.net/register) and place it in `api_key.txt`.
This repository assumes that you have Python installed. If you don't, [get Python](https://python.org/downloads). When you are installing, make sure to check the box "Add Python to PATH."


## Setup
Put your stable horde key in ```api_key.txt``` and put your bot token in ```bot_token.txt```. You can get a bot token at the [Discord Developer Portal](https://discord.com/developers/applications) and an api key at the [Stable Horde register page](https://stablehorde.net/register).

Next, run this command to clone the Stable Horde repository:
```shell
git clone 'https://github.com/db0/AI-Horde'
```

If you are on Linux or MacOS, run these commands to install the dependencies:
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r AI-Horde/cli_requirements.txt
```

If you are on Windows, run these commands to install the dependencies:
```shell
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
pip install -r AI-Horde/cli_requirements.txt
```


## How to get faster image generations
Stable Horde uses as system called Kudos to rank users on a queue. The more Kudos you have, the higher you are on the queue. To get more Kudos, first stick your api key in at [this page](https://tinybots.net/artbot/settings). Then, rate some images at [this page](https://tinybots.net/artbot/rate). After rating a few, you should have gotten a bunch more Kudos!
