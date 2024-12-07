from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.usuarios import UsuarioModel
import logging

def deletar_usuario_por_id(id: int,  db: Session ):

    existeUsuario =  db.query(UsuarioModel.Usuario).filter(UsuarioModel.Usuario.id == id).first()

    logging.info(f"Deletando usuario com o id: {id} no banco de dados")
    if not existeUsuario:
        logging.warning("Usuário não existe!")
        raise HTTPException(status_code= 404, detail = "Usuário não encontrado")

    db.delete(existeUsuario)
    db.commit()

