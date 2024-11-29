from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    nome: str
    email: str
    senha: str


class UsuarioReponse(BaseModel):
    id: int
    nome: str
    email: str
