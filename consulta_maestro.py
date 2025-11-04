from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Numeric,
    ForeignKey,
    text,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)
Base = declarative_base()

class Artista(Base):
    __tablename__ = "artistas"

    id_artista = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    instrumento_principal = Column(String(60))
    genero_musical = Column(String(40))
    data_entrada = Column(Date)

    projetos = relationship(
        "Projeto",
        secondary="artista_projeto",
        back_populates="artistas",
    )


class Projeto(Base):
    __tablename__ = "projetos"

    id_projeto = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    status = Column(String(20), nullable=False, default="em_producao")
    data_inicio = Column(Date)
    data_fim = Column(Date)
    orcamento = Column(Numeric(12, 2))

    sessoes = relationship("Sessao", back_populates="projeto")
    artistas = relationship(
        "Artista",
        secondary="artista_projeto",
        back_populates="projetos",
    )


class Estudio(Base):
    __tablename__ = "estudios"

    id_estudio = Column(Integer, primary_key=True)
    nome = Column(String(60), nullable=False, unique=True)
    capacidade = Column(Integer)

    sessoes = relationship("Sessao", back_populates="estudio")


class Sessao(Base):
    __tablename__ = "sessoes"

    id_sessao = Column(Integer, primary_key=True)
    id_projeto = Column(
        Integer,
        ForeignKey("projetos.id_projeto"),
        nullable=False,
    )
    id_estudio = Column(
        Integer,
        ForeignKey("estudios.id_estudio"),
        nullable=False,
    )
    data_horario = Column(DateTime, nullable=False)
    duracao_horas = Column(Numeric(4, 2), nullable=False)
    status = Column(String(20), nullable=False, default="Agendada")

    projeto = relationship("Projeto", back_populates="sessoes")
    estudio = relationship("Estudio", back_populates="sessoes")


class ArtistaProjeto(Base):
    __tablename__ = "artista_projeto"

    id_artista = Column(
        Integer,
        ForeignKey("artistas.id_artista"),
        primary_key=True,
    )
    id_projeto = Column(
        Integer,
        ForeignKey("projetos.id_projeto"),
        primary_key=True,
    )

QUERY_A = text("""
SELECT
  s.id_sessao,
  p.nome AS nome_projeto,
  e.nome AS nome_estudio,
  s.data_horario,
  s.duracao_horas,
  s.status
FROM sessoes s
INNER JOIN projetos p ON p.id_projeto = s.id_projeto
INNER JOIN estudios e ON e.id_estudio = s.id_estudio
ORDER BY s.data_horario;
""")

QUERY_B = text("""
SELECT
  p.id_projeto,
  p.nome AS nome_projeto,
  s.id_sessao,
  s.data_horario,
  s.status AS status_sessao
FROM projetos p
LEFT JOIN sessoes s ON s.id_projeto = p.id_projeto
ORDER BY p.id_projeto, s.data_horario;
""")

QUERY_C = text("""
SELECT
  p.id_projeto,
  p.nome AS nome_projeto,
  ap.id_artista
FROM artista_projeto ap
RIGHT JOIN projetos p ON ap.id_projeto = p.id_projeto
ORDER BY p.id_projeto;
""")

def consultar_como_dicionarios():
    """
    Executa as três consultas SQL e retorna os resultados
    como listas de dicionários.
    """
    with engine.connect() as conn:
        resultado_a = conn.execute(QUERY_A).mappings().all()
        resultado_b = conn.execute(QUERY_B).mappings().all()
        resultado_c = conn.execute(QUERY_C).mappings().all()

        dicts_a = [dict(linha) for linha in resultado_a]
        dicts_b = [dict(linha) for linha in resultado_b]
        dicts_c = [dict(linha) for linha in resultado_c]

    return dicts_a, dicts_b, dicts_c

def consultar_como_listas():
    """
    Executa as três consultas SQL e retorna os resultados
    como listas.
    """
    with engine.connect() as conn:
        linhas_a = conn.execute(QUERY_A).all()
        linhas_b = conn.execute(QUERY_B).all()
        linhas_c = conn.execute(QUERY_C).all()

        listas_a = [list(linha) for linha in linhas_a]
        listas_b = [list(linha) for linha in linhas_b]
        listas_c = [list(linha) for linha in linhas_c]

    return listas_a, listas_b, listas_c


if __name__ == "__main__":
    # DICIONÁRIOS
    a_dicts, b_dicts, c_dicts = consultar_como_dicionarios()

    print("\n=== CONSULTA A (INNER JOIN) - DICIONÁRIOS ===")
    for d in a_dicts:
        print(d)

    print("\n=== CONSULTA B (LEFT JOIN) - DICIONÁRIOS ===")
    for d in b_dicts:
        print(d)

    print("\n=== CONSULTA C (RIGHT JOIN) - DICIONÁRIOS ===")
    for d in c_dicts:
        print(d)

    # LISTAS
    listas_a, listas_b, listas_c = consultar_como_listas()

    print("\n=== CONSULTA A (INNER JOIN) - LISTAS ===")
    for linha in listas_a:
        print(linha)

    print("\n=== CONSULTA B (LEFT JOIN) - LISTAS ===")
    for linha in listas_b:
        print(linha)

    print("\n=== CONSULTA C (RIGHT JOIN) - LISTAS ===")
    for linha in listas_c:
        print(linha)