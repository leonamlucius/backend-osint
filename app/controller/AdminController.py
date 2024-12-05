from fastapi import APIRouter, HTTPException, Depends, status

from app.controller.UsuarioController import atualizar_usuario
from app.db.database import SessionLocal, engine
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


@routerAdmin.get(endpointAdmin + "{usuarioId}", response_model = UsuarioSchemas.UsuarioReponse)
def obter_usuario_por_id_admin(usuarioId: int, db: Session = Depends(get_db)):
    usuarioEncontrado = UsuarioService.obter_usuario_pelo_id(db, usuarioId)

    return usuarioEncontrado

@routerAdmin.delete(endpointAdmin + "deletar/{id}")
def deletar_usuario_por_id_admin(id: int,  db: Session = Depends(get_db)):

    usuarioApagado = AdminService.deletar_usuario_por_id(id, db)

    return usuarioApagado

@routerAdmin.post(endpointAdmin, response_model = UsuarioSchemas.UsuarioReponse, status_code=status.HTTP_201_CREATED )
def criar_usuario_admin(usuario: UsuarioSchemas.CreateUserRequest,  db: Session= Depends(get_db)):

    usuarioAdmin = UsuarioService.criar_usuario(db, usuario)

    return usuarioAdmin

@routerAdmin.post(endpointAdmin + '/email')
def enviar_email_admin(destinatario: str, assunto: str, mensagem_html: str):

    emailEnviado = EmailService.enviar_email

    return emailEnviado

@routerAdmin.post(endpointAdmin + '/atualizar-usuario')
def atualizar_usuario_admin(usuario_id: int, usuario: UsuarioSchemas.UpdateUserRequest,db: Session= Depends(get_db)):

    usuarioAtualizado = UsuarioService.atualizar_usuario(db, usuario_id, usuario)

    return usuarioAtualizado

