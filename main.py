from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import productos
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import categorias


app = FastAPI(
    title="API de Inventario ERP",
    description="Backend para la gestión del negocio",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(productos.router, prefix="/api/v1/productos", tags=["Productos"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(categorias.router, prefix="/api/v1/categorias", tags=["Categorias"])

# AAAAAA:... CON costo lo logré jajajaja, dime que tal si fallé en algo, fue divertido, me gusto este reto. Me gustaría repetir retos así. Copié como se estructuraba los archivos similares, aun que estoy inseguro