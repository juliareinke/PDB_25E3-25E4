CREATE SCHEMA maestro_estudio;

USE maestro_estudio;

CREATE TABLE Funcionarios_Maestro (
    id_funcionario INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(80) NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    data_contratacao DATETIME NOT NULL,
    treinamento_concluido BOOLEAN NOT NULL
);
