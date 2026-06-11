import os
from http.client import HTTPException

from anyio.functools import lru_cache
from dotenv import load_dotenv

import requests

load_dotenv()

headers = {
    "User-Agent": os.getenv('HH_USER_AGENT'),
    "Authorization": f"Bearer {os.getenv('HH_ACCESS_TOKEN')}"
}


@lru_cache(maxsize=1)
def get_categories():
    try:
        response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles", headers=headers)
        response.raise_for_status()
        data = response.json()
        categories = {}

        for cat_dict in data["categories"]:
            categories[cat_dict['id']] = cat_dict['name']
        return categories
    except requests.exceptions.Timeout:
        raise HTTPException(504, "External service is not responding (timeout)")
    except requests.exceptions.ConnectionError:
        raise HTTPException(503, "The service is temporarily unavailable (connection error)")
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status == 429:
            raise HTTPException(429, "Слишком много запросов, попробуйте позже")
        elif status == 404:
            raise HTTPException(404, "Ресурс не найден")
        else:
            raise HTTPException(502, f"Внешний сервис вернул ошибку {status}")


@lru_cache(maxsize=50)
def get_roles_by_category_id(category_id: str):
    try:
        response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles", headers=headers)
        data = response.json()
        roles = {}

        for cat_dict in data["categories"]:
            if category_id == cat_dict["id"]:
                for role in cat_dict["roles"]:
                    roles[role["id"]] = role["name"]
            else:
                continue

        return roles
    except requests.exceptions.Timeout:
        raise HTTPException(504, "External service is not responding (timeout)")
    except requests.exceptions.ConnectionError:
        raise HTTPException(503, "The service is temporarily unavailable (connection error)")
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status == 429:
            raise HTTPException(429, "Слишком много запросов, попробуйте позже")
        elif status == 404:
            raise HTTPException(404, "Ресурс не найден")
        else:
            raise HTTPException(502, f"Внешний сервис вернул ошибку {status}")
