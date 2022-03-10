import os
import json
from secrets import SECRETS_STORE_PATH


secrets = {
    "OPEN_SOURCE_TOKEN": None,
    "GUILD_ID": None
}


if os.path.exists(SECRETS_STORE_PATH):
    res = input(
        "Do you want to overwrite existing secret tokens? yes/no: ")

    if res.lower() != "yes":
        quit()


for key in secrets.keys():
    value = input("{} : ".format(key))
    secrets[key] = value

with open(SECRETS_STORE_PATH, "w") as json_file:
    json.dump(secrets, json_file)

print("Secret tokens have been successfully updated!")
