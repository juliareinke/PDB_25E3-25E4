from db import engine
import pandas as pd
from sqlalchemy import text

# CONEXÃO COM BANCO DE DADOS em db.py
# TESTE DE PERFOMANCE 4

def print_artistas(mensagem: str):
    """
    Exibe o estado atual da tabela artistas para conferência.
    """
    with engine.connect() as conn:
        resultado = conn.execute(text("""
            SELECT id_artista, nome, instrumento_principal, genero_musical, data_entrada
            FROM artistas
            ORDER BY id_artista;
        """))

        print(f"\n--- {mensagem} ---")
        for linha in resultado:
            print(dict(linha._mapping))


def upsert_artistas(json_path: str = "artistas_upsert.json"):
    """
    Realiza UPSERT (INSERT + UPDATE) em massa na tabela artistas,
    lendo os dados de um arquivo JSON orientado a registros.

    Espera um JSON no formato:
    [
      {
        "id_artista": 1,
        "nome": "Alice (Atualizada)",
        "instrumento_principal": "Voz",
        "genero_musical": "Pop",
        "data_entrada": "2025-10-15"
      },
      ...
    ]
    """
    df = pd.read_json(json_path)
    df.columns = ["id_artista", "nome", "instrumento_principal", "genero_musical", "data_entrada"]

    tabela = "artistas"
    pk = "id_artista"

    colunas = list(df.columns)
    cols_str = ", ".join(colunas)                       
    vals_str = ", ".join([f":{c}" for c in colunas])      

    set_str = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in colunas if c != pk]
    )

    sql_upsert = text(f"""
        INSERT INTO {tabela} ({cols_str})
        VALUES ({vals_str})
        ON CONFLICT ({pk})
        DO UPDATE SET
            {set_str};
    """)

    registros = df.to_dict(orient="records")

    with engine.begin() as conn: 
        conn.execute(sql_upsert, registros)

    print(f"\nUPSERT em massa concluído a partir de '{json_path}'.")


def delete_artistas(json_path: str = "artistas_delete.json"):
    """
    Realiza deleção massiva na tabela artistas,
    lendo um JSON orientado a registros contendo os IDs a serem removidos.

    Exemplo de JSON:
    [
      { "id_artista": 3 },
      { "id_artista": 4 }
    ]
    """
    df_del = pd.read_json(json_path)
    df_del.columns = ["id_artista"]

    registros = df_del.to_dict(orient="records")

    sql_delete = text("""
        DELETE FROM artistas
        WHERE id_artista = :id_artista;
    """)

    with engine.begin() as conn:
        conn.execute(sql_delete, registros)

    print(f"\nDeleção em massa concluída a partir de '{json_path}'.")


if __name__ == "__main__":
    # Conferência antes do UPSERT
    print_artistas("Estado da tabela 'artistas' ANTES do UPSERT")

    # UPSERT (inserção/atualização)
    upsert_artistas("artistas_upsert.json")

    # Conferência depois do UPSERT
    print_artistas("Estado da tabela 'artistas' DEPOIS do UPSERT")

    # Conferência antes da deleção
    print_artistas("Estado da tabela 'artistas' ANTES da deleção")

    # Deleção massiva
    delete_artistas("artistas_delete.json")

    # Conferência depois da deleção
    print_artistas("Estado da tabela 'artistas' DEPOIS da deleção")
