from fastapi import APIRouter, HTTPException, Depends
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




@routerusuarios.get(endpointUsuario + "procurar/{usuarioId}", response_model= UsuarioSchemas.UsuarioReponse)
def obter_usuario_por_id(usuarioId: int, db: Session= Depends(get_db)):

    usuarioEncontrado = UsuarioService.get_usuarios(db, usuarioId)

    if usuarioEncontrado is None:
        raise HTTPException(status_code = 404, detail= "Usuario não encontrado")


    return usuarioEncontrado






