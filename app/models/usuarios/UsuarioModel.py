from operator import index

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db.Base import Base
from app.utils.assets.Images_url import usuario_avatar


class Usuario(Base):
    __tablename__ = "usuarios"  # Corrigido aqui
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    senha = Column(String, index=True, nullable=False)
    avatar = Column(String, index=True, nullable=False, default=usuario_avatar)
    data_criacao = Column(DateTime, index=True, default = datetime.utcnow)
    notificacoes_ativadas = Column(Boolean, index=True, default=False)

    vazamentos = relationship("Vazamento", back_populates="usuario", cascade = "all,delete") # O cascade pra poder fazer delete das tabelas, tanto usuario quanto vazamentos