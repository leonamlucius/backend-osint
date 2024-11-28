from app.models.vazamentos import models, schemas
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




def get_vazamento(db: Session, vazamentoId: int):
  return db.query(models.Vazamento).filter(vazamentoId == models.Vazamento.id).first()




def get_vazamento_by_email(email: str, db: Session):
  return db.query(models.Vazamento).filter(email == models.Vazamento.email).first()


def get_all_vazamentos(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Vazamento).offset(skip).limit(limit).all()


def create_vazamento(vazamento: schemas.VazamentoRequest, db: Session):

  db_vazamento = models.Vazamento(
    email= vazamento.email

  )
  db.add(db_vazamento)
  db.commit()
  db.refresh(db_vazamento)
  return db_vazamento