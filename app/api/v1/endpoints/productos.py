from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.productos import ProductoCreate, ProductoResponse
from app.crud.productos import create_producto, get_producto_by_codigo, get_productos, get_producto_by_id, update_producto, delete_producto
from typing import List
from app.api.deps import get_current_user
from app.models.usuario import Usuario

router = APIRouter()

# REQUEST GET
@router.get("/", response_model=List[ProductoResponse])
def listar_productos(
    skip: int = 0, 
    limit: int = 100, 
    nombre: str | None = None,
    db: Session = Depends(get_db)
    ):
    return get_productos(db, skip=skip, limit=limit, nombre=nombre)

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# REQUEST POST
@router.post("/", response_model=ProductoResponse)
def crear_nuevo_producto(producto: ProductoCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(get_current_user)):
    db_producto = get_producto_by_codigo(db, codigo=producto.codigo)
    if db_producto:
        raise HTTPException(status_code=400, detail="Producto ya existente")
    return create_producto(db=db, producto=producto)

# REQUEST PUT
@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(get_current_user)):
    db_producto = update_producto(db, producto_id, producto)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# REQUEST DELETE
@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(get_current_user)):
    db_producto = delete_producto(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
