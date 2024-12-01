from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.Base import Base

class Usuario(Base):
    __tablename__ = "usuarios"  # Corrigido aqui
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    senha = Column(String, index=True, nullable=False)
    data_criacao = Column(DateTime, nullable=True)
    notificacoes_ativadas = Column(Boolean, default=False)

    vazamentos = relationship("Vazamento", back_populates="usuario")