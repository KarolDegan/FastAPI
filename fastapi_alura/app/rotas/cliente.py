from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated

from modelos.cliente import Cliente, ClienteCriarAtualizar
from banco_de_dados.cliente_repositorio import ClienteRepositorio
from dependencias import obter_cliente_repositorio

CLIENTE_LIST = [Cliente(id_=1, nome="João Silva", email="joao.silva@example.com", telefone="(11) 1111-1111"),
                Cliente(id_=2, nome="Maria Oliveira", email="maria.oliveira@example.com", telefone="(11) 2222-2222")]

router = APIRouter(
    prefix="/clientes" #define um prefixo que será adicionado automaticamente a todas as rotas desse roteador

)

@router.get("/", response_model=list[Cliente])
async def listar_clientes(cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)]):
    return await cliente_repositorio.listar_clientes()
    
    
    return CLIENTE_LIST

@router.get("/{cliente_id}", response_model=Cliente | None)
async def obter_cliente(cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)], cliente_id: int):
    cliente = await cliente_repositorio.obter_cliente(cliente_id)
    if not cliente:
        return HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.post("/", response_model=Cliente, status_code=201)
async def criar_cliente(
    cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)],
    cliente: ClienteCriarAtualizar
):
    
    return await cliente_repositorio.criar_cliente(cliente)

@router.put("/{cliente_id}", response_model=Cliente | None)
async def atualizar_cliente(
    cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)],
    cliente_id: int,
    cliente_atualizado: ClienteCriarAtualizar
):
    cliente_atualizado = await cliente_repositorio.atualizar_cliente(cliente_id, cliente_atualizado)
    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente_atualizado

@router.delete("/{cliente_id}", status_code=204)
async def deletar_cliente(
    cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)],
    cliente_id: int
):
    sucesso = await cliente_repositorio.deletar_cliente(cliente_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")