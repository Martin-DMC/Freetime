import httpx
from utils.http_client_factory import get_async_github_client
from persistence.memory_storage import memoryStorage

API_BASE_URL = "http://127.0.0.1:8000"

async def fetch_user_data(username: str) -> dict:
    """
    get the user data of our local api
    """
    try:
        async with get_async_github_client() as client:
            resp = await client.get(f"{API_BASE_URL}/graphql-user/{username}")
            resp.raise_for_status() # throws an exception for errors 4xx 5xx
            return resp.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print(f"Usuario no encontrado: {username}")
            return None
        raise # Rethrow any other errors

async def update_user_stats(usernames: list, storage: memoryStorage):
    """
    It loops through the users, gets their data and updates it if it is not the same.
    """
    for username in usernames:
        new_data = await fetch_user_data(username)
        if new_data is None:
            continue

        old_data = storage.get_user_data(username)

        if old_data != new_data:
            storage.save_user_data(username, new_data)