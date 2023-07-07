# AI Drawing ChatBot

![License](https://img.shields.io/github/license/mak448a/Stable-Diffusion-Bot)
![Contributors](https://img.shields.io/github/contributors/mak448a/Stable-Diffusion-Bot)
![Repo Size](https://img.shields.io/github/repo-size/mak448a/Stable-Diffusion-Bot)

This is an AI image generator Discord bot written in Python. It has a chatbot that uses ChatGPT!

This project uses various APIs, allowing it to run efficiently on less powerful computers.

**DISCLAIMER:** ChatGPT uses your Poe account. I am not responsible if your Poe account gets banned, as using Poe in programs is against their TOS.

![Demo](demo.png)

## Broken stuff
- Using text-davinci-003 as the chatbot model
- Using Imaginepy

## Table of Contents
1. [Features](#Features)
2. [Notes](#Notes)
3. [Prerequisites](#Prerequisites)
4. [Setup](#Setup)
5. [Configuration](#Configuration)
6. [Generate images faster with Stable Horde](#Generate-images-faster-with-Stable-Horde)

## Features
- ChatGPT chatbot that is integrated with Imaginepy
- 3 slash commands for generating images
- Stable Diffusion
- Anything Diffusion
- Pollinations

## Notes
- ChatGPT is the fastest model that you can use.
- While generating a response with GPT4All, the program locks up.
- Do not input any personal information on the `/imagine_poly` command because your generated image will be displayed on their official front page.
- Please do not enter any personal information in the Chatbot or in the image generators, as your prompts are sent to various providers.
- When you use Stable Horde to generate images, your prompts are sent to Stable Horde, as listed in their [privacy policy](https://stablehorde.net/privacy).
- The chatbot may not work as expected if multiple users are chatting with it at once.
- When using Replit, GPT4All cannot be used.
- When using Replit, you must input your .env variables in the `Secrets` button on Replit.

## Prerequisites
This project assumes that:
- Python 3.8+ is installed and is on your PATH
- Pip is installed
- Python-venv is installed (only for Debian-based distros)
- Git is installed
- You know how to create a Discord Bot account
- You know JSON syntax (It's basically a Python Dictionary)

## Setup
1. Create a Discord Bot and grab the token. Make sure to switch on Message Content Intent in the `Bot` tab of the [Developer Portal](https://discord.com/developers/applications).
2. Grab an API key from Stable Horde [at their register page](https://stablehorde.net/register).
3. Rename `example.env` to `.env` and place your bot token and your API key under `API_KEY`.
4. [Register](https://poe.com) for Poe and open the inspect tool. [Find your token](https://github.com/ading2210/poe-api#finding-your-token) and place it under `POE_TOKEN` in your `.env` file.
5. Place your Discord bot token under `BOT_TOKEN`.
6. Clone the Stable Horde module:
```shell
git clone https://github.com/mak448a/horde_module --depth=1
```
7. Create a virtual environment and install the dependencies:

Linux or MacOS:
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows:
```shell
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```
8. Rename `example_config.json` to `config.json`. Edit this file as needed. See [Configuration](#Configuration).
9. Run the bot and invite it using the link it provides.
10. Type `/` in the message box and try out the commands!
11. You can chat with the bot by mentioning the bot and typing your message.

Docker Method:
1. Make sure you have Docker installed on your machine.
2. Clone this repository to your local machine.
3. Rename `example.env` to `.env` and update the environment variable values in the file.
4. Build the Docker image using the following command:
   ```shell
   docker build -t ai-drawing-chatbot .
   ```
5. Run the Docker container using the following command:
   ```shell
   docker run -d --name chatbot ai-drawing-chatbot
   ```
6. The ChatBot should now be up and running inside the Docker container.

Please note that you need to replace the environment variable values in the `.env` file with your own values.

## Configuration
<details><summary>Configuring chat model</summary>
Go to `config.json` and set the value of the key `"model"` to the desired model.

**Available Models**
- ChatGPT
- GPT4All
- text-davinci-003

The model name must be written exactly as listed here.
When using ChatGPT, you must sign up for a Poe account.

When you are done, the edited line should look like this:
```json
"model": "ChatGPT",
```
</details>
<details><summary>Disable chatbot</summary>
Go to `config.json` and set the value of the key `"chatbot"` to `false`.

It should look like this:
```json
"chatbot": false,
```
</details>
<details><summary>Change loading GIF</summary>
Go to `config.json` and set the value of the key `"loading_gif"` to the URL of your preferred GIF from Tenor.

It should look like this:
```json
"loading_gif": "https://tenor.com/your/favorite/loading/gif",
```
</details>
<details><summary>Turn off command syncing (makes bot load faster)</summary>
Go to `config.json` and set the value of the key `"sync"` to `false`.

It should look like this:
```json
"sync": false
```
</details>

## Generate images faster with Stable Horde
Stable Horde uses Kudos to rank users on a queue. The more Kudos you have, the higher you are on the generation queue.
You can earn Kudos by rating images and/or generating images for Stable Horde on your local hardware.
To earn more Kudos, first add your API key [here](https://tinybots.net/artbot/settings).
Then, rate some images generated by other users [here](https://tinybots.net/artbot/rate).
After rating for a few minutes, you will have more Kudos!
**IMPORTANT: When an image says, "This rating must be x," you must rate it that. This picture is used as a Captcha to avoid spam.**
