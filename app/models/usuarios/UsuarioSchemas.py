from pydantic import BaseModel


class UsuarioRequest(BaseModel):
    nome: str


class UsuarioReponse(BaseModel):
    id: int
    nome: str
