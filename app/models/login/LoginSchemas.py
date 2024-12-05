from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    senha: str



