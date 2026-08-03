from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique= True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    disponible = Column(Boolean, default=True)
    