from enum import Enum
from typing import Optional

from aiohttp import ClientSession


class HttpMethod(str, Enum):
    """ """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HttpRequest:
    """ """

    def __init__(
        self,
        method: HttpMethod,
        endpoint: str,
        headers: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> None:
        self.method = method
        self.endpoint = endpoint
        self.headers = headers or {}
        self.body = body or {}


class ResponseContent:
    """ """

    def __init__(self, content: bytes) -> None:
        self.__content = content

    async def read_as_string_async(self) -> str:
        """ """
        return self.__content.decode("utf-8")


class HttpResponse:
    def __init__(self, status_code: int, headers: dict, content: bytes):
        self.status_code = status_code
        self.headers = headers
        self.content = ResponseContent(content)


class HttpClient:
    """ """

    def __init__(self, base_address: str) -> None:
        """ """
        self._base_address = base_address

    async def send_async(self, request: HttpRequest) -> HttpResponse:
        """ """
        async with ClientSession() as session:
            url = self._base_address + request.endpoint

            async with session.request(
                request.method, url, headers=request.headers, json=request.body
            ) as response:
                response_body = await response.read()
                return HttpResponse(
                    status_code=response.status,
                    headers=dict(response.headers),
                    content=response_body,
                )
