import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('HH_ACCESS_TOKEN')}",
    "User-Agent": os.getenv('HH_USER_AGENT')
}

response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles", headers=headers)

roles = {}

for cat_dict in response.json()["categories"]:
    if cat_dict["id"] == "11":
        for role in cat_dict["roles"]:
            roles[role["id"]] = role["name"]
        break
    else:
        continue

with open("roles.json", "w", encoding="UTF-8") as file:
    json.dump(roles, file, ensure_ascii=False)
