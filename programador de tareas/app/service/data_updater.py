from dotenv import load_dotenv
from persistence.memory_storage import memoryStorage
from service.github_client import update_user_stats

LIST_USERS = ['Martin-DMC', 'glovek08', 'federico-paganini']

async def run_updates():
    """
    function that connect everything
    """
    load_dotenv()

    user_storage = memoryStorage()

    await update_user_stats(usernames=LIST_USERS, storage=user_storage)
    
    for username, user_data in user_storage._storage.items():
        print(f"Usuario: {username}")
        print(f"Datos: {user_data}")
        print("-" * 20)