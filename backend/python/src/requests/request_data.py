class RequestData:
    def __init__(self, method, params, headers=None, body=None) -> None:
        self.method = method
        self.headers = headers or {}
        self.params = params or {}
        self.body = body
