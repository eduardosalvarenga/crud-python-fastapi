from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from schemas import schemas
from models import models

class RepositorioUsuario():

    def __init__(self, db: Session):
        self.db = db

    def criar(self, usuario: schemas.User):
        bd_usuario = models.User(nome=usuario.nome, email=usuario.email, cpf=usuario.cpf, 
        pis=usuario.pis, 
        senha=usuario.senha,
        endereco = models.Endereco(pais=usuario.endereco.pais, estado=usuario.endereco.estado,
        municipio=usuario.endereco.municipio, cep=usuario.endereco.cep, rua=usuario.endereco.rua,
        numero=usuario.endereco.numero, complemento=usuario.endereco.complemento)
        )

        self.db.add(bd_usuario)
        self.db.commit()
        self.db.refresh(bd_usuario)
        return bd_usuario

    def listar(self):
        stmt = select(models.User)
        usuarios = self.db.execute(stmt).scalars().all()
        return usuarios

    def atualizar(self, id: int, usuario: schemas.User):
        update_stmt = update(models.User).where(
            models.User.id == id).values(
                nome=usuario.nome,
                email=usuario.email,
                cpf=usuario.cpf, 
                pis=usuario.pis, 
                senha=usuario.senha,
            )
        self.db.execute(update_stmt)
        self.db.commit()

    def remover(self, id: int):
        delete_endereco = delete(models.Endereco).where(
            models.Endereco.usuario_id == id
        )
        self.db.execute(delete_endereco)
        delete_stmt = delete(models.User).where(
            models.User.id == id
        )
        self.db.execute(delete_stmt)
        self.db.commit()

    def atualizar_endereco(self, user_id: int, endereco: schemas.Endereco):
        update_stmt = update(models.Endereco).where(
            models.Endereco.usuario_id == user_id
        ).values(
            pais=endereco.pais,
            estado=endereco.estado,
            municipio=endereco.municipio,
            cep=endereco.cep,
            rua=endereco.rua,
            numero=endereco.numero,
            complemento=endereco.complemento
        )
        self.db.execute(update_stmt)
        self.db.commit()

    # Buscar o primeiro usuário cadastrado com x email
    def obter_usuario_por_email(self, email):
        query = select(models.User).where(models.User.email == email)
        return self.db.execute(query).scalars().first()