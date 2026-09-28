from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List

class Usuario(BaseModel):
    id: int
    username: str
    roles: List[str]
    
    model_config = ConfigDict(from_attributes=True)

class UsuarioConPermisos(Usuario):
    permissions: List[str]