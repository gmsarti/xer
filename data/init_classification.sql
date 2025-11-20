CREATE TABLE IF NOT EXISTS classificacoes (
    classificacao_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_classificacao TEXT NOT NULL,
    framework TEXT NOT NULL,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS conto_classificacao (
    conto_id INTEGER NOT NULL,
    classificacao_id INTEGER NOT NULL,
    PRIMARY KEY (conto_id, classificacao_id),
    FOREIGN KEY (conto_id) REFERENCES tales(id) ON DELETE CASCADE,
    FOREIGN KEY (classificacao_id) REFERENCES classificacoes(classificacao_id) ON DELETE CASCADE
);

INSERT INTO classificacoes (nome_classificacao, framework, descricao) VALUES
    ('ATU 333', 'ATU', 'Chapeuzinho Vermelho'),
    ('ATU 510A', 'ATU', 'Cinderela'),
    ('ATU 709', 'ATU', 'Branca de Neve'),
    ('Superando o Monstro', 'Booker', NULL),
    ('De Pobre a Rico', 'Booker', NULL),
    ('Viagem e Retorno', 'Booker', NULL),
    ('Herói', 'Propp_Papel', NULL),
    ('Vilão', 'Propp_Papel', NULL),
    ('Doador', 'Propp_Papel', NULL);

-- Exemplo: vincular o conto com id 1 (se existir) às classificações ATU 333, Superando o Monstro e Vilão
INSERT INTO conto_classificacao (conto_id, classificacao_id)
SELECT 1, classificacao_id FROM classificacoes WHERE nome_classificacao IN ('ATU 333','Superando o Monstro','Vilão');
