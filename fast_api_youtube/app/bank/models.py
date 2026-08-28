from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
#from sqlalchemy_utils import ChoiceType

#cria a conexão com o banco

db = create_engine("sqlite:///app/bank/database/banco.db")

"""
Quando você escreve sqlite:///database/banco.db, o SQLite tenta procurar uma pasta chamada database dentro do diretório atual de trabalho do contêiner Docker (geralmente /app). Se essa pasta não existir dentro do contêiner, o SQLAlchemy vai falhar silenciosamente ou dar erro de OperationalError ao tentar ler.
"""

# cria a base de dados
Base = declarative_base()

#criar as classes/tabelas do banco
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = [
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #pendente, cancelado, finalizado
    preco = Column("preco", Float) #preço total de todos os itens do pedido
    usuario_id = Column("usuario_id", ForeignKey("usuarios.id"))
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario_id, status="PENDENTE", preco=0):
        self.status = status
        self.preco = preco
        self.usuario_id = usuario_id
        
    
    def calcular_preco(self):
        self.preco = sum(item.quantidade * item.preco_unitario for item in self.itens)

class ItemPedido(Base):
    __tablename__ = "pedido_itens"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido_id = Column("pedido_id", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido_id):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido_id = pedido_id    

#metodos do banco
