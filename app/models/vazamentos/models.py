from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from app.db.Base import Base

class Vazamento(Base):
    __tablename__ = "vazamentos"  # Corrigido aqui
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    titulo = Column(String, index=True)
    dominio_url = Column(String, index=True)
    data_vazamento = Column(Date, nullable=True, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, nullable=True)
    descricao = Column(String, index=True)
    image_uri = Column(String, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="vazamentos")

