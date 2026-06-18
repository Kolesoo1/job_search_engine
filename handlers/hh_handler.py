from functools import wraps
import requests
from fastapi import HTTPException


def handle_hh_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
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

    return wrapper
