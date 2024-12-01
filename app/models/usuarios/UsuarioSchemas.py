from typing import Optional

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    nome: str
    email: str
    senha: str


class UsuarioReponse(BaseModel):
    id: int
    nome: str
    email: str
    notificacoes_ativadas: bool


    class Config:
        orm_mode = True



class UpdateUserRequest(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    notificacoes_ativadas: Optional[bool] = None




