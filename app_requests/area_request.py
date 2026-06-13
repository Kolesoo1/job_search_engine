import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('HH_ACCESS_TOKEN')}",
    "User-Agent": os.getenv('HH_USER_AGENT')
}

categories_response = requests.get(f"{os.getenv('HH_BASE_URL')}/areas", headers=headers)

print(categories_response.json())


# Информационные технологии: id = 11