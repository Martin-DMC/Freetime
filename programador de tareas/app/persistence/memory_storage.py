class memoryStorage():
    """
    This class stores the user data from the last update
    """
    def __init__(self):
        # the key is username
        self._storage = {}

    def get_user_data(self, username: str) -> dict:
        """
        get data of specific user.
        return a empty dict if user not found
        """
        return self._storage.get(username, {})

    def save_user_data(self, username: str, data: dict):
        """
        save or upload user data
        """
        self._storage[username] = data
