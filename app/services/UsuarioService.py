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

def atualizar_usuario(db: Session, usuario_id: int, usuario: UsuarioSchemas.UpdateUserRequest):
    usuariodb = obter_usuario_pelo_id(db, usuario_id)


    if usuario.email != usuariodb.email:
        email_usuario_existente = db.query(UsuarioModel.Usuario).filter(
            usuario.email == UsuarioModel.Usuario.email).first()
        if email_usuario_existente:
            raise ValueError("Já existe um usuário com esse e-mail.")


    if usuario.nome:
        usuariodb.nome = usuario.nome
    if usuario.email:
        usuariodb.email = usuario.email
    if usuario.senha:
        senha_criptografada = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt())
        usuariodb.senha = senha_criptografada.decode('utf-8')
    if usuario.notificacoes_ativadas is not None:
        usuariodb.notificacoes_ativadas = usuario.notificacoes_ativadas


    db.commit()
    db.refresh(usuariodb)

    return usuariodb

def obter_lista_de_usuarios_com_notifacao_ativadas(db: Session):

    lista_de_usuarios_ativados = db.query(UsuarioModel.Usuario).filter(UsuarioModel.Usuario.notificacoes_ativadas == True).all()

    return lista_de_usuarios_ativados


