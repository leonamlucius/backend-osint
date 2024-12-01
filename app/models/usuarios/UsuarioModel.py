from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db.Base import Base

class Usuario(Base):
    __tablename__ = "usuarios"  # Corrigido aqui
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    senha = Column(String, index=True, nullable=False)
    data_criacao = Column(DateTime, default = datetime.utcnow)
    notificacoes_ativadas = Column(Boolean, default=False)

    vazamentos = relationship("Vazamento", back_populates="usuario")