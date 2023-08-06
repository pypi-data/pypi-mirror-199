from reach_python.http_client.creator import HTTPClient


class SyncHTTPClient(HTTPClient):
    # HTTP Client based on requests library for synchronous requests
    def __init__(self):
        import requests
        self._session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, *err):
        self._session.close()
        self._session = None

    def get(self, url, params=None):
        return self._session.get(url, params=params).json()

    def post(self, url, data=None):
        return self._session.post(url, json=data).json()

    def put(self, url, data=None):
        return self._session.put(url, json=data).json()

    def delete(self, url):
        return self._session.delete(url).json()
