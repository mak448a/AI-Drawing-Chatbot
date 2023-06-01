from os import environ

if "REPL_OWNER" in environ:
    is_replit = True
else:
    is_replit = False

print("We're replit" if is_replit else "We're on a normal machine")
