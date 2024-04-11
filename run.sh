#! /bin/sh
FILE=venv/bin/activate

if [ -d "helper_utils/horde_module" ]
then
  :
else
  git clone https://github.com/mak448a/horde_module helper_utils/horde_module --depth=1
fi


if test -f "$FILE";
then
  # We're setup
  source venv/bin/activate
  python3 main.py
else
  # We're not setup, let's get the tokens and API keys from the user
  # Let's also install dependencies
  cp "example_config.json" "config.json"
  touch .env
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  echo -n "Enter your bot token: "
  read TOKEN

  echo -n "Enter your Prodia API Key: "
  read PRODIA_KEY

  echo -n "Enter your Stable Horde API Key: "
  read API_KEY

  echo -n "Enter your ChatGPT Key: "
  read CHATGPT_KEY

  # If token is none exit
  if [ -z $PRODIA_KEY ] || [-z $TOKEN] || [-z $API_KEY]
  then
    echo "ERROR! YOU DIDN'T ENTER ALL YOUR CREDENTIALS!"
    exit 1
  fi

  # Overwrite existing file if it exists
  echo "BOT_TOKEN=$TOKEN" > .env
  echo "PRODIA_KEY=$PRODIA_KEY" >> .env
  echo "API_KEY=$API_KEY" >> .env
  echo "CHATGPT_KEY=$CHATGPT_KEY" >> .env
  python3 main.py
fi
