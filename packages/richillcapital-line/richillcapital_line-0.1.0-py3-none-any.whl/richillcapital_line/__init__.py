import json

from richillcapital_http import HttpMethod, HttpClient, HttpRequest


class LineNotifyException(Exception):
    """Exception raised when there is an error in LINE Notify API response."""

    def __init__(self, status: int, message: str):
        super().__init__(f"LineNotify API returned error {status}: {message}")
        self.status = status
        self.message = message


class LineNotifyClient:
    """
    A client for the LINE Notify API.

    Args:
        access_token: The LINE Notify API access token.
    """

    BASE_ADDRESS = "https://notify-api.line.me"

    def __init__(self, access_token: str) -> None:
        self.__access_token = access_token or ""
        self.__http_client = HttpClient(self.BASE_ADDRESS)

    async def send_notification_async(self, message: str) -> dict:
        """
        Send a notification message to LINE Notify API.

        Args:
            message: The message to be sent.

        Returns:
            A dictionary containing the response from the API.

        Raises:
            LineNotifyException: If the request fails with non-200 HTTP status code.
        """
        request = HttpRequest(
            HttpMethod.POST,
            "/api/notify",
            headers={
                "Authorization": f"Bearer {self.__access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body={"message": message},
        )
        response = await self.__http_client.send_async(request)
        content = await response.content.read_as_string_async()
        response_json: dict[str, str] = json.loads(content)

        if response.status_code != 200:
            raise LineNotifyException(
                response.status_code, response_json.get("message", "")
            )

        return response_json

    async def get_status_async(self) -> dict:
        """
        Get the status of the LINE Notify API.

        Returns:
            A dictionary containing the response from the API.
        """
        request = HttpRequest(
            HttpMethod.GET,
            "/api/status",
            headers={
                "Authorization": f"Bearer {self.__access_token}",
            },
        )
        response = await self.__http_client.send_async(request)
        content = await response.content.read_as_string_async()
        return json.loads(content)
