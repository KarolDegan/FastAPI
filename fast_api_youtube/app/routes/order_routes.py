from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import pegar_sessao, verificar_token, Session
from app.bank.schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from app.bank.models import Pedido, ItemPedido
from app.bank.models import Usuario
from typing import List

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)]) #todas as rotas de pedido precisam do token 

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """
    return {"mensagem" : "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def pedido(pedido_schema: PedidoSchema,  session = Depends(pegar_sessao)):
    try:
        novo_pedido = Pedido(usuario_id = pedido_schema.id_usuario)
        session.add(novo_pedido)
        session.commit()
        return {"mensagem" : f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}. Usuário {pedido_schema.id_usuario}"}
    except Exception as e:
       raise HTTPException(status_code=400, detail=f"Erro ao criar pedido {pedido_schema.id} {str(e)}")

#usuario: Usuario = Depends(verificar_token) vai retornar um usuário que já teve o token verificado

@order_router.get("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail=f"Pedido com ID {id_pedido} não encontrado")
    if not usuario.admin and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar este pedido")
    pedido.status = "CANCELADO"
    session.commit()
    return {"mensagem": f"Pedido com ID {pedido.id} cancelado com sucesso",     
            "pedido": pedido 
    }

@order_router.get("/listar")
async def listar_pedidos(session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para listar todos os pedidos")
    else:
        pedidos = session.query(Pedido).all()
        return {"pedidos": pedidos}

@order_router.post("/pedido/adicionar_item/{id_pedido}")
async def adicionar_item(id_pedido: int, item_schema: ItemPedidoSchema, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail=f"Pedido com ID {id_pedido} não encontrado")
    if not usuario.admin and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar itens a este pedido")
    
    item_pedido = ItemPedido(item_schema.quantidade, item_schema.sabor, item_schema.tamanho, item_schema.preco_unitario, id_pedido)

    session.add(item_pedido)
    pedido.calcular_preco() #chama o método calcular_preco para atualizar o preço do pedido
    session.commit()
    return {"mensagem": f"Item adicionado ao pedido com ID {id_pedido} com sucesso",   
            "item": item_pedido,
            "pedido": pedido.preco
    }

@order_router.post("/pedido/remover_item/{id_item_pedido}")
async def remover_item(id_item_pedido: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=404, detail=f"Item de pedido com ID {id_item_pedido} não encontrado")

    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido_id).first()

    if not usuario.admin and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para remover itens deste pedido")
    
    
    session.delete(item_pedido)
    
    pedido.calcular_preco()
    session.commit()
    return {"mensagem": f"Item removido do pedido com ID {item_pedido.pedido_id} com sucesso",
            "itens_pedido": pedido.itens,   
            "pedido": pedido
    }

@order_router.get("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail=f"Pedido com ID {id_pedido} não encontrado")
    if not usuario.admin and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para finalizar este pedido")
    pedido.status = "FINALIZADO"
    session.commit()
    return {"mensagem": f"Pedido com ID {pedido.id} finalizado com sucesso",     
            "pedido": pedido 
    }

@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao) ):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    if usuario.id != pedido.usuario_id and not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para vizualizar esse pedido")
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

@order_router.get("/listar/pedido_usuario", response_model = List[ResponsePedidoSchema]) #define o modelo de saida das respostas
def listar_pedidos(session: Session = Depends(pegar_sessao), usuario:Usuario = Depends(verificar_token)):
    try:
        pedidos = session.query(Pedido).filter(Pedido.usuario_id == usuario.id).all()
        return pedidos
    except Exception as e:
        print(f"Erro ao listar pedidos do usuário {str(e)}")
        
    