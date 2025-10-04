import os
from dotenv import load_dotenv

import pandas as pd
from datetime import datetime
import mysql.connector

load_dotenv() 

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DATABASE")
port = "3306" # Porta padrão do mySQL

df = pd.read_excel("tabela_funcionarios_MAESTRO.xlsx", sheet_name="FUNCIONARIOS")
print(df)

cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
cursor = cnx.cursor()

"""
for _,col in df.iterrows():
    cursor.execute(
        '''
        insert into funcionarios_maestro values (%s,%s,%s,%s,%s,%s,%s)
        ''',(col["ID do Funcionário"],
             col["Nome"],
             col["Cargo"],
             col["Departamento"],
             col["Salário (R$)"],
             col["Data da Contratação"], 
             col["Treinamento Concluído"]
             )
    )

cnx.commit()   
cnx.close()
cursor.close()

print("DataFrame gravado com sucesso na tabela do mySQL.")
"""

#1) Selecione todos os funcionários que trabalham no departamento de Produção Musical(era TI).
query = "SELECT * FROM funcionarios_maestro WHERE departamento = 'Produção Musical'"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#2) Selecione os nomes dos funcionários que possuem um salário maior que 5.000,00
query = "SELECT nome FROM funcionarios_maestro WHERE salario > 5000"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#3) Selecione o nome e a data de contratação dos funcionários que foram contratados após 01/01/2022.
query = "SELECT nome, data_contratacao FROM funcionarios_maestro WHERE data_contratacao > '2022-01-01'"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#4) Selecione o departamento e o salário médio de cada departamento.
query = "SELECT departamento, AVG(salario) FROM funcionarios_maestro GROUP BY departamento"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#5) Selecione o nome e o cargo dos funcionários que possuem "Sou" (Sousa e Souza) no nome.
query = "SELECT nome, cargo FROM funcionarios_maestro WHERE nome LIKE '%Sou%'"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#6) Selecione todos os funcionários que têm treinamento concluído.
query = "SELECT * FROM funcionarios_maestro WHERE treinamento_concluido = TRUE"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#7) Selecione o nome e o departamento dos Engenheiros(a).
query = "SELECT nome, departamento FROM funcionarios_maestro WHERE cargo LIKE 'Engenheir%'"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#8) Selecione o nome dos funcionários e seus salários ordenados de forma decrescente pelo salário.
query = "SELECT nome, salario FROM funcionarios_maestro ORDER BY salario DESC"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#9) Selecione o nome e o ID dos funcionários que foram contratados no ano de 2023.
query = "SELECT nome, id_funcionario FROM funcionarios_maestro WHERE data_contratacao BETWEEN '2023-01-01' AND '2023-12-31'"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#10) Selecione o nome dos funcionários que trabalham no departamento Marketing & Vendas e possuem um salário menor ou igual a 5.000,00.
query = "SELECT nome FROM funcionarios_maestro WHERE departamento = 'Marketing & Vendas' AND salario <= 5000"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#11) Selecione o nome dos funcionários que são Gerentes ou Diretores.
query = "SELECT nome FROM funcionarios_maestro WHERE cargo LIKE 'Gerente%' OR cargo LIKE 'Diretor%'"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#12) Selecione o nome dos funcionários e os anos de experiência (considerando que estamos em 2025).
query = "SELECT nome, (YEAR('2025-01-01') - YEAR(data_contratacao)) AS anos_experiencia FROM funcionarios_maestro ORDER BY anos_experiencia DESC"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#13) Selecione o nome e o departamento dos funcionários, ordenados pelo nome em ordem alfabética.
query = "SELECT nome, departamento FROM funcionarios_maestro ORDER BY nome ASC"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#14) Selecione o nome e o cargo dos funcionários cujo nome começa com 'João'.
query = "SELECT nome, cargo FROM funcionarios_maestro WHERE nome LIKE 'João%'"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")

#15) Selecione a quantidade de funcionários em cada departamento.
query = "SELECT departamento, COUNT(id_funcionario) AS quantidade_funcionarios FROM funcionarios_maestro GROUP BY departamento"
df = pd.read_sql_query(query, cnx)
print(df)

print("\n************************************\n")