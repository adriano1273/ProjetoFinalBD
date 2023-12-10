DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS emprestimo;
DROP TABLE IF EXISTS item_emprestimo;
DROP TABLE IF EXISTS livro;
DROP TABLE IF EXISTS local_fisico;
DROP TABLE IF EXISTS materiais_didaticos;
DROP TABLE IF EXISTS usuario;

-- Table: Categoria
CREATE TABLE IF NOT EXISTS categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    nome TEXT NOT NULL
);

-- Table: Emprestimo
CREATE TABLE IF NOT EXISTS emprestimo (
    id_usuario INTEGER NOT NULL,
    data_emprestimo DATE NOT NULL,
    data_devolucao DATE NOT NULL,
    status TEXT,
    id_item INTEGER NOT NULL REFERENCES item_emprestimo (id),
    PRIMARY KEY (id_usuario, id_item),
    FOREIGN KEY (id_usuario) REFERENCES usuario (ID)
);

-- Table: Item_emprestimo
CREATE TABLE IF NOT EXISTS item_emprestimo (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    id_livro REFERENCES Livro (ISBN),
    id_material REFERENCES materiais_didaticos (ID)
);

-- Table: Livro
CREATE TABLE IF NOT EXISTS livro (
    ISBN INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    titulo TEXT NOT NULL,
    autor TEXT,
    descricao TEXT,
    data_aquisicao DATE,
    estado_conservacao TEXT,
    url_foto_capa TEXT,
    localizacao_fisica INTEGER REFERENCES local_fisico (id),
    categoria INTEGER REFERENCES categoria (id)
);

-- Table: Local_fisico
CREATE TABLE IF NOT EXISTS local_fisico (
    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    nome TEXT NOT NULL
);

-- Table: Materiais_didaticos
CREATE TABLE IF NOT EXISTS materiais_didaticos (
    ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
    descricao TEXT,
    numero_serie TEXT,
    data_aquisicao DATE,
    estado_conservacao TEXT,
    url_foto_material TEXT,
    localizacao_fisica INTEGER REFERENCES local_fisico (id),
    categoria INTEGER REFERENCES categoria (id)
);

-- Table: Usuario
CREATE TABLE IF NOT EXISTS usuario (
    ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    sobrenome TEXT,
    funcao TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT UNIQUE NOT NULL,
    url_foto TEXT
);
