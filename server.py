from fastapi import FastAPI
from config.database import criar_bd
from fastapi.middleware.cors import CORSMiddleware
from routers import usuarios, endereco

criar_bd()
app = FastAPI()

origins = [""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Rotas de Usuários
app.include_router(usuarios.app)

# Rotas relacionadas aos Endereços
app.include_router(endereco.app)