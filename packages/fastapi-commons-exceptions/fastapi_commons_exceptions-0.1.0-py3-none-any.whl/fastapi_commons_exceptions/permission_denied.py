from fastapi import HTTPException, status


class PermissionDenied(HTTPException):
    def __init__(
        self,
        detail: any = "You Do Not Have Permission To Perform This Action",
        headers: dict[str, any] | None = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
        self.headers = headers
