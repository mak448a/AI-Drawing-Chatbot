from os import environ

# Solution from https://replit.com/talk/ask/Can-a-Python-script-detect-it-is-running-in-replit/24945
if "REPL_OWNER" in environ:
    is_replit = True
else:
    is_replit = False

print("We're replit" if is_replit else "We're on a normal machine")
