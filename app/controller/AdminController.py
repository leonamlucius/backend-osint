from fastapi import APIRouter, HTTPException, Depends, status

from app.controller.UsuarioController import atualizar_usuario
from app.db.database import SessionLocal, engine
from app.models.autenticacao.login_schemas import ErrorResponse
from app.models.usuarios import UsuarioModel, UsuarioSchemas
from app.services import UsuarioService
from app.db.database import SessionLocal, engine
from sqlalchemy.orm import Session
from app.services import AdminService
from app.services import EmailService

UsuarioModel.Base.metadata.create_all(bind= engine)
routerAdmin = APIRouter()



endpointAdmin = "/admin"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routerAdmin.get(
    endpointAdmin + "{usuarioId}",
     response_model = UsuarioSchemas.UsuarioReponse,
    summary="Obter usuário por ID",
    description=(
            "Este endpoint permite buscar um usuário pelo seu ID. "
            "O ID deve ser um UUID válido."
    ),
    tags=["Usuários"],
    responses={
        404: {
            "description": "Usuário não encontrado.",
            "model": ErrorResponse,
        },
        422: {
            "description": "Erro de validação nos parâmetros.",
            "model": ErrorResponse,
        },
        200: {
            "description": "Usuário obtido.",
            "model": ErrorResponse,
        },

    }


)
def obter_usuario_por_id_admin(usuarioId: int, db: Session = Depends(get_db)):
    usuarioEncontrado = UsuarioService.obter_usuario_pelo_id(db, usuarioId)

    return usuarioEncontrado

@routerAdmin.delete(endpointAdmin + "deletar/{id}",
description=(
        "Este endpoint permite apagar pelo seu respectivo id "
    ),
    tags=["Usuários"],
    responses={
        200: {
            "description": "Usuário apagado com sucesso.",
            "model": ErrorResponse,
        },

        404: {
            "description": "Usuário não encontrado.",
            "model": ErrorResponse,
        },
        422: {
            "description": "Erro de validação de parâmetro.",
            "model": ErrorResponse,
        },
    }
)
def deletar_usuario_por_id_admin(id: int,  db: Session = Depends(get_db)):

    usuarioApagado = AdminService.deletar_usuario_por_id(id, db)

    return usuarioApagado

@routerAdmin.post(endpointAdmin,
    response_model = UsuarioSchemas.UsuarioReponse,
    status_code=status.HTTP_201_CREATED,
    summary = "Criar um novo usuário",
    description = (
        "Este endpoint permite criar um novo usuário no sistema. "
        "Os dados obrigatórios incluem nome, e-mail e senha."
    ),
    tags = ["Usuários"],
    responses = {
        400: {
            "description": "Erro de validação dos dados enviados.",
            "model": ErrorResponse,
        },
        422: {
            "description": "Erro de validação nos parâmetros.",
            "model": ErrorResponse,
        },
    }

)
def criar_usuario_admin(usuario: UsuarioSchemas.CreateUserRequest,  db: Session= Depends(get_db)):

    usuarioAdmin = UsuarioService.criar_usuario(db, usuario)

    return usuarioAdmin

@routerAdmin.post(endpointAdmin + '/email',
    summary = "Envia um email ",
    description = (
        "Este endpoint permite enviar um email por meio deloe."
        "Os dados obrigatórios incluem destinatário, assunto e mensagem."
    ),
    tags = ["Email"],
    responses = {
        500: {
            "description": "Erro ao enviar o e-mail.",
            "model": ErrorResponse,
        },
        422: {
            "description": "Erro de validação nos parâmetros.",
            "model": ErrorResponse,
        },
        200: {
            "description": "Email enviado..",
            "model": ErrorResponse,
        },

    }
)
def enviar_email_admin(destinatario: str, assunto: str, mensagem_html: str,):

    emailEnviado = EmailService.enviar_email

    return emailEnviado

@routerAdmin.post(endpointAdmin + '/atualizar-usuario',
    response_model=UsuarioSchemas.UsuarioReponse,
    summary="Atualizar dados de um usuário",
    description=(
        "Este endpoint permite que um administrador atualize os dados de um usuário existente. "
        "Os dados podem incluir nome, e-mail, senha e notificações ativadas."
    ),
    tags=["Usuários"],
    responses={
        400: {
            "description": "Erro de validação dos dados enviados.",
            "model": ErrorResponse,
        },
        404: {
            "description": "Usuário não encontrado.",
            "model": ErrorResponse,
        },
        401: {
            "description": "Token de autenticação inválido ou ausente.",
            "model": ErrorResponse,
        },
        422: {
            "description": "Erro de validação nos parâmetros.",
            "model": ErrorResponse,
        },
        200: {
            "description": "Usuário atualizado.",
            "model": ErrorResponse,
        },
    }
)
def atualizar_usuario_admin(usuario_id: int, usuario: UsuarioSchemas.UpdateUserRequest,db: Session= Depends(get_db)):

    usuarioAtualizado = UsuarioService.atualizar_usuario(db, usuario_id, usuario)

    return usuarioAtualizado

