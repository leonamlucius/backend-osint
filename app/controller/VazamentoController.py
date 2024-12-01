from fastapi import APIRouter, HTTPException, Depends
from app.services import VazamentoService
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


@router.get(endpointVazamento + "procurar/{email}", response_model=List[schemas.VazamentoResponse])
async def obter_vazamentos_do_usuario_por_email(email: str, db: Session = Depends(get_db)):
    """
    Busca e retorna todos os vazamentos associados ao e-mail fornecido.
    """
    vazamentoEncontrado = await VazamentoService.obter_vazamentos_pelo_email_usuario(db, email)
    return vazamentoEncontrado



@router.get(endpointVazamento + "exporvazamentos/", response_model=List[schemas.VazamentoResponse])
def expor_vazamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os vazamentos registrados no banco de dados com suporte a paginação.
    """
    vazamentos = VazamentoService.get_all_vazamentos(db, skip, limit) # Função do serviço para pegar os vazamentos

    if not vazamentos: # Verificando se foram encontrados vazamentos
        raise HTTPException(status_code=404, detail="Nenhum vazamento encontrado")

    return vazamentos








