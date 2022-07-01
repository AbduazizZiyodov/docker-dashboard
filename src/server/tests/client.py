import httpx
import typing as t


class CustomAsyncTestClient:
    API_URL: str = "http://127.0.0.1:2121/api"

    async def send_request(
        self,
        method: str,
        endpoint: str,
        data: t.Optional[dict] = {},
        headers: t.Optional[httpx.Headers] = httpx.Headers({})
    ) -> httpx.Response:

        url: str = f"{self.API_URL}/{endpoint}"

        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client\
                .request(method, url, json=data, headers=headers, timeout=60 * 5)

        return response

    async def get(
        self,
        endpoint: str,
        data: t.Optional[dict] = {},
        headers: t.Optional[httpx.Headers] = httpx.Headers({})
    ) -> httpx.Response:
        return await self.send_request("GET", endpoint, data, headers)

    async def post(
        self,
        endpoint: str,
        data: t.Optional[dict] = {},
        headers: t.Optional[httpx.Headers] = httpx.Headers({})
    ) -> httpx.Response:
        return await self.send_request("POST", endpoint, data, headers)

    async def put(
        self,
        endpoint: str,
        data: t.Optional[dict] = {},
        headers: t.Optional[httpx.Headers] = httpx.Headers({})
    ) -> httpx.Response:
        return await self.send_request("PUT", endpoint, data, headers)

    async def patch(
        self,
        endpoint: str,
        data: t.Optional[dict] = {},
        headers: t.Optional[httpx.Headers] = httpx.Headers({})
    ) -> httpx.Response:
        return await self.send_request("PATCH", endpoint, data, headers)

    async def delete(
        self,
        endpoint: str,
        data: t.Optional[dict] = {},
        headers: t.Optional[httpx.Headers] = httpx.Headers({})
    ) -> httpx.Response:
        return await self.send_request("DELETE", endpoint, data, headers)


__all__ = ["CustomAsyncTestClient", ]
