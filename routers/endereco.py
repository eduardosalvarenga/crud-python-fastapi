from fastapi import APIRouter, Depends
from schemas.schemas import Endereco
from repositorios.usuario import RepositorioUsuario
from sqlalchemy.orm import Session
from config.database import get_db

app = APIRouter()

# Editar o endereço de um usuário com base no id
@app.put('/endereco/{user_id}')
def atualizar_endereco(user_id: int, endereco: Endereco, db: Session = Depends(get_db)):
    RepositorioUsuario(db).atualizar_endereco(user_id, endereco)
    return {"mensagem": "endereço atualizado"}