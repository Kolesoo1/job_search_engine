import json
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

acceptable_parameters = {
    "search parameters":
        {
            "text": "search text",
            "area": "search region",
            "specialization": "specialization in vacancies",
            "experience": "required work experience"
        },
    "pagination parameters": {
        "pages": "the number of pages in the response",
        "per_pages": "number of vacancies per page",
        "page": "number of the loaded page (indexing from 0)"
    }
}

app = FastAPI(
    title="JobSearchEngine",
    description="API that will help you with job search on HeadHunter",
    version="1.0.0"
)


@app.get("/all_categories")
def show_all_categories():
    response = requests.get(f"{os.getenv('HH_BASE_URL')}/professional_roles")
    data = response.json()
    categories = {}

    for cat_dict in data["categories"]:
        categories[cat_dict['id']] = cat_dict['name']

    return categories


@app.get("/categories/{category_id}/show_roles")
def show_roles(category_id: str = "11"):
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


@app.get("/parameters")
def show_parameters():
    return acceptable_parameters
