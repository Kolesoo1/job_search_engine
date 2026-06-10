import json

from fastapi import FastAPI

app = FastAPI(
    title="JobSearchEngine",
    description="API that will help you with job search on HeadHunter",
    version="1.0.0"
)

with open("../requests/roles.json", "r", encoding="UTF-8") as file:
    data: dict[str, str] = json.load(file)

for idr, role in data.items():
    print(f"id: {idr}, role: {role}")
