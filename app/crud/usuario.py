from sqlalchemy.orm import Session
from app.models.usuario import Usuario

def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()