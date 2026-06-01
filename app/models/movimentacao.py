#Tabela de movimentacao

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TipoDeMovimentacao(String, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tipo = Column(Enum(TipoDeMovimentacao), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Integer, nullable=False, default=0.0)
    observacao = Column(String(255), nullable=True)
    criado_em = Column(DateTime, server_default=func.now())

    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=False)

    #Relacionamento
    produto = relationship("Produto", back_populates="movimentacoes")
    usuario = relationship("Usuario", back_populates="movimentacoes")

    @property
    def valor_total(self):
        return self.quantidade * self.preco_unitario