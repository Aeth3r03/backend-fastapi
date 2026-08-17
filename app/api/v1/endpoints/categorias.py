from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.schemas.productos import ProductoResponse
from app.crud.categoria import get_categorias, create_categoria, get_categoria_by_id
from app.crud.productos import get_producto_by_categoria
from app.models.usuario import Usuario
from app.api.deps import get_current_user

router = APIRouter()

#GET
@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    
    return get_categorias(db)

@router.get("/{categoria_id}", response_model=List[ProductoResponse])
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_categoria = get_categoria_by_id(db, categoria_id)
    if not db_categoria:
        raise HTTPException(
            status_code=404,
            detail="categoria no encontrada"
        )
    return get_producto_by_categoria(db, categoria_id, skip=skip, limit=limit)

#POST
@router.post("/", response_model=CategoriaResponse)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(get_current_user)):
    return create_categoria(db, categoria)