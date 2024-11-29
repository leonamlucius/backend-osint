from fastapi import APIRouter, HTTPException, Depends, status
from app.service import UsuarioService
from app.models.usuarios import UsuarioModel, UsuarioSchemas
from app.db.database import SessionLocal, engine
from sqlalchemy.orm import Session

UsuarioModel.Base.metadata.create_all(bind= engine)
routerusuarios = APIRouter()

endpointUsuario = "/usuarios/"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@routerusuarios.get(endpointUsuario + "{usuarioId}", response_model= UsuarioSchemas.UsuarioReponse)
def obter_usuario_por_id(usuarioId: int, db: Session= Depends(get_db)):
    usuarioEncontrado = UsuarioService.obter_usuario_pelo_id(db, usuarioId)
    return usuarioEncontrado

@routerusuarios.get(endpointUsuario + "procurar/{usuarioEmail}", response_model= UsuarioSchemas.UsuarioReponse)
def obter_usuario_por_email(usuarioEmail: str, db: Session= Depends(get_db)):

    usuarioEncontrado = UsuarioService.obter_usuario_pelo_email(db, usuarioEmail)
    return usuarioEncontrado


@routerusuarios.post(endpointUsuario, response_model = UsuarioSchemas.UsuarioReponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioSchemas.CreateUserRequest, db: Session= Depends(get_db)):

    usuario = UsuarioService.criar_usuario(db, usuario)

    return  usuario





