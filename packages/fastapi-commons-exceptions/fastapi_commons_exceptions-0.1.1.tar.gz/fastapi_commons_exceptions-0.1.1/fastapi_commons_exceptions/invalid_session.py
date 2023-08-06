from fastapi import HTTPException, status


class InvalidSession(HTTPException):
    def __init__(
            self,
            detail: any = "Invalid Session or Expire",
            headers: dict[str, any] | None = None,
    ):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        self.headers = headers
