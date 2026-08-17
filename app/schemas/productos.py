from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    precio: float
    stock: Optional[int] = 0
    disponible: Optional[bool] = True
    categoria_id: int

class ProductoCreate(ProductoBase):
    pass 

class ProductoResponse(ProductoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    