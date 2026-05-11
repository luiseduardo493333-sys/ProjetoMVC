# 1. Hash e verificação de senha com bcrpt
# 2. Gerção de token JWT
# 3. leitrua e validção do token vindo de cookie

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import requests, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALOGRITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACESS_TOKEN_EXPIRE_MINUTES")

#CryptContext - configure o bycrpt como algoritmo de hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# funções de senha
def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha = senha_hash)

#  funções do token - JWT
def criar_toke(data: dict):
    payload = data.copy()

    # definir quando o token vai expirar
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})

    # Criar o token - JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALOGRITHM)
    return token

def decodificar_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALOGRITHM])
    return payload

# dependecias dp FastAPI
def get_usuario_logado(request: requests):

    token = request.cookies.get("acess_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    
    try:
        payload = decodificar_token(token)
        email = payload.get("sub")


        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return payload
    except JWTError:
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"

        )
    

def usuario_opcional(request: Request):
    try:
        return get_usuario_logado(request)
    except HTTPException:
        return None