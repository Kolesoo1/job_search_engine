import os

import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('HH_ACCESS_TOKEN')}",
    "User-Agent": os.getenv('HH_USER_AGENT')
}

params = {
    "per_page": 1,
    "page": 0,
    # "text": "",  # ищется в полях вакансии,
    # "experience": "",  # опыт работы
    # "area": ""
}

response = requests.get(f"{os.getenv('HH_BASE_URL')}/vacancies", headers=headers, params=params)

vacancies = response.json()["items"]

# for vacancy in

print(response.json()["items"])
print(len(response.json()["items"]))
print(response.json()["found"])
print(response.json()["pages"])

