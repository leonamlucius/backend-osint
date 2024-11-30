from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class VazamentoBase(BaseModel):
    nome: str
    titulo: str
    dominio_url: str
    data_vazamento: Optional[date]
    data_atualizacao: Optional[datetime]
    descricao: Optional[str] = None
    image_uri: Optional[str] = None

class VazamentoCreate(BaseModel):
    nome: str
    titulo: str
    dominio_url: str
    data_vazamento: Optional[date]
    data_atualizacao: Optional[datetime]
    descricao: Optional[str] = None
    image_uri: Optional[str] = None
    usuario_id: int


class VazamentoResponse(BaseModel):
    id: int
    nome: str
    titulo: str
    dominio_url: str
    data_vazamento: Optional[date]
    data_atualizacao: Optional[datetime]
    descricao: Optional[str] = None
    image_uri: Optional[str] = None
    usuario_id: int

    class Config:
        orm_mode = True
