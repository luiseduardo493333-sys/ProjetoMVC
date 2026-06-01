#Tabela de movimentacao

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class tipo_de_movimentacao(String, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    tipo = Column(Enum(tipo_de_movimentacao), nullable=False)

    valor = Column(Integer, nullable=False)

    data = Column(DateTime, nullable=False)
