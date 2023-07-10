#! /bin/sh
FILE=venv/bin/activate

if [ -d "horde_module" ]
then
  echo "Already setup."
else
  echo "Not ready!"
  git clone https://github.com/mak448a/horde_module --depth=1
fi


if test -f "$FILE";
then
  echo "Already setup! Let's get running!"
  source venv/bin/activate
  python3 main.py
else
  cp "example_config.json" "config.json"
  touch .env
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  echo -n "Enter your bot token: "
  read TOKEN
  echo "BOT_TOKEN=$TOKEN" >> .env
  echo -n "Enter your Poe token: "
  read POE_TOKEN
  echo "POE_TOKEN=$POE_TOKEN" >> .env
  echo -n "Enter your API Key: "
  read API_KEY
  echo "API_KEY=$API_KEY" >> .env
  python3 main.py
fi
