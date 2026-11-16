-- =====================================================================
-- PMR3304 - Segunda entrega de laboratorio
-- Secao 4: exercicios com SQL sobre o db.sqlite3 da aplicacao
--
-- Tabelas geradas pelo ORM do Django:
--   blog_post             id, titulo, conteudo, data_postagem
--   blog_comment          id, texto, data_postagem, autor_id, post_id
--   blog_category         id, nome, descricao
--   blog_post_categorias  id, post_id, category_id   (tabela do ManyToMany)
--
-- Rode uma de cada vez no DB Browser for SQLite para tirar o printscreen
-- de cada resultado.
-- =====================================================================


-- ---------------------------------------------------------------------
-- 1. Todos os posts, ordenados pela data, sendo o mais recente primeiro.
-- ---------------------------------------------------------------------
SELECT
    id,
    titulo,
    data_postagem
FROM blog_post
ORDER BY data_postagem DESC;


-- ---------------------------------------------------------------------
-- 2. Para um post com comentarios, todos os seus comentarios.
--    Post 1 = "Guga em 1997: o backhand que ninguem tinha visto".
-- ---------------------------------------------------------------------
SELECT *
FROM blog_comment
WHERE post_id = 1
ORDER BY data_postagem DESC;


-- ---------------------------------------------------------------------
-- 3. Para um post com comentarios, todos os seus comentarios, incluindo
--    todas as colunas da tabela de comentarios (exceto o post_id), o
--    titulo do post e sua data de publicacao renomeada para post_date.
--
--    Colunas de blog_comment sao id, texto, data_postagem, autor_id e
--    post_id; as quatro primeiras entram, post_id fica de fora.
-- ---------------------------------------------------------------------
SELECT
    c.id,
    c.texto,
    c.data_postagem,
    c.autor_id,
    p.titulo,
    p.data_postagem AS post_date
FROM blog_comment AS c
INNER JOIN blog_post AS p
        ON p.id = c.post_id
WHERE c.post_id = 1
ORDER BY c.data_postagem DESC;


-- ---------------------------------------------------------------------
-- 4. Para uma categoria, todos os posts pertencentes a ela, incluindo
--    as colunas da tabela de categoria e da tabela de posts.
--    Categoria escolhida: Saibro.
--
--    O ManyToMany obriga a passar pela tabela intermediaria
--    blog_post_categorias, que guarda os pares post/categoria.
-- ---------------------------------------------------------------------
SELECT
    cat.id          AS categoria_id,
    cat.nome        AS categoria_nome,
    cat.descricao   AS categoria_descricao,
    p.id            AS post_id,
    p.titulo        AS post_titulo,
    p.conteudo      AS post_conteudo,
    p.data_postagem AS post_data_postagem
FROM blog_category AS cat
INNER JOIN blog_post_categorias AS pc
        ON pc.category_id = cat.id
INNER JOIN blog_post AS p
        ON p.id = pc.post_id
WHERE cat.nome = 'Saibro'
ORDER BY p.data_postagem DESC;


-- ---------------------------------------------------------------------
-- 5. Todas as categorias que possuem dois ou mais posts.
--
--    HAVING e nao WHERE: o filtro e sobre o resultado da agregacao,
--    que so existe depois do GROUP BY.
-- ---------------------------------------------------------------------
SELECT
    cat.id,
    cat.nome,
    COUNT(pc.post_id) AS total_posts
FROM blog_category AS cat
INNER JOIN blog_post_categorias AS pc
        ON pc.category_id = cat.id
GROUP BY cat.id, cat.nome
HAVING COUNT(pc.post_id) >= 2
ORDER BY total_posts DESC, cat.nome;
