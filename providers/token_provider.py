from datetime import datetime, timedelta
from jose import jwt 

SECRET_KEY = 'chave_secreta'
ALGORITHM = 'HS256'
EXPIRES_IN_MINUTES = 3000

def criar_access_token(data: dict):
    dados = data.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MINUTES)

    dados.update({'exp': expiracao})

    token_jwt = jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def verificar_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload.get('sub')