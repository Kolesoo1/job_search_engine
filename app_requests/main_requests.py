import os

from anyio.functools import lru_cache
from dotenv import load_dotenv

import requests

from handlers.hh_handler import handle_hh_errors
from models.params import SearchParams

load_dotenv()

headers = {
    "User-Agent": os.getenv('HH_USER_AGENT'),
    "Authorization": f"Bearer {os.getenv('HH_ACCESS_TOKEN')}"
}


@lru_cache(maxsize=1)
@handle_hh_errors
def get_areas():
    response = requests.get(f"{os.getenv('HH_BASE_URL')}/areas", headers=headers)
    response.raise_for_status()
    data = response.json()
    res_areas = {}

    for area_country_level in data:
        res_area = {"name": area_country_level["name"]}
        areas = area_country_level["areas"]
        regions = {region["id"]: region["name"] for region in areas}
        res_area["regions"] = regions
        res_areas[area_country_level["id"]] = res_area

    return res_areas


@lru_cache(maxsize=1)
@handle_hh_errors
def get_categories():
    response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles", headers=headers)
    response.raise_for_status()
    data = response.json()
    return {cat_dict['id']: cat_dict['name'] for cat_dict in data["categories"]}


@lru_cache(maxsize=50)
@handle_hh_errors
def get_roles_by_category_id(category_id: str):
    response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles", headers=headers)
    response.raise_for_status()
    data = response.json()
    roles = {}

    for cat_dict in data["categories"]:
        if category_id == cat_dict["id"]:
            for role in cat_dict["roles"]:
                roles[role["id"]] = role["name"]
            break

    return roles


@handle_hh_errors
def search_vacancies(params: SearchParams):
    response = requests.get(
        f"{os.getenv('HH_BASE_URL')}/vacancies",
        params=params.model_dump(),
        headers=headers
    )
    response.raise_for_status()
    return response.json()
