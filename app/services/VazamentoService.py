from typing import Optional
import httpx
import os
from fastapi import HTTPException
from datetime import datetime
from dotenv import load_dotenv
from app.models.vazamentos import models, schemas
from sqlalchemy.orm import Session
from app.services import UsuarioService
from app.services.EmailService import enviar_email

load_dotenv()
HIBP_API_KEY = os.getenv("HIBP_API_KEY")

if not HIBP_API_KEY:
    raise RuntimeError("Chave de API não configurada corretamente!")


def obter_vazamento_por_id(db: Session, vazamentoId: int):
    vazamento = db.query(models.Vazamento).filter(vazamentoId == models.Vazamento.id).first()
    if not vazamento:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return vazamento


HEADERS = {
    "HIBP-API-Key": HIBP_API_KEY,
    "User-Agent": "Osint Cyber",
}

API_URL_TEMPLATE = "https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"


async def obter_vazamentos_pelo_email_usuario(db: Session, email: str) -> list[schemas.VazamentoResponse]:
    """
    Obtém vazamentos de segurança associados a um e-mail.
    Busca localmente no banco ou externamente na API Have I Been Pwned.
    """

    usuario = UsuarioService.obter_usuario_pelo_email(db, email)
    vazamentos_locais = buscar_vazamentos_no_banco(db, usuario.id)
    if vazamentos_locais:
        return vazamentos_locais


    resultados_api = await buscar_vazamentos_na_api(email)


    if resultados_api:
        for vazamento_data in resultados_api:
            criar_vazamento_no_banco_de_dados(db, processar_vazamento(vazamento_data), usuario.id)


    return buscar_vazamentos_no_banco(db, usuario.id)



def buscar_vazamentos_no_banco(db: Session, usuario_id: int) -> list[schemas.VazamentoResponse]:
    """Busca vazamentos associados a um usuário no banco de dados."""
    return db.query(models.Vazamento).filter(models.Vazamento.usuario_id == usuario_id).all()


async def buscar_vazamentos_na_api(email: str) -> Optional[list[dict]]:
    """
    Faz uma requisição à API Have I Been Pwned para buscar vazamentos por e-mail.
    Lança exceções personalizadas para erros conhecidos.
    """
    url = API_URL_TEMPLATE.format(email=email)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    try:
        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Nenhum vazamento foi encontrado para este e-mail.")
        else:

            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Erro na requisição para a API externa: {e.response.text}",
            )
    except httpx.RequestError as e:

        raise HTTPException(status_code=500, detail=f"Erro ao conectar à API externa: {str(e)}")
    except ValueError:

        raise HTTPException(status_code=500, detail="Erro ao processar a resposta da API externa. Não é um JSON válido.")


def processar_vazamento(vazamento_data: dict) -> dict:
    """
    Processa os dados de um vazamento para o formato do banco de dados.
    Faz conversões de data e atribuições de valores padrão.
    """
    return {
        "nome": vazamento_data.get("Name"),
        "titulo": vazamento_data.get("Title", ""),
        "dominio_url": vazamento_data.get("Domain", ""),
        "data_vazamento": datetime.strptime(vazamento_data.get("BreachDate", ""), "%Y-%m-%d").date()
        if vazamento_data.get("BreachDate")
        else None,
        "data_atualizacao": datetime.strptime(vazamento_data.get("ModifiedDate", ""), "%Y-%m-%dT%H:%M:%SZ")
        if vazamento_data.get("ModifiedDate")
        else None,
        "descricao": vazamento_data.get("Description", None),
        "image_uri": vazamento_data.get("LogoPath", None),
    }


def criar_vazamento_no_banco_de_dados(db: Session, vazamento_dados: dict, usuario_id: int):
    """
    Salva um vazamento no banco de dados associado a um usuário.
    """
    novo_vazamento = models.Vazamento(
        nome=vazamento_dados["nome"],
        titulo=vazamento_dados["titulo"],
        dominio_url=vazamento_dados["dominio_url"],
        data_vazamento=vazamento_dados["data_vazamento"],
        data_atualizacao=vazamento_dados["data_atualizacao"],
        descricao=vazamento_dados.get("descricao", ""),
        image_uri=vazamento_dados.get("image_uri", ""),
        usuario_id=usuario_id,
    )
    db.add(novo_vazamento)
    db.commit()
    db.refresh(novo_vazamento)
    return novo_vazamento

def get_all_vazamentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vazamento).offset(skip).limit(limit).all()

async def notificar_vazamento_usuario_por_email_demonstrativo(email_usuario: str, titulo_vazamento: str, data: str, descricao: str) :
    mensagem = (
        f"Olá,\n\n"
        f"Um novo vazamento foi identificado relacionado ao seu e-mail:\n\n"
        f"**Título:** {titulo_vazamento}\n"
        f"**Data:** {data}\n"
        f"**Descrição:** {descricao}\n\n"
        f"Recomendamos que altere suas senhas imediatamente e esteja atento a possíveis fraudes.\n\n"
        f"Atenciosamente,\n"
        f"Equipe de Segurança Start Cyber 2"
    )
    assunto = f"Novo vazamento detectado: {titulo_vazamento}"
    await enviar_email(email_usuario, assunto, mensagem)








