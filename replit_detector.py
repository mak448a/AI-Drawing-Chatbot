from os import environ
import logging

# Solution from https://replit.com/talk/ask/Can-a-Python-script-detect-it-is-running-in-replit/24945
if "REPL_OWNER" in environ:
    is_replit = True
else:
    is_replit = False

logging.info("We're on Replit!" if is_replit else "We're not on Replit.")
