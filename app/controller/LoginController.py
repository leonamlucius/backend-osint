from fastapi import APIRouter, HTTPException, Depends, status
from app.services import UsuarioService, LoginService
from app.models.usuarios import UsuarioModel, UsuarioSchemas
from app.models.login import LoginSchemas
from app.db.database import SessionLocal, engine
from sqlalchemy.orm import Session

UsuarioModel.Base.metadata.create_all(bind= engine)
routerlogin = APIRouter()

endpointLogin = "/login"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@routerlogin.post(endpointLogin, response_model = UsuarioSchemas.UsuarioReponse)
def logar_usuario(dadosUsuario: LoginSchemas.LoginRequest, db: Session= Depends(get_db)):
    return  LoginService.autenticar_usuario(db, dadosUsuario)





