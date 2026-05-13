from pydantic import BaseModel


class FindEmailData(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    domain: str | None = None


class FindEmailResponse(BaseModel):
    data: FindEmailData  # noqa: WPS110


class VerifyEmailData(BaseModel):
    status: str


class VerifyEmailResponse(BaseModel):
    data: VerifyEmailData  # noqa: WPS110


class VerifiedEmailRecord(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    domain: str | None = None
    status: str
