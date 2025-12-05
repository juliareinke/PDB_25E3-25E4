from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base, engine

# TESTE DE PERFORMANCE 5

class PaginaWiki(Base):
    __tablename__ = "paginas_wiki"

    id_pagina = Column(Integer, primary_key=True)
    url = Column(Text, unique=True, nullable=False)
    titulo = Column(Text)
    status_code = Column(Integer)
    data_coleta = Column(DateTime, default=datetime.now)

    secoes = relationship("SecaoWiki", back_populates="pagina")


class SecaoWiki(Base):
    __tablename__ = "secoes_wiki"

    id_secao = Column(Integer, primary_key=True)
    id_pagina = Column(Integer, ForeignKey("paginas_wiki.id_pagina"), nullable=False)
    titulo_secao = Column(Text, nullable=False)
    nivel = Column(Integer) 
    ordem = Column(Integer)
    conteudo_resumido = Column(Text)

    pagina = relationship("PaginaWiki", back_populates="secoes")


class ErroWiki(Base):
    __tablename__ = "erros_wiki"

    id_erro = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    mensagem = Column(Text)
    data_erro = Column(DateTime, default=datetime.now)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")
