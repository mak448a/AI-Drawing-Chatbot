#! /bin/sh
FILE=venv/bin/activate

if [ -d "horde_module" ]
then
  :
else
  git clone https://github.com/mak448a/horde_module --depth=1
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

  echo -n "Enter your Poe token: "
  read POE_TOKEN

  echo -n "Enter your API Key: "
  read API_KEY
  # If token is none exit
  if [ -z $POE_TOKEN ] || [-z $TOKEN] || [-z $API_KEY]
  then
    echo "ERROR! YOU DIDN'T ENTER ALL YOUR CREDENTIALS!"
    exit 1
  fi

  # Overwrite existing file if it exists
  echo "BOT_TOKEN=$TOKEN" > .env
  echo "POE_TOKEN=$POE_TOKEN" >> .env
  echo "API_KEY=$API_KEY" >> .env
  python3 main.py
fi
