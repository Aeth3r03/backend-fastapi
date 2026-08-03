from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    precio: float
    stock: Optional[int] = 0
    disponible: Optional[bool] = True

class ProductoCreate(ProductoBase):
    pass 

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True
