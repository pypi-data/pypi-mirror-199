from typing import Optional

from aiohttp import ClientSession

from richillcapital_http.enums import HttpMethod


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
        self._headers = headers or {}
        self.body = body or {}

    def add_header(self, key: str, value: str) -> "HttpRequest":
        """ """
        self._headers[key] = value
        return self


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
            async with session.request(
                request.method,
                self._base_address + request.endpoint,
                headers=request._headers,
                data=request.body,
            ) as response:
                return HttpResponse(
                    status_code=response.status,
                    headers=dict(response.headers),
                    content=await response.read(),
                )
