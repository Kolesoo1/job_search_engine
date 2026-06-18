import os

from async_lru import alru_cache
from dotenv import load_dotenv

from app.client import get_client
from handlers.hh_handler import handle_hh_errors
from models.params import SearchParams

load_dotenv()

headers = {
    "User-Agent": os.getenv('HH_USER_AGENT'),
    "Authorization": f"Bearer {os.getenv('HH_ACCESS_TOKEN')}"
}


@alru_cache(maxsize=1)
@handle_hh_errors
async def get_areas():
    client = get_client()
    response = await client.get(f"{os.getenv('HH_BASE_URL')}/areas", headers=headers)
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


@alru_cache(maxsize=1)
@handle_hh_errors
async def get_categories():
    client = get_client()
    response = await client.get(f"{os.getenv('HH_BASE_URL')}/professional_roles", headers=headers)
    response.raise_for_status()
    data = response.json()
    return {cat_dict['id']: cat_dict['name'] for cat_dict in data["categories"]}


@alru_cache(maxsize=50)
@handle_hh_errors
async def get_roles_by_category_id(category_id: str):
    client = get_client()
    response = await client.get(f"{os.getenv('HH_BASE_URL')}/professional_roles", headers=headers)
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
async def search_vacancies(params: SearchParams):
    client = get_client()
    response = await client.get(
        f"{os.getenv('HH_BASE_URL')}/vacancies",
        params=params.model_dump(),
        headers=headers
    )
    response.raise_for_status()
    return response.json()
