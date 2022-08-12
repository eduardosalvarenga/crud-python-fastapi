from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    cpf = Column(String)
    pis = Column(Integer)
    senha = Column(String)
    endereco = relationship("Endereco", back_populates="usuario", uselist=False)

class Endereco(Base):
    __tablename__ = 'endereco'

    id = Column(Integer, primary_key = True)
    pais = Column(String)
    estado = Column(String)
    municipio = Column(String)
    cep = Column(String)
    rua = Column(String)
    numero = Column(Integer)
    complemento = Column(Integer)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship('User', back_populates='endereco')