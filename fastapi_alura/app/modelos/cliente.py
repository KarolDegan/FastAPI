from pydantic import BaseModel

class Cliente(BaseModel):
    id_: int #apenas id é um método interno do Python, então usamos id_ para evitar conflitos
    nome: str
    email: str
    telefone: str

class ClienteCriarAtualizar(BaseModel):
    nome: str
    email: str
    telefone: str