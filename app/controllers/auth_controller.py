from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_toke


router = APIRouter(prefix="/auth", tags=["Autentificação"])

templastes = Jinja2Templates(directory="app/templates")

@router.get("/cadastro")
def tela_cadastro (request: Request):
        return templastes.TemplateResponse(
                request,
                "auth/cadastro.html",
               {"request": request}
        )

#Tela login

@router.get("/login")
def tela_login (request: Request):
        return templastes.TemplateResponse(
                request,
                "auth/login.html",
               {"request": request}
        )

# rota para criar um usuario no banco de daos
@router.post("/cadastro")
def fazer_cadastro(
        request: Request,
        nome: str = Form(...),
        email: str = Form(...),
        senha: str = Form(...),
        db: Session = Depends(get_db)
):
        #verificar o email do usuario
        user_existente = db.query(Usuario).filter_by(email=email).first()

        if user_existente:
                return templastes.TemplateResponse(
                        request,
                        "auth/cadastro.html",
                        {"request": request,"erro": "Este e-mail já esta cadastrado"}
                )
        
        #Cria o novo usuario
        novo_usuario = Usuario(nome=nome, email=email, senha_hash=hash_senha(senha))
        db.add(novo_usuario)
        db.commit()

        return RedirectResponse(url="/auth/login", status_code=302)