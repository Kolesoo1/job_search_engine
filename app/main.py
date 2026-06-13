from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request
from pydantic import Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi import _rate_limit_exceeded_handler

from app_requests.main_requests import get_categories, get_roles_by_category_id, search_vacancies, get_areas
from models.params import SearchParams


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.acceptable_parameters = {
        "search parameters":
            {
                "text": "search text",
                "area": "search region",
                "speciality": "specialization in vacancies",
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

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5/minute"]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/all_categories")
@limiter.limit("5/minute")
async def show_all_categories(request: Request):
    return get_categories()


@app.get("/areas")
@limiter.limit("55/minute")
async def show_areas(request: Request):
    return get_areas()


@app.get("/categories/{category_id}/show_roles")
@limiter.limit("5/minute")
async def show_roles(request: Request, category_id: Annotated[str, Field(..., min_length=1, max_length=4,
                                                                         description="Category's id. You can get all categories with id by /all_categories endpoint")]):
    return get_roles_by_category_id(category_id)


@app.get("/parameters")
@limiter.limit("5/minute")
async def show_parameters(request: Request):
    return app.state.acceptable_parameters


@app.post("/search")
@limiter.limit("5/minute")
async def search(request: Request, params: SearchParams):
    return search_vacancies(params)
