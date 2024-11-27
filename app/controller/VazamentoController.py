from fastapi import APIRouter, HTTPException, Depends
from app.service import VazamentoService
from app.models import models
from app.models import schemas
from app.db.database import SessionLocal, engine
from sqlalchemy.orm import Session

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



@router.get(endpointVazamento + "procurar/{email}", response_model= schemas.VazamentoReponse )
def obter_vazamentos_por_email(email: str, db: Session= Depends(get_db())):

    vazamentoEncontrado = VazamentoService.get_vazamento_by_email(email, db)

    if vazamentoEncontrado is None:
        raise HTTPException(status_code = 404, detail= "Vazamentos não encontrados")


    return vazamentoEncontrado


