from reach_python.http_client.async_http_client import AsyncHTTPClient
from reach_python.http_client.creator import HTTPClient
from reach_python.http_client.sync_http_client import SyncHTTPClient


class HTTPClientFactory:
    def build(self, client_type) -> HTTPClient:
        if client_type == "async":
            return AsyncHTTPClient()
        elif client_type == "sync":
            return SyncHTTPClient()
        raise NotImplementedError(f"Client Type {client_type} is not implemented")
