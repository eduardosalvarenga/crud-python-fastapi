from fastapi import APIRouter, HTTPException
from fastapi import Depends
from schemas.schemas import User, LoginData
from typing import List
from repositorios.usuario import RepositorioUsuario
from sqlalchemy.orm import Session
from config.database import get_db
from providers import hash_provider, token_provider
from routers.auth_utils import obter_usuario_logado

app = APIRouter()

# Listar Todos os Usuários
@app.get("/usuarios", response_model=List[User])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = RepositorioUsuario(db).listar()
    return usuarios

# Adicionar um usuário novo
@app.post('/usuarios', status_code=201, response_model=User)
async def criar_usuario(user: User, db: Session = Depends(get_db)):
    # verificar se já existe um usuario com o email
    usuario_localizado = RepositorioUsuario(db).obter_usuario_por_email(user.email)
    if usuario_localizado:
        raise HTTPException(status_code=400, detail="Já existe um usuário para este telefone")
        
    user.senha = hash_provider.gerar_hash(user.senha)
    usuario_criado = RepositorioUsuario(db).criar(user)
    return usuario_criado

# Editar um usuário existente com base no id
@app.put('/usuarios/{id}')
def atualizar_usuario(id: int, user: User, db: Session = Depends(get_db)):
    RepositorioUsuario(db).atualizar(id, user)
    return {"mensagem": "usuario atualizado"}

# Deletar um usuário existente com base no id
@app.delete('/usuarios/{id}')
def remover_usuario(id: int, db: Session = Depends(get_db)):
    RepositorioUsuario(db).remover(id)
    return {"mensagem": "usuario removido"}

# Login
@app.post('/token')
def login(login_data: LoginData, db: Session = Depends(get_db)):
    senha = login_data.senha
    email = login_data.email

    usuario = RepositorioUsuario(db).obter_usuario_por_email(email)

    if not usuario:
        raise HTTPException(status_code=400, detail='Email ou senha estão incorretos!')

    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)

    if not senha_valida:
        raise HTTPException(status_code=400, detail='Email ou senha estão incorretos!')

    token = token_provider.criar_access_token({'sub': usuario.email})
    return {'usuario': usuario, 'access_token': token}

@app.get('/me')
def me(usuario: User = Depends(obter_usuario_logado)):
    return usuario