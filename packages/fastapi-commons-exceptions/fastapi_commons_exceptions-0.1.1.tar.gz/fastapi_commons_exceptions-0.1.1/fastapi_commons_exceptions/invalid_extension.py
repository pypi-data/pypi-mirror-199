from fastapi import HTTPException, status

class InvalidExtension(HTTPException):
    def __init__(
            self,
            detail: any = '"The file extension is not accepted"',
            headers: dict[str, any] | None = None,
    ):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        self.headers = headers