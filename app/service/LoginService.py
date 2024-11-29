import bcrypt
from fastapi import HTTPException

from app.models.login import LoginSchemas
from app.models.usuarios import UsuarioModel
from sqlalchemy.orm import Session




def autenticar_usuario(db: Session, dadosLogin: LoginSchemas.LoginRequest):
    usuarioExistente = db.query(UsuarioModel.Usuario).filter(dadosLogin.email == UsuarioModel.Usuario.email).first()

    if not usuarioExistente:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not bcrypt.checkpw(dadosLogin.senha.encode('utf-8'), usuarioExistente.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    return {"message": "Usuário autenticado com sucesso", "user": usuarioExistente.nome}
