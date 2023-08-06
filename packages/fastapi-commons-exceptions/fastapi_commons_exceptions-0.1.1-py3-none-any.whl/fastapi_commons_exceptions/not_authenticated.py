from fastapi import HTTPException, status


class NotAuthenticated(HTTPException):
    def __init__(
            self,
            detail: any = "Authentication credentials were not provided",
            headers: dict[str, any] | None = None,
    ):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        self.headers = headers
