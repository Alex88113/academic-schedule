import asyncio
import httpx

class HTTPSettings:
    def get_client(self) -> httpx.AsyncClient:
        timeout = httpx.Timeout(
            connect=10.0,
            read=30.0,
            write=10.0,
            pool=5
        )

        limits = httpx.Limits(
            max_keepalive_connections=5,
            max_connections=10,
            keepalive_expiry=5.0
        )
        return httpx.AsyncClient(timeout=timeout, limits=limits)

def get_connect_settings():
    obj_settings = HTTPSettings()
    result = obj_settings.get_client()
    return result
