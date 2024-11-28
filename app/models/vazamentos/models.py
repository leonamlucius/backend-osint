from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.db.database import Base




class Vazamento(Base):
    __tablename__ = "vazamentos"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
