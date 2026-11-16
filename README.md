# Quadra Lenta

Blog de tênis feito com Django. Segunda entrega de laboratório de PMR3304
(Sistemas de Informação) — aplicação CRUD com posts, comentários e categorias.

O conteúdo dos posts é guardado como HTML e renderizado com o filtro `safe`,
o que permite que o corpo de cada matéria traga placar de partida, tabela de
estatísticas e quadro de títulos sem depender de editor de texto rico.

## Rodando localmente

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py popular_banco  # cria posts, categorias, usuários e comentários
python manage.py runserver
```

O site sobe em <http://localhost:8000/> e o administrador em
<http://localhost:8000/admin/>.

O comando `popular_banco` cria um super-usuário de desenvolvimento; o login
está no cabeçalho de `blog/management/commands/popular_banco.py`. Serve só
para a máquina local — troque antes de pôr qualquer coisa no ar.

## Estrutura

```
tennisblog/      configuração do projeto
blog/            aplicação: modelos, views, forms, admin, urls
templates/       base.html e os templates do blog
static/css/      folha de estilo
consultas.sql    as cinco consultas da seção 4 do enunciado
```

## Modelos

| Modelo     | Campos                                           |
|------------|--------------------------------------------------|
| `Post`     | título, conteúdo (HTML), data de postagem        |
| `Comment`  | post, autor (`AUTH_USER_MODEL`), texto, data     |
| `Category` | nome, descrição — ligada a `Post` por ManyToMany |

## Histórico do git

As três versões das views pedidas na parte 1 estão cada uma em seu commit, e
cada parte do enunciado tem o seu branch, com merge no principal:

```
*   Merge do branch categories
|\
| * Sistema de categorias de posts
|/
*   Merge do branch comments
|\
| * Sistema de comentarios nos posts
|/
* CRUD de posts com as classes genericas do Django      <- versão 3
* CRUD de posts com views funcionais usando Django form <- versão 2
* CRUD de posts com views funcionais, sem Django forms  <- versão 1
* Modelo Post registrado no administrador
* Estrutura inicial do projeto Django
```

Para ver uma versão específica do arquivo de views:

```bash
git show <commit>:blog/views.py
```

## Implantação

Preparado para o Render: `requirements.txt` com gunicorn e whitenoise,
`build.sh` rodando `collectstatic` e `migrate`, e `STATIC_ROOT` definido.
Antes de publicar, ajuste `DEBUG`, `SECRET_KEY` e `ALLOWED_HOSTS` em
`tennisblog/settings.py`.
