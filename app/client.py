import httpx

_client: httpx.AsyncClient | None = None

def set_client(client: httpx.AsyncClient):
    global _client
    _client = client

def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("Client not initialized")
    return _client