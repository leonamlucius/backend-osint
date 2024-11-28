from fastapi import APIRouter, HTTPException, Depends
from app.service import VazamentoService
from app.models.vazamentos import models, schemas
from app.db.database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind= engine)
router = APIRouter()

endpointVazamento = "/vazamentos/"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(endpointVazamento)
def getHello():
    return "Hello, word"



@router.get(endpointVazamento + "procurar/{email}", response_model= schemas.VazamentoReponse)
def obter_vazamentos_por_email(email: str, db: Session= Depends(get_db)):

    vazamentoEncontrado = VazamentoService.get_vazamento_by_email(email, db)

    if vazamentoEncontrado is None:
        raise HTTPException(status_code = 404, detail= "Vazamentos não encontrados")


    return vazamentoEncontrado


@router.post(endpointVazamento, response_model = schemas.VazamentoReponse)
def criar_vazamentos(vazamentos: schemas.VazamentoRequest, db: Session= Depends(get_db)):

    vazamento= VazamentoService.create_vazamento(vazamentos, db)


    return  vazamento


@router.get(endpointVazamento + "exporvazamentos/", response_model=List[schemas.VazamentoReponse])
def expor_vazamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint para buscar todos os vazamentos de e-mails, com paginação.
    """
    vazamentos = VazamentoService.get_all_vazamentos(db, skip, limit) # Função do serviço para pegar os vazamentos

    if not vazamentos: # Verificando se foram encontrados vazamentos
        raise HTTPException(status_code=404, detail="Nenhum vazamento encontrado")

    return vazamentos








