DROP TABLE IF EXISTS artista_projeto;
DROP TABLE IF EXISTS sessoes;
DROP TABLE IF EXISTS artistas;
DROP TABLE IF EXISTS projetos;
DROP TABLE IF EXISTS estudios;

CREATE TABLE artistas (
  id_artista           SERIAL PRIMARY KEY,
  nome                 VARCHAR(100) NOT NULL,
  instrumento_principal VARCHAR(60),
  genero_musical       VARCHAR(40),
  data_entrada         DATE DEFAULT CURRENT_DATE
);

CREATE TABLE projetos (
  id_projeto   SERIAL PRIMARY KEY,
  nome         VARCHAR(120) NOT NULL,
  status       VARCHAR(20) NOT NULL DEFAULT 'em_producao',
  data_inicio  DATE,
  data_fim     DATE,
  orcamento    NUMERIC(12,2)
);

CREATE TABLE estudios (
  id_estudio SERIAL PRIMARY KEY,
  nome       VARCHAR(60) NOT NULL UNIQUE,
  capacidade INTEGER
);

CREATE TABLE sessoes (
  id_sessao      SERIAL PRIMARY KEY,
  id_projeto     INTEGER NOT NULL REFERENCES projetos(id_projeto) ON DELETE CASCADE,
  id_estudio     INTEGER NOT NULL REFERENCES estudios(id_estudio) ON DELETE RESTRICT,
  data_horario   TIMESTAMP NOT NULL,
  duracao_horas  NUMERIC(4,2) NOT NULL,
  status         VARCHAR(20) NOT NULL DEFAULT 'Agendada'
);

CREATE TABLE artista_projeto (
  id_artista INTEGER NOT NULL REFERENCES artistas(id_artista) ON DELETE CASCADE,
  id_projeto INTEGER NOT NULL REFERENCES projetos(id_projeto) ON DELETE CASCADE,
  PRIMARY KEY (id_artista, id_projeto)
);

INSERT INTO artistas (nome, instrumento_principal, genero_musical) VALUES
 ('Alice', 'Voz', 'Pop'),
 ('Bruno', 'Guitarra', 'Rock'),
 ('Chiara', 'Teclado', 'Gospel');

INSERT INTO projetos (nome, status, data_inicio, orcamento) VALUES
 ('Álbum Verão', 'em_producao', '2025-10-01', 50000),
 ('Single Outono', 'em_producao', '2025-10-10', 15000),
 ('EP Inverno', 'concluido', '2025-08-01', 20000);

INSERT INTO estudios (nome, capacidade) VALUES
 ('Estúdio A', 4),
 ('Estúdio B', 6);

INSERT INTO artista_projeto (id_artista, id_projeto) VALUES
 (1, 1),  
 (2, 1),  
 (1, 2);  

INSERT INTO sessoes (id_projeto, id_estudio, data_horario, duracao_horas, status) VALUES
 (1, 1, '2025-11-05 14:00', 2.0, 'Agendada'),
 (1, 2, '2025-11-06 10:00', 3.5, 'Agendada'),
 (2, 1, '2025-11-07 09:30', 2.0, 'Concluída');

-- CONSULTA A (INNER JOIN)
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

-- CONSULTA B (LEFT JOIN)
SELECT
  p.id_projeto,
  p.nome AS nome_projeto,
  s.id_sessao,
  s.data_horario,
  s.status AS status_sessao
FROM projetos p
LEFT JOIN sessoes s ON s.id_projeto = p.id_projeto
ORDER BY p.id_projeto, s.data_horario;

-- CONSULTA C (RIGHT JOIN)
SELECT
  p.id_projeto,
  p.nome AS nome_projeto,
  ap.id_artista
FROM artista_projeto ap
RIGHT JOIN projetos p ON ap.id_projeto = p.id_projeto
ORDER BY p.id_projeto;
