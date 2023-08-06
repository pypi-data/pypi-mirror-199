import pytest

from richillcapital_http import HttpClient, HttpMethod, HttpRequest


@pytest.fixture
def http_client():
    return HttpClient("http://localhost:3001")


@pytest.fixture
def ping_request():
    return HttpRequest(method=HttpMethod.GET, endpoint="/api/v1/ping")


@pytest.mark.asyncio
async def test_ping(http_client: HttpClient, ping_request: HttpRequest):
    response = await http_client.send_async(ping_request)
    assert response.status_code == 200
