from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_toke


router = APIRouter(prefix="/auth", tags=["Autentificação"])

templastes = Jinja2Templates(directory="app/templates")

@router.get("/cadrasto")
def tela_cadrasto (request: Request):
        return templastes.TemplateResponse(
                request,
                "auth/cadrasto.html",
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