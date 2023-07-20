@echo off
set FILE=venv\Scripts\activate

if exist horde_module (
  goto setup
) else (
  echo Downloading horde_module repository...
  curl -LJO https://github.com/mak448a/horde_module/archive/refs/heads/main.zip
  echo Extracting repository...
  powershell -command "Expand-Archive -Path .\main.zip -DestinationPath .\horde_module -Force"
  del main.zip
)

:setup
if exist %FILE% (
  call venv\Scripts\activate
  python main.py
) else (
  copy example_config.json config.json
  echo > .env
  python -m venv venv
  call venv\Scripts\activate
  pip install -r requirements.txt
  set /p TOKEN=Enter your bot token: 
  echo BOT_TOKEN=%TOKEN% > .env
  set /p POE_TOKEN=Enter your Poe token: 
  echo POE_TOKEN=%POE_TOKEN% >> .env
  set /p API_KEY=Enter your API Key: 
  echo API_KEY=%API_KEY% >> .env
  if [%TOKEN%]==[] (
    goto fail
  )
  if [%TOKEN%]==[] (
    goto fail
  )
  if [%POE_TOKEN%]==[] (
    goto fail
  )
  if [%API_KEY%]==[] (
    goto fail
  )
  python main.py
)

:fail
echo ERROR! YOU DIDN'T ENTER ALL YOUR CREDENTIALS!
EXIT /b 1
