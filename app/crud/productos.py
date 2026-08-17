from sqlalchemy.orm import Session
from app.models.productos import Producto
from app.schemas.productos import ProductoCreate

def get_producto_by_codigo(db: Session, codigo: str):
    return db.query(Producto).filter(Producto.codigo == codigo).first()

def get_producto_by_categoria(
        db: Session, 
        categoria_id: int,
        skip: int = 0,
        limit: int = 100,
        ):
    query = db.query(Producto).filter(Producto.categoria_id == categoria_id).offset(skip).limit(limit).all()
    return query

def get_productos(
        db: Session, 
        skip: int = 0, 
        limit: int =100,
        nombre: str | None = None,
        disponible: bool | None = None
        ):
    
    query = db.query(Producto)
    if nombre:
        query = query.filter(Producto.nombre.ilike(f"%{nombre}"))
    if disponible is not None:
        query = query.filter(Producto.disponible == disponible)
    return query.offset(skip).limit(limit).all()

def get_producto_by_id(
        db: Session, 
        producto_id: int
        ):
    
    return db.query(Producto).filter(Producto.id == producto_id).first()

def create_producto(
        db: Session, 
        producto: ProductoCreate
        ):
    
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto: ProductoCreate):
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        return None
    for campo, valor in producto.model_dump().items():
        setattr(db_producto, campo, valor)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        return None
    db.delete(db_producto)
    db.commit()
    return db_producto