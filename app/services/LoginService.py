import bcrypt
from fastapi import HTTPException

from app.models.login import LoginSchemas
from app.models.usuarios import UsuarioModel
from sqlalchemy.orm import Session




def autenticar_usuario(db: Session, dadosLogin: LoginSchemas.LoginRequest):

    usuarioExistente = db.query(UsuarioModel.Usuario).filter(
        UsuarioModel.Usuario.email == dadosLogin.email
    ).first()


    if not usuarioExistente:
        raise HTTPException(status_code=404, detail="E-mail ou Senha incorreta, verifique as suas credenciais")


    if not bcrypt.checkpw(dadosLogin.senha.encode('utf-8'), usuarioExistente.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="E-mail ou Senha incorreta, verifique as suas credenciais")


    return usuarioExistente
