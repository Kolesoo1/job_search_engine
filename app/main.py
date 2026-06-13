import io
from contextlib import asynccontextmanager
from typing import Annotated, cast

from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Request, HTTPException, status
from pydantic import Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi import _rate_limit_exceeded_handler
import pandas as pd

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
    roles = get_roles_by_category_id(category_id)
    if not roles:
        raise HTTPException(status_code=404, detail="Category not found")
    return roles


@app.get("/parameters")
@limiter.limit("5/minute")
async def show_parameters(request: Request):
    return app.state.acceptable_parameters


@app.post("/search")
@limiter.limit("5/minute")
async def search(request: Request, params: SearchParams):
    data = search_vacancies(params)
    df = pd.DataFrame(
        columns=["name", "salaries_from", "salaries_to", "salaries_frequency", "url", "employer",
                 "employer_url",
                 "requirement",
                 "responsibility", "work_format"])
    names = []
    salaries_from = []
    salaries_to = []
    salaries_frequency = []
    urls = []
    employers = []
    employer_urls = []
    requirements = []
    responsibilities = []
    work_formats = []

    for vacancy in data["items"]:
        name = vacancy["name"]

        salary = vacancy.get("salary")
        if salary and salary.get("from") is not None:
            salary_from = salary["from"]
        else:
            salary_from = None

        if salary and salary.get("to") is not None:
            salary_to = salary["to"]
        else:
            salary_to = None

        if salary and salary.get("frequency") and salary["frequency"].get("name"):
            salary_frequency = salary["frequency"]["name"]
        else:
            salary_frequency = None

        url = vacancy["alternate_url"]

        employer = vacancy["employer"]
        employer_name = employer["name"]
        employer_url = employer["alternate_url"]

        requirement = vacancy["snippet"].get("requirement", "")
        responsibility = vacancy["snippet"].get("responsibility", "")

        work_format = ""
        if "work_formats" in vacancy and vacancy["work_formats"]:
            for formats in vacancy["work_formats"]:
                work_format += f"/{formats['name']}"
            work_format = work_format.lstrip('/')

        names.append(name)
        salaries_from.append(salary_from)
        salaries_to.append(salary_to)
        salaries_frequency.append(salary_frequency)
        urls.append(url)
        employers.append(employer_name)
        employer_urls.append(employer_url)
        requirements.append(requirement)
        responsibilities.append(responsibility)
        work_formats.append(work_format)

    df["name"] = names
    df["salaries_from"] = salaries_from
    df["salaries_to"] = salaries_to
    df["salaries_frequency"] = salaries_frequency
    df["url"] = urls
    df["employer"] = employers
    df["employer_url"] = employer_urls
    df["requirement"] = requirements
    df["responsibility"] = responsibilities
    df["work_format"] = work_formats

    buffer = io.BytesIO()

    df.to_excel(buffer, engine="openpyxl", index=False)

    buffer.seek(0)

    headers = {
        "Content-Disposition": 'attachment; filename="processed_data.xlsx"'
    }

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )
