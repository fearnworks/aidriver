import httpx
from loguru import logger


class AuthService:
    def __init__(self):
        self.client = httpx.Client()  # Create a client instance
        self._access_token = None

    async def login(self, email: str, password: str):
        form_data = {"username": email, "password": password, "grant_type": "password"}
        response = self.client.post(
            "http://ai_driver:28001/api/v1/auth/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=form_data,
        )
        token_data = response.json()
        logger.info(token_data)
        self._access_token = token_data["access_token"]
        return token_data

    async def get_current_user(self):
        headers = {"Authorization": f"Bearer {self._access_token}"}
        response = self.client.get(
            "http://ai_driver:28001/api/v1/auth/me", headers=headers
        )
        return response.json()

    def add_auth_headers(self, client):
        # Retrieve the token from the auth_service (assuming a get_token method exists)
        token = self._access_token
        # Add the token to the client's default headers
        client.headers.update({"Authorization": f"Bearer {token}"})
        return client


auth_service = AuthService()
