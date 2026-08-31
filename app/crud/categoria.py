from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate

def get_categorias(db: Session):
    return db.query(Categoria).all()

def create_categoria(db: Session, categoria: CategoriaCreate):
    db_categoria = Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def get_categoria(db: Session, skip: int = 0, limit: int = 100, nombre: str | None = None):
    query = db.query(Categoria)
    if nombre:
        query = query.filter(Categoria.nombre.ilike(f"%{nombre}"))
    return query.offset(skip).limit(limit).all()

def get_categoria_by_id(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()

def update_categoria(db: Session, categoria_id: int, categoria: CategoriaCreate):
    db_categoria = get_categoria_by_id(db, categoria_id)
    if not db_categoria:
        return None
    for campo, valor in categoria.model_dump().items():
        setattr(db_categoria, campo, valor)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    db_categoria = get_categoria_by_id(db, categoria_id)
    if not db_categoria:
        return None
    db.delete(db_categoria)
    db.commit()
    return db_categoria