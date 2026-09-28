from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.config import settings
from app.core.permissions import has_permission
from app.crud.usuario import get_usuario_by_username
from app.schemas.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        roles = payload.get("roles", [])
        if username is None:
            raise credenciales_invalidas
    except JWTError:
        raise credenciales_invalidas

    usuario = get_usuario_by_username(db, username)
    if usuario is None:
        raise credenciales_invalidas
    return Usuario(id=usuario.id, username=username, roles=roles)

def require_permission(permission: str):
    def permission_checker(current_user: Usuario = Depends(get_current_user)):
        has_perm = has_permission(current_user.roles, permission)

        if not has_perm:
            raise HTTPException(
                status_code=403,
                detail=f"Falta de permiso. Permiso requerido: { permission }"
            )
        
        return current_user
    return Depends(permission_checker)