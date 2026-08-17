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