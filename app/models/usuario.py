from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    has_admin = Column(Boolean, default=False, nullable=False)