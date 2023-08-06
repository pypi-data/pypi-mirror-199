from fastapi import HTTPException, status


class AuthenticationFailed(HTTPException):
    def __init__(
        self,
        detail: any = "Incorrect Authentication Credentials",
        headers: dict[str, any] | None = None,
    ):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        self.headers = headers
