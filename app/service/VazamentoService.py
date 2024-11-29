import httpx
from fastapi import HTTPException

from app.models.vazamentos import models, schemas
from sqlalchemy.orm import Session

from app.service import UsuarioService


def obter_vazamento_por_id(db: Session, vazamentoId: int):
    vazamento = db.query(models.Vazamento).filter(vazamentoId == models.Vazamento.id).first()
    if not vazamento:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return vazamento


async def obter_vazamentos_pelo_email_usuario(db: Session, email: str) -> list[schemas.VazamentoResponse]:

    usuario = UsuarioService.obter_usuario_pelo_email(db, email)

    vazamentos_locais = db.query(models.Vazamento).filter(models.Vazamento.usuario_id == usuario.id).all()

    if vazamentos_locais:
        return vazamentos_locais

    try:
        response = await httpx.AsyncClient().get("https://api.externa.com/vazamentos", params={"email": email})
        response.raise_for_status()

        resultados_api = response.json()
        for vazamento_data in resultados_api:
            criar_vazamento_no_banco_de_dados(db, vazamento_data, usuario.id)


        vazamentos_locais = db.query(models.Vazamento).filter(models.Vazamento.usuario_id == usuario.id).all()
        return vazamentos_locais

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar à API externa: {str(e)}")


def get_all_vazamentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vazamento).offset(skip).limit(limit).all()


def criar_vazamento_no_banco_de_dados(db: Session, vazamento_dados: dict, usuario_id: int):
    novo_vazamento = models.Vazamento(
        nome=vazamento_dados['nome'],
        titulo=vazamento_dados['titulo'],
        dominio_url=vazamento_dados['dominio_url'],
        data_vazamento=vazamento_dados['data_vazamento'],
        data_atualizacao=vazamento_dados['data_atualizacao'],
        descricao=vazamento_dados.get('descricao', ''),
        image_uri=vazamento_dados.get('image_uri', ''),
        usuario_id=usuario_id
    )
    db.add(novo_vazamento)
    db.commit()
    db.refresh(novo_vazamento)
    return novo_vazamento
