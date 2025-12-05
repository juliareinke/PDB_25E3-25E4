from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from db import engine
from tabelas_web import PaginaWiki, SecaoWiki, ErroWiki

# TESTE DE PERFORMANCE 5

SessionLocal = sessionmaker(bind=engine)

# Seguindo meu tema de projeto, peguei a página 'Música' da Wikipedia
URL_MUSICA = "https://pt.wikipedia.org/wiki/M%C3%BAsica"


def acessar_url(url: str):
    """
    Faz o acesso à URL usando urllib.
    Retorna o response em caso de sucesso, ou None em caso de falha.
    """
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urlopen(request)
        return response

    except HTTPError as ex:
        print(f"Erro HTTP ao acessar {url}: {ex.code} - {ex.reason}")
        return None

    except URLError as ex:
        print(f"Erro de URL ao acessar {url}: {ex.reason}")
        return None

    except Exception as ex:
        print(f"Erro inesperado ao acessar {url}: {ex}")
        return None


def registrar_erro(session, url: str, mensagem: str):
    """
    Registra um erro ocorrido durante o scraping na tabela erros_wiki.
    """
    erro = ErroWiki(
        url=url,
        mensagem=mensagem,
        data_erro=datetime.now()
    )
    session.add(erro)
    session.commit()


def coletar_pagina_musica():
    """
    Realiza o scraping da página 'Música' da Wikipédia:
    - Acessa o HTML
    - Extrai o título e as seções
    - Salva nas tabelas correspondentes
    - Em caso de falha, registra o erro
    """
    session = SessionLocal()

    try:
        response = acessar_url(URL_MUSICA)

        if response is None:
            registrar_erro(session, URL_MUSICA, "Falha ao carregar a página (response None).")
            print("Não foi possível carregar a página de Música.")
            return

        status_code = response.getcode()
        html = response.read().decode("utf-8", errors="ignore")

        soup = BeautifulSoup(html, "html.parser")

        h1 = soup.find("h1")
        titulo = h1.get_text(strip=True) if h1 else "Sem título"

        # Verifica se essa página já existe no banco
        pagina = (
            session.query(PaginaWiki)
            .filter(PaginaWiki.url == URL_MUSICA)
            .first()
        )

        # Se não existir, cria. Se existir, atualiza
        if pagina is None:
            pagina = PaginaWiki(
                url=URL_MUSICA,
                titulo=titulo,
                status_code=status_code,
                data_coleta=datetime.now()
            )
            session.add(pagina)
            session.commit()
            session.refresh(pagina)
        else:
            pagina.titulo = titulo
            pagina.status_code = status_code
            pagina.data_coleta = datetime.now()
            session.commit()

        # Se já tinha seções dessa página no banco, apaga pra substituir pelas novas
        session.query(SecaoWiki).filter(
            SecaoWiki.id_pagina == pagina.id_pagina
        ).delete()
        session.commit()

        # Pega seções <h2> e <h3> da página
        secoes_html = soup.select("h2, h3")
        ordem = 1

        for tag in secoes_html:
            nivel = int(tag.name[1])  # vira 2 ou 3
            titulo_secao = tag.get_text(strip=True)

            #Tenta pegar o primeiro parágrafo relacionado à seção
            conteudo_resumido = ""
            prox_el = tag.find_next_sibling()
            while prox_el and prox_el.name not in ["h2", "h3"]:
                if prox_el.name == "p":
                    conteudo_resumido = prox_el.get_text(strip=True)[:500]
                    break
                prox_el = prox_el.find_next_sibling()

            secao = SecaoWiki(
                id_pagina=pagina.id_pagina,
                titulo_secao=titulo_secao,
                nivel=nivel,
                ordem=ordem,
                conteudo_resumido=conteudo_resumido
            )
            session.add(secao)
            ordem += 1

        session.commit()

    except Exception as ex:
        registrar_erro(session, URL_MUSICA, f"Exceção durante scraping: {ex}")
        print(f"Erro ao processar a página: {ex}")

    finally:
        session.close()


def relatorio_console():
    """
    Mostra um resumo geral do scraping:
    - Total de páginas salvas
    - Total de seções extraídas
    - Inner join mostrando quantas seções cada página tem
    - Erros registrados
    - Falhas agrupadas por URL
    """
    session = SessionLocal()

    print("\nRELATÓRIO PÁGINA WIKIPEDIA - MÚSICA")

    # Quantas páginas existem no banco
    total_paginas = session.query(func.count(PaginaWiki.id_pagina)).scalar()
    print(f"Total de páginas salvas: {total_paginas}")

    # Quantas seções já foram salvas
    total_secoes = session.query(func.count(SecaoWiki.id_secao)).scalar()
    print(f"Total de seções salvas: {total_secoes}")

    # Inner join de páginas x seções
    print("\nSeções por página (INNER JOIN paginas_wiki x secoes_wiki):")
    rows = (
        session.query(
            PaginaWiki.titulo,
            func.count(SecaoWiki.id_secao).label("qtd_secoes")
        )
        .join(SecaoWiki, PaginaWiki.id_pagina == SecaoWiki.id_pagina)
        .group_by(PaginaWiki.titulo)
        .all()
    )
    for titulo, qtd in rows:
        print(f"- {titulo}: {qtd} seções")

    # Quantos erros aconteceram
    total_erros = session.query(func.count(ErroWiki.id_erro)).scalar()
    print(f"\nTotal de erros registrados: {total_erros}\n")

    if total_erros > 0:
        print("\nDetalhes dos erros:")
        erros = session.query(ErroWiki).all()
        for erro in erros:
            print(f"- URL: {erro.url} | Mensagem: {erro.mensagem} | Data: {erro.data_erro}")

        # Quantas falhas por URL 
        print("\nFalhas por URL:")
        falhas_por_url = (
            session.query(
                ErroWiki.url,
                func.count(ErroWiki.id_erro).label("qtd_falhas")
            )
            .group_by(ErroWiki.url)
            .all()
        )
        for url, qtd in falhas_por_url:
            print(f"- {url}: {qtd} falha(s)")

    session.close()


if __name__ == "__main__":
    coletar_pagina_musica()
    relatorio_console()
