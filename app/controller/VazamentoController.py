from fastapi import APIRouter, HTTPException, Depends
from app.services import VazamentoService
from app.models.vazamentos import models, schemas
from app.db.database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List

from app.services.VazamentoService import notificar_vazamento_usuario_por_email_demonstrativo

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
    vazamentoEncontrado = await VazamentoService.obter_vazamentos_pelo_email_usuario(db, email)
    return vazamentoEncontrado



@router.get(endpointVazamento + "exporvazamentos/", response_model=List[schemas.VazamentoResponse])
def expor_vazamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint para buscar todos os vazamentos de e-mails, com paginação.
    """
    vazamentos = VazamentoService.get_all_vazamentos(db, skip, limit) # Função do serviço para pegar os vazamentos

    if not vazamentos: # Verificando se foram encontrados vazamentos
        raise HTTPException(status_code=404, detail="Nenhum vazamento encontrado")

    return vazamentos


@router.post(endpointVazamento + "notificar-vazamento-demonstrativo")
async def notificar_vazamento_demonstrativo(notificacao: schemas.NotificacaoRequest):
    """
    Endpoint para notificar um usuário sobre um vazamento por e-mail.
    """
    try:
        await notificar_vazamento_usuario_por_email_demonstrativo(
            email_usuario=notificacao.email_usuario,
            titulo_vazamento=notificacao.titulo_vazamento,
            data=notificacao.data,
            descricao=notificacao.descricao
        )
        return {"message": "E-mail enviado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mail: {str(e)}")








