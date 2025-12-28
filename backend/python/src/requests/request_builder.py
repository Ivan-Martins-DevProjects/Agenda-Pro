class RequestBuilder:
    @staticmethod
    def from_flask(request):
        from .request_data import RequestData
        return RequestData(
            method=request.method,
            params=request.args.to_dict(),
            headers=dict(request.headers),
            body=request.get_json(silent=True)
        )
