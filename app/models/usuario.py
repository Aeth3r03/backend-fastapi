import enum
from sqlalchemy import Column, Integer, String, ARRAY
from app.db.database import Base

class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    INVENTORY_MANAGER = 'inventory_manager'
    DEVELOPER = 'developer'
    VIEWER = 'viewer'

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    roles = Column(ARRAY(String), default=[UserRole.VIEWER.value], nullable=False)