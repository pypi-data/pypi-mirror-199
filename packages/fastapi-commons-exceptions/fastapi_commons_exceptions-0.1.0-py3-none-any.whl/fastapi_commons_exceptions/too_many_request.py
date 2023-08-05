from fastapi import HTTPException, status


class TooManyRequest(HTTPException):
    def __init__(
        self,
        detail: any = "You have exceeded the number of requests allowed",
        headers: dict[str, any] | None = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)
        self.headers = headers
