from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    # se for apenas o que está a cima será transformado em dicionário

    class Config:
        from_attributes = True # não será interpretado como dicionário padrão, mas como uma (ORM)classe que será transformada em sql diretamente em um banco de dados

class PedidoSchema(BaseModel):

    id_usuario: int
    

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True

class ResponsePedidoSchema(BaseModel):
    try:

        id : int
        status : str 
        preco : float 
        itens: List[ItemPedidoSchema]

        class Config:
            from_attributes = True
    except Exception as e:
        print(f"Esso no Schema ResponsePEdidoSchema: {str(e)}")