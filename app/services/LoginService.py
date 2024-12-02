import logging

import bcrypt
from fastapi import HTTPException

from app.models.login import LoginSchemas
from app.models.usuarios import UsuarioModel
from sqlalchemy.orm import Session



def autenticar_usuario(db: Session, dadosLogin: LoginSchemas.LoginRequest):
    logging.info(f"Tentando autenticar usuário com e-mail: {dadosLogin.email}")

    usuarioExistente = db.query(UsuarioModel.Usuario).filter(
        UsuarioModel.Usuario.email == dadosLogin.email
    ).first()

    if not usuarioExistente:
        logging.warning(f"Falha na autenticação: E-mail não encontrado {dadosLogin.email}")
        raise HTTPException(status_code=404, detail="E-mail ou Senha incorreta, verifique as suas credenciais")

    if not bcrypt.checkpw(dadosLogin.senha.encode('utf-8'), usuarioExistente.senha.encode('utf-8')):
        logging.warning(f"Falha na autenticação: Senha incorreta para o e-mail {dadosLogin.email}")
        raise HTTPException(status_code=401, detail="E-mail ou Senha incorreta, verifique as suas credenciais")

    logging.info(f"Usuário com e-mail {dadosLogin.email} autenticado com sucesso.")
    return usuarioExistente