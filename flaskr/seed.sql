-- Table: Categoria
INSERT INTO Categoria (id, nome) VALUES (3, 'Terror');
INSERT INTO Categoria (id, nome) VALUES (2, 'Poesia');
INSERT INTO Categoria (id, nome) VALUES (1, 'Distopia');
INSERT INTO Categoria (id, nome) VALUES (4, 'Educacional');

-- Table: Emprestimo
INSERT INTO Emprestimo (id_item, id_usuario, data_emprestimo, data_devolucao, status) VALUES (1, 2, '20-11-2022', '20-12-2022', 'Atrasado');
INSERT INTO Emprestimo (id_item, id_usuario, data_emprestimo, data_devolucao, status) VALUES (2, 3, '20-01-2021', '20-02-2021', 'Devolvido');
INSERT INTO Emprestimo (id_item, id_usuario, data_emprestimo, data_devolucao, status) VALUES (3, 3, '20-02-2021', '20-03-2021', 'Emprestado');

-- Table: Item_emprestimo
INSERT INTO Item_emprestimo (id, id_livro, id_material) VALUES (1, 1, NULL);
INSERT INTO Item_emprestimo (id, id_livro, id_material) VALUES (2, NULL, 2);
INSERT INTO Item_emprestimo (id, id_livro, id_material) VALUES (3, 1, NULL);

-- Table: Livro
INSERT INTO Livro (ISBN, titulo, autor, descricao, data_aquisicao, estado_conservacao, url_foto_capa, localizacao_fisica, categoria) VALUES (1, '1984', 'George Orwell', NULL, '2022-12-12', 'Novo', NULL, 3, 1);
INSERT INTO Livro (ISBN, titulo, autor, descricao, data_aquisicao, estado_conservacao, url_foto_capa, localizacao_fisica, categoria) VALUES (2, 'O senhor das moscas', 'Willian Golding', NULL, '2022-12-12', 'Regular', NULL, 3, 1);
INSERT INTO Livro (ISBN, titulo, autor, descricao, data_aquisicao, estado_conservacao, url_foto_capa, localizacao_fisica, categoria) VALUES (3, 'Lira dos Vinte Anos', 'Álvares de Azevedo', NULL, '2022-12-12', 'Regular', 'https://books.google.com.br/books/publisher/content?id=tAS6DAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70Eeosm0YJTzepOzbyS-rEe_wxyd1EtrJ5m4V7FLBJ65BWfqj1RUYjjeQeSGYFyiCqwpXE-ix7rH6DB2xn8Y99CCSgsEvF3mhOG4QmhvoeFrk0u-_-BynIAVgMNakp6lAguDAMI', 3, 2);

-- Table: Local_fisico
INSERT INTO Local_fisico (id, nome) VALUES (1, 'Estante 1');
INSERT INTO Local_fisico (id, nome) VALUES (2, 'Estante 2');
INSERT INTO Local_fisico (id, nome) VALUES (3, 'Estante 3');
INSERT INTO Local_fisico (id, nome) VALUES (4, 'Estante virtual');

-- Table: Materiais_didaticos
INSERT INTO Materiais_didaticos (ID, descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material, localizacao_fisica, categoria) VALUES (1, 'jogo educativo', 'XY123-4567-ABCD', '12/11/2023', 'novo', NULL, 1, 4);
INSERT INTO Materiais_didaticos (ID, descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material, localizacao_fisica, categoria) VALUES (2, 'software de simulação', '7890-WXYZ-1234', '12/11/2023', 'regular', NULL, 1, 4);
INSERT INTO Materiais_didaticos (ID, descricao, numero_serie, data_aquisicao, estado_conservacao, url_foto_material, localizacao_fisica, categoria) VALUES (3, 'kit de experimentos', 'LMN5678-QWER-90', '12/11/2023', 'desgastado', NULL, 4, 4);

-- Table: Usuario
INSERT INTO Usuario (ID, nome, sobrenome, funcao, login, senha, url_foto) VALUES (1, 'João', 'Silva', 'admin', 'admin', '21232f297a57a5a743894a0e4a801fc3', '');
INSERT INTO Usuario (ID, nome, sobrenome, funcao, login, senha, url_foto) VALUES (2, 'José', 'Souza', 'membro', 'login', 'e8d95a51f3af4a3b134bf6bb680a213a', '');
INSERT INTO Usuario (ID, nome, sobrenome, funcao, login, senha, url_foto) VALUES (3, 'Maria', 'Pereira', 'membro', 'maria', '34ae07655b9a94e90556aff79bfd60b0', '');
