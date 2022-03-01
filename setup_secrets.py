import os
import json
from secrets import SECRETS_STORE_PATH


secrets = {
    "OPEN_SOURCE_TOKEN": None,
}


if os.path.exists(SECRETS_STORE_PATH):
    res = input(
        "It is going to overwrite the existing secrets. Continue? (y/N) : ")

    if res != "y":
        quit()


for key in secrets.keys():
    value = input("{} : ".format(key))
    secrets[key] = value

with open(SECRETS_STORE_PATH, "w") as json_file:
    json.dump(secrets, json_file)

print("Secrets has been successfully update.")
