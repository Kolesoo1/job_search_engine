import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('HH_ACCESS_TOKEN')}",
    "User-Agent": os.getenv('HH_USER_AGENT')
}

categories_response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles", headers=headers)

categories = {}

for cat_dict in categories_response.json()["categories"]:
    categories[cat_dict['id']] = cat_dict['name']

with open("categories.json", "w", encoding="utf-8") as file:
    json.dump(categories, file, ensure_ascii=False)


# Информационные технологии: id = 11