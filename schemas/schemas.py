from pydantic import BaseModel
from typing import Optional

class Endereco(BaseModel):
    id: Optional[int]
    pais: str
    estado: str
    municipio: str
    cep: str
    rua: str
    numero: int
    complemento: Optional[int]
    usuario_id: Optional[int]

    class Config:
        orm_mode = True

class User(BaseModel):
    id: Optional[int]
    nome: str
    email: str
    cpf: str
    pis: int
    senha: str
    endereco: Optional[Endereco]

    class Config:
        orm_mode = True

class LoginData(BaseModel):
    senha: str
    email: str