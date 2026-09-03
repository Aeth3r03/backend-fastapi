from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.schemas.productos import ProductoResponse
from app.crud.categoria import get_categorias, create_categoria, get_categoria_by_id, update_categoria, delete_categoria
from app.crud.productos import get_producto_by_categoria
from app.models.usuario import Usuario
from app.api.deps import get_current_user
import shutil
from pathlib import Path

router = APIRouter()
UPLOAD_DIR = Path("static/categorias")

not_found = HTTPException(
    status_code=404,
    detail="categoría no encontrada"
)

error_delete = HTTPException(
    status_code=400,
    detail="No fue posible borrar la categoria, tiene productos en ella"
)

TIPOS_PERMITIDOS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
}

MAX_TAMANO_BYTES = 5 * 1024 * 1024

#GET
@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    
    return get_categorias(db)

@router.get("/{categoria_id}", response_model=List[ProductoResponse])
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100): # type: ignore
    db_categoria = get_categoria_by_id(db, categoria_id)
    if not db_categoria:
        raise not_found
    return get_producto_by_categoria(db, categoria_id, skip=skip, limit=limit)

#POST
@router.post("/", response_model=CategoriaResponse)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(get_current_user)):
    return create_categoria(db, categoria)

#PUT
@router.put("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(categoria_id: int, categoria: CategoriaCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(get_current_user)):
    db_categoria = update_categoria(db, categoria_id, categoria)
    if not db_categoria:
        raise not_found
    return db_categoria

#DELETE
@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id, db: Session = Depends(get_db), usario_actual: Usuario = Depends(get_current_user)):
    db_categoria = get_categoria_by_id(db, categoria_id)
    if not db_categoria:
        raise not_found
    hay_productos = get_producto_by_categoria(db, categoria_id)
    if hay_productos:
        raise error_delete
    delete_categoria(db, categoria_id)

#SUBIDA DE ARCHIVOS
#POST
@router.post("/{categoria_id}/imagen", response_model=CategoriaResponse)
async def subir_imagen_categoria(
    categoria_id: int,
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user)
):
    db_categoria = get_categoria_by_id(db, categoria_id)
    if not db_categoria:
        raise not_found

    if imagen.content_type not in TIPOS_PERMITIDOS:
        raise HTTPException(
            status_code=400,
            detail="Tipo de imagen no permitido. Usa JPG, PNG o WebP",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    for archivo_viejo in UPLOAD_DIR.glob(f"{categoria_id}.*"):
        archivo_viejo.unlink()

    ext = TIPOS_PERMITIDOS[imagen.content_type]
    nombre_archivo = f"{categoria_id}{ext}"
    destino = UPLOAD_DIR / nombre_archivo

    tamano = 0
    with destino.open("wb") as buffer:
        while chunk := await imagen.read(1024 * 1024):
            tamano += len(chunk)
            if tamano > MAX_TAMANO_BYTES:
                buffer.close()
                destino.unlink()
                raise HTTPException(
                    status_code=400,
                    detail="La imagen no puede pesar mas de 5MB"
                )
            buffer.write(chunk)

    db_categoria.imagen_url = f"/static/categorias/{nombre_archivo}"
    db.commit()
    db.refresh(db_categoria)
    return db_categoria