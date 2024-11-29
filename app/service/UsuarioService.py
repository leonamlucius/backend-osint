import bcrypt
from fastapi import HTTPException

from app.models.usuarios import UsuarioSchemas, UsuarioModel
from sqlalchemy.orm import Session




def obter_usuario_pelo_id(db: Session, usuario_id: int):
    usuario = db.query(UsuarioModel.Usuario).filter(usuario_id == UsuarioModel.Usuario.id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

def obter_usuario_pelo_email(db: Session, user_email: str):
    usuario = db.query(UsuarioModel.Usuario).filter(user_email == UsuarioModel.Usuario.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

def criar_usuario(db: Session, usuario: UsuarioSchemas.CreateUserRequest):

    usuario_existente = db.query(UsuarioModel.Usuario).filter(usuario.email == UsuarioModel.Usuario.email).first()
    if usuario_existente:
        raise ValueError("Já existe um usuário com esse e-mail.")

    senha_criptografada = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt())

    db_usuario = UsuarioModel.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_criptografada.decode('utf-8')
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
