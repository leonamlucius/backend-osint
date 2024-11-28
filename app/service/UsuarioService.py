from app.models.usuarios import UsuarioSchemas, UsuarioModel
from sqlalchemy.orm import Session


def obter_vazamentos_por_email(email: str) -> str:

    if not is_valid(email):
        return "O email não pode ser nulo ou vazio."

    return  procurar_email(email)


def is_valid(string: str) -> bool:
    return bool(string)  # Retorna True se não for nulo ou vazio


def procurar_email(usuarioemail : str):

   if usuarioemail in emails:

       return "EMAIL ENCONTRADO "+ emails[usuarioemail]

   return "Não usuário com esse email"

emails = {
    "joao.silva@example.com": "João Silva",
    "maria.oliveira@example.com": "Maria Oliveira",
    "pedro.santos@example.com": "Pedro Santos",
    "ana.lima@example.com": "Ana Lima",
    "carla.souza@example.com": "Carla Souza"
}




def get_usuarios(db: Session, usuarioId: int):
  return db.query(UsuarioModel.Usuario).filter(usuarioId == UsuarioModel.Usuario.id).first()



