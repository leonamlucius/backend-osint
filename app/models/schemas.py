from pydantic import BaseModel


class VazamentoRequest(BaseModel):
    email: str


class VazamentoReponse(BaseModel):
    id: int
    email: str