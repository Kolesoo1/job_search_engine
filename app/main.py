from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI
from pydantic import Field

from app_requests.main_requests import get_categories, get_roles_by_category_id


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.acceptable_parameters = {
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
    yield
    app.state.acceptable_parameters = None


app = FastAPI(
    title="JobSearchEngine",
    description="API that will help you with job search on HeadHunter",
    version="1.0.0"
)


@app.get("/all_categories")
def show_all_categories():
    return get_categories()


@app.get("/categories/{category_id}/show_roles")
def show_roles(category_id: Annotated[str | None, Field(..., min_length=1, max_length=4, alias="11")]):
    return get_roles_by_category_id(category_id)


@app.get("/parameters")
def show_parameters():
    return app.state.acceptable_parameters


@app.get("/search")
def search():
    pass
