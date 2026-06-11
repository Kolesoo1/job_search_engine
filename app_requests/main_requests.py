import os

from anyio.functools import lru_cache
from dotenv import load_dotenv

import requests

load_dotenv()


@lru_cache(maxsize=1)
def get_categories():
    response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles")
    data = response.json()
    categories = {}

    for cat_dict in data["categories"]:
        categories[cat_dict['id']] = cat_dict['name']

    return categories


@lru_cache(maxsize=1)
def get_roles_by_category_id(category_id: str):
    response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles")
    data = response.json()
    roles = {}

    for cat_dict in data["categories"]:
        if category_id == cat_dict["id"]:
            for role in cat_dict["roles"]:
                roles[role["id"]] = role["name"]
        else:
            continue

    return roles
