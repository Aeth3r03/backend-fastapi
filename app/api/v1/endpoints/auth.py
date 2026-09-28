from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud.usuario import get_usuario_by_username
from app.core.security import verify_password, crear_token_acceso
from app.api.deps import get_current_user
from app.schemas.token import Token 
from app.schemas.usuario import Usuario, UsuarioConPermisos
from app.core.permissions import get_user_permissions

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = get_usuario_by_username(db, form_data.username)
    if not usuario or not verify_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    token = crear_token_acceso(data={"sub": usuario.username, "roles": usuario.roles})
    return {"access_token": token}

@router.get("/me", response_model=UsuarioConPermisos)
def get_user(usuario: Usuario = Depends(get_current_user)):
    permissions = get_user_permissions(usuario.roles)
    return UsuarioConPermisos(
        id=usuario.id,
        username=usuario.username,
        roles=usuario.roles,
        permissions=permissions
    )

@router.get("/permissions", response_model=list[str])
def get_my_permissions(usuario: Usuario = Depends(get_current_user)):
    return get_user_permissions(usuario.roles)