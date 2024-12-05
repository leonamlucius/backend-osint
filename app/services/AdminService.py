

from sqlalchemy.orm import Session
from app.models.usuarios import UsuarioModel


def deletar_usuario_por_id(id: int,  db: Session ):


    existeUsuario =  db.query(UsuarioModel.Usuario).filter(UsuarioModel.Usuario.id == id).first()

    if not existeUsuario:
        return "Não existe esse usuario"

    db.delete(existeUsuario)
    db.commit()

