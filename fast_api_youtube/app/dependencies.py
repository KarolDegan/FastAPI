from fastapi import Depends, HTTPException
from app.main import SECRET_KEY,ALGORITHM,oauth2_schema
from app.bank.models import db, Usuario
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db) #abrindo conexão
        session = Session() #criando 1 sessão
        yield session #retorno temporário da sessão
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token,SECRET_KEY,ALGORITHM) # da como resposta o dicionário com as informações do usuário
        id_usuario = int(dic_info.get("sub"))
    except JWTError as e:
        print(f"Erro ao decodificar o token: {str(e)}")
        raise HTTPException(status_code=401, detail="Acesso Negado,verifique a validade do token")

    usuario = (session.query(Usuario).filter(Usuario.id == id_usuario).first())
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")

    #verificar se o token é válido
    #extrair o ID do usuário dono do token
    
    return usuario