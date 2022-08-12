from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db 
from providers import token_provider
from jose import JWTError
from repositorios.usuario import RepositorioUsuario

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

def obter_usuario_logado(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
    exception = HTTPException(status_code=401, detail='Token inválido')

    try:
        email = token_provider.verificar_access_token(token)
    except JWTError:
        raise exception

    if not email:
        raise exception

    usuario = RepositorioUsuario(session).obter_usuario_por_email(email)

    if not usuario:
        raise exception

    return usuario